"""Export saved Space Editor NBT to JSON, or compile JSON into an import pack.

Python 3.10+; standard library only. Does not write to the source world.
Usage: python editor_data.py export WORLD_OR_DAT --out level.json
       python editor_data.py inspect level.json
       python editor_data.py pack level.json --out SpaceEditor-Level.zip
"""
from __future__ import annotations
import argparse
import gzip
import io
import json
import math
from pathlib import Path
import struct
import zipfile

from editor_block_config import load_editor_block_config


class NBTReader:
    def __init__(self, raw: bytes):
        self.stream = io.BytesIO(raw)

    def read(self, size):
        value = self.stream.read(size)
        if len(value) != size:
            raise ValueError("Truncated NBT file")
        return value

    def number(self, fmt):
        return struct.unpack(">" + fmt, self.read(struct.calcsize(fmt)))[0]

    def string(self):
        # Java's modified UTF-8 encodes astral characters as surrogate pairs.
        raw = self.read(self.number("H")).replace(b"\xc0\x80", b"\x00")
        return raw.decode("utf-8", "surrogatepass").encode("utf-16-le", "surrogatepass").decode("utf-16-le")

    def payload(self, kind, depth=0):
        if depth > 64:
            raise ValueError("NBT nesting is too deep")
        if kind in (1, 2, 3, 4, 5, 6):
            return self.number({1:"b",2:"h",3:"i",4:"q",5:"f",6:"d"}[kind])
        if kind == 8:
            return self.string()
        if kind == 10:
            result = {}
            while True:
                child = self.number("B")
                if child == 0:
                    return result
                name = self.string()
                result[name] = self.payload(child, depth + 1)
        if kind in (7, 9, 11, 12):
            child = self.number("B") if kind == 9 else {7:1,11:3,12:4}[kind]
            count = self.number("i")
            if not 0 <= count <= 10_000_000:
                raise ValueError("Invalid NBT array length")
            return [self.payload(child, depth + 1) for _ in range(count)]
        raise ValueError(f"Unsupported NBT type: {kind}")

    def root(self):
        kind = self.number("B")
        if kind != 10:
            raise ValueError("Expected named root compound")
        self.string()
        return self.payload(kind)


def load_state(path: Path):
    if path.is_dir():
        candidates = [path / "data/editor/command_storage.dat", path / "data/command_storage_editor.dat"]
        path = next((p for p in candidates if p.is_file()), candidates[0])
    raw = path.read_bytes()
    if raw.startswith(b"\x1f\x8b"):
        raw = gzip.decompress(raw)
    root = NBTReader(raw).root()
    contents = root.get("data", root).get("contents", {})
    state = contents.get("data")
    if not isinstance(state, dict) or "document" not in state:
        raise ValueError("Space Editor document not found. Save and close the world first.")
    return state, path


def integer(value, label, lo=-1_000_000, hi=1_000_000):
    if type(value) is not int or not lo <= value <= hi:
        raise ValueError(f"{label}: expected integer {lo}..{hi}")
    return value


def validate(doc):
    if not isinstance(doc, dict) or doc.get("schema") != 1:
        raise ValueError("Only schema 1 is supported")
    if not isinstance(doc.get("name","Untitled"),str) or len(doc.get("name","Untitled"))>100:
        raise ValueError("Document name must be a string of at most 100 characters")
    objects = doc.get("objects")
    if not isinstance(objects, list) or len(objects) > 512:
        raise ValueError("objects must be a list of at most 512 entries")
    palettes = doc.get("palettes")
    config_path = Path(__file__).resolve().parents[1] / "space_editor_blocks.json"
    config = load_editor_block_config(config_path, check_textures=False)
    expected = {
        name: {"normal": value["normalBlock"], "maskable": value["carrierBlock"]}
        for name, value in config["maskablePalettes"].items()
    }
    expected["air"] = {"normal":"minecraft:air","maskable":"minecraft:air"}
    if palettes != expected:
        raise ValueError("Palette mapping must match the bundled resource pack")
    ids = set()
    allowed = {"id","label","type","dim","ax","ay","az","bx","by","bz","x1","y1","z1","x2","y2","z2","sx","sy","sz","palette","variant","mode","material","px","py","pz","lox","loy","loz","hix","hiy","hiz","ox","oy","oz","ex","ey","ez","target"}
    for obj in objects:
        if not isinstance(obj, dict) or set(obj)-allowed:
            raise ValueError("Unknown object fields")
        oid = integer(obj.get("id"), "id", 1, 1_000_000_000)
        if oid in ids:
            raise ValueError("Duplicate object id")
        ids.add(oid)
        dim = obj.get("dim")
        if dim not in ("minecraft:overworld","minecraft:the_nether","minecraft:the_end"):
            raise ValueError("Unsupported dimension")
        if not isinstance(obj.get("label",""), str) or len(obj.get("label","")) > 100:
            raise ValueError("Label must be at most 100 characters")
        for axis in "xyz":
            av = integer(obj.get("a"+axis), "a"+axis)
            bv = integer(obj.get("b"+axis), "b"+axis)
            low = integer(obj.get(axis+"1"), axis+"1")
            high = integer(obj.get(axis+"2"), axis+"2")
            if (low, high) != (min(av,bv),max(av,bv)) or not 1 <= high-low+1 <= 32:
                raise ValueError("Invalid selection bounds")
        ylo,yhi = (-64,319) if dim == "minecraft:overworld" else (0,255)
        if not ylo <= obj["y1"] <= obj["y2"] <= yhi:
            raise ValueError("Selection outside dimension build height")
        if obj.get("type") == "block_fill":
            if set(obj) & {"px","py","pz","ox","oy","oz","ex","ey","ez","lox","loy","loz","hix","hiy","hiz","target","material"}:
                raise ValueError("Block operations must not contain display transform fields")
            if obj.get("palette") not in palettes or obj.get("variant") not in ("normal","maskable"):
                raise ValueError("Unknown palette or variant")
            if obj.get("mode","fill") not in ("fill","hollow","outline"):
                raise ValueError("Unknown fill mode")
            for axis in "xyz":
                if obj.get("s"+axis) != obj[axis+"2"]-obj[axis+"1"]+1:
                    raise ValueError("Invalid fill size")
        elif obj.get("type") in ("mask","teleport_volume"):
            if set(obj) & {"palette","variant","mode"} or (obj["type"]=="mask" and "target" in obj):
                raise ValueError("Object contains fields for another operation type")
            if obj["type"] == "mask" and obj.get("material") != "mask_default":
                raise ValueError("Unknown mask material")
            for axis in "xyz":
                offset = integer(obj.get("o"+axis), "offset", -16000,16000)
                expand = integer(obj.get("e"+axis), "expand", -16000,16000)
                low = obj[axis+"1"]*1000+offset-expand
                size = (obj[axis+"2"]-obj[axis+"1"]+1)*1000+2*expand
                integer(obj.get("lo"+axis),"lo"+axis,-1_100_000_000,1_100_000_000)
                integer(obj.get("hi"+axis),"hi"+axis,-1_100_000_000,1_100_000_000)
                if not 1 <= size <= 64000:
                    raise ValueError("Invalid transformed size")
                for field, value in (("p"+axis,low/1000),("s"+axis,size/1000),("lo"+axis,low),("hi"+axis,low+size)):
                    actual = obj.get(field)
                    if not isinstance(actual,(int,float)) or not math.isfinite(actual) or abs(actual-value)>0.000001:
                        raise ValueError("Inconsistent transform: "+field)
            if "target" in obj:
                target=obj["target"]
                if set(target) != {"dim","pos","rotation"} or target["dim"] not in ("minecraft:overworld","minecraft:the_nether","minecraft:the_end"):
                    raise ValueError("Invalid teleport target")
                for name,length,bound in (("pos",3,1_000_000),("rotation",2,360)):
                    if not isinstance(target[name],list) or len(target[name])!=length or any(type(x) not in (float,int) or not math.isfinite(x) or abs(x)>bound for x in target[name]):
                        raise ValueError("Invalid teleport coordinates")
        else:
            raise ValueError("Unknown object type")
    return doc


def snbt(value):
    if isinstance(value,dict):
        return "{"+",".join(json.dumps(k)+":"+snbt(v) for k,v in value.items())+"}"
    if isinstance(value,list):
        return "["+",".join(snbt(v) for v in value)+"]"
    if isinstance(value,str):
        return json.dumps(value,ensure_ascii=False)
    if type(value) is int:
        return str(value)
    if type(value) is float and math.isfinite(value):
        return repr(value)+"d"
    raise ValueError("Unsupported value in document")


def make_pack(doc, dest):
    validate(doc)
    lines=[
        '# Generated by editor_data.py. Replaces the active document; Undo restores it.',
        'execute unless score #enabled se matches 1 run return run tellraw @s {text:"Space Editorを先に導入してください。",color:"red"}',
        'execute if data storage editor:runtime job run return run tellraw @s {text:"処理完了後に再実行してください。",color:"yellow"}',
        'function editor:internal/history/save',
        'data modify storage editor:data document.objects set value []',
        'data modify storage editor:data document.name set value '+snbt(str(doc.get("name","Imported"))),
        'data modify storage editor:data document.palettes set value '+snbt(doc["palettes"]),
    ]
    for obj in doc["objects"]:
        lines.append('data modify storage editor:data document.objects append value '+snbt(obj))
        dest_list="footprints" if obj["type"]=="block_fill" else "display_footprints"
        lines.append('data modify storage editor:data '+dest_list+' append value '+snbt(obj))
    next_id=max((obj["id"] for obj in doc["objects"]),default=0)+1
    lines += ['execute store result score #next se run data get storage editor:data next_id',
              f'scoreboard players set #import_next se {next_id}',
              'scoreboard players operation #next se > #import_next se',
              'execute store result storage editor:data next_id int 1 run scoreboard players get #next se',
              'function editor:internal/revision','function editor:build']
    meta={"pack":{"description":"Space Editor imported level", "min_format":[101,1],"max_format":[101,1]}}
    with zipfile.ZipFile(dest,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("pack.mcmeta",json.dumps(meta))
        z.writestr("data/editor_import/function/load.mcfunction","\n".join(lines)+"\n")
        z.writestr("level.json",json.dumps(doc,ensure_ascii=False,indent=2))
    print(f"Wrote {dest}; install beside Space Editor, then /reload and /function editor_import:load")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("export","inspect","pack"))
    parser.add_argument("source",type=Path)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    if args.command=="export":
        state,path=load_state(args.source)
        doc=validate(state["document"])
        out=args.out or Path("space-editor-level.json")
        out.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"Exported {len(doc['objects'])} objects from {path} to {out}")
        print(f"Revision: {state.get('revision')}; saved build state: {state.get('build_state')}")
    else:
        doc=validate(json.loads(args.source.read_text(encoding="utf-8-sig")))
        if args.command=="pack":
            make_pack(doc,args.out or Path("SpaceEditor-Level.zip"))
        else:
            print(f"{doc.get('name','Untitled')}: {len(doc['objects'])} objects")
            for obj in doc["objects"]:
                print(f"#{obj['id']} {obj['type']} {obj.get('label','')} {obj['dim']} ({obj['x1']},{obj['y1']},{obj['z1']})..({obj['x2']},{obj['y2']},{obj['z2']})")


if __name__=="__main__":
    try:
        main()
    except (OSError,ValueError,KeyError,TypeError,struct.error) as error:
        raise SystemExit(f"Error: {error}") from None
