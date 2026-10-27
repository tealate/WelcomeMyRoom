"""Validate authored assets and produce the portable distribution."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import zipfile
from PIL import Image
from build_space_editor import ROOT, DP, RP, PALETTES
from editor_block_config import resource_path
from mark_textures_translucent import image_pixels, process_png


def main():
    checks=[]
    json_files=[]
    for root in (DP,RP):
        for p in sorted(root.rglob("*")):
            if p.is_file() and p.suffix in (".json",".mcmeta"):
                json.loads(p.read_text(encoding="utf-8"))
                json_files.append(p.relative_to(ROOT).as_posix())
            if p.suffix==".mcfunction":
                for i,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
                    if line.rstrip()!=line:
                        raise ValueError(f"Trailing whitespace: {p}:{i}")
    checks.append(f"Parsed {len(json_files)} JSON/mcmeta files")
    png_results=[]
    for name,(_,_,source_name) in PALETTES.items():
        source=resource_path(ROOT,source_name,"textures",".png")
        dest=RP/f"assets/editor/textures/block/{name}_maskable.png"
        with Image.open(source) as im:
            before=image_pixels(im.convert("RGBA"))
        with Image.open(dest) as im:
            after=image_pixels(im.convert("RGBA"))
        assert len(before)==len(after)
        changed=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b]
        assert all(a[:3]==b[:3] for a,b in zip(before,after)), dest
        already=any(0<a[3]<255 for a in before)
        if already:
            assert not changed, dest
            reason="既存の複製元に部分αがあるため、追加のピクセル変更はスキップ"
        else:
            assert len(changed)==1, dest
            index=changed[0]
            assert before[index][3]==255 and after[index][3]==254, dest
            reason="1ピクセルだけα255→254、RGBおよび他のαは保持"
        assert process_png(dest,True)=="already-translucent", dest
        png_results.append((dest.relative_to(ROOT).as_posix(),reason))
    for name in ("mask_body","selection","guide"):
        p=RP/f"assets/editor/textures/block/{name}.png"
        with Image.open(p) as im:
            alphas={pixel[3] for pixel in image_pixels(im.convert("RGBA"))}
        assert alphas==({1} if name=="mask_body" else {0,255}), (p,alphas)
        png_results.append((p.relative_to(ROOT).as_posix(),"新規の描画用画像。全画素α1" if name=="mask_body" else "新規の線表示画像。α0/255のみ"))
    checks.append("5 maskable textures: exact RGB/pixel checks and no-op dry-run passed")
    checks.append("Mask body alpha={1}; selection and guide alpha={0,255}")

    # Custom namespace references must resolve; vanilla parents are provided by
    # the installed game (and present in the original local resource tree).
    for p in RP.rglob("*.json"):
        model=json.loads(p.read_text(encoding="utf-8"))
        references=[]
        if "variants" in model:
            references += [(value["model"],"models",".json") for value in model["variants"].values()]
        references += [(v,"textures",".png") for v in model.get("textures",{}).values() if isinstance(v,str) and not v.startswith("#")]
        for ref,folder,ext in references:
            namespace,path=ref.split(":")
            assert (RP/f"assets/{namespace}/{folder}/{path}{ext}").is_file(), (p,ref)
    checks.append("All custom model/texture references resolved")
    import re
    functions={"editor:"+p.relative_to(DP/"data/editor/function").with_suffix("").as_posix() for p in (DP/"data/editor/function").rglob("*.mcfunction")}
    for p in DP.rglob("*.mcfunction"):
        for ref in re.findall(r"\bfunction (editor:[a-z0-9_./-]+)",p.read_text(encoding="utf-8")):
            assert ref in functions, (p,ref)
    checks.append(f"All references among {len(functions)} functions resolved")

    out=ROOT/"dist/SpaceEditor-1.0"
    out.mkdir(parents=True,exist_ok=True)
    for root,name in ((DP,"SpaceEditor-Datapack.zip"),(RP,"SpaceEditor-Resources.zip")):
        with zipfile.ZipFile(out/name,"w",zipfile.ZIP_DEFLATED) as z:
            for p in sorted(root.rglob("*")):
                if p.is_file():
                    z.write(p,p.relative_to(root).as_posix())
        with zipfile.ZipFile(out/name) as z:
            assert "pack.mcmeta" in z.namelist()
            assert z.testzip() is None
    shutil.copyfile(ROOT/"README_SpaceEditor.md",out/"はじめに.md")
    (out/"tools").mkdir(exist_ok=True)
    for name in ("editor_data.py","Export-Level.ps1","Export-Level.cmd"):
        shutil.copyfile(ROOT/"tools"/name,out/"tools"/name)
    shutil.copyfile(ROOT/"tools/editor_block_config.py",out/"tools/editor_block_config.py")
    shutil.copyfile(ROOT/"space_editor_blocks.json",out/"space_editor_blocks.json")
    # Windows PowerShell 5 needs a BOM to recognize Japanese UTF-8 scripts.
    ps=out/"tools/Export-Level.ps1"
    ps.write_text(ps.read_text(encoding="utf-8-sig"),encoding="utf-8-sig")
    manifest={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob("*")) if p.is_file() and p.name!="SHA256.json"}
    (out/"SHA256.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    log=["# Space Editor アセット検証", "", *["- "+c for c in checks], "", "## PNG（すべて独立した配布用リソースパック内）", ""]
    log += [f"- `{path}` — {result}" for path,result in png_results]
    log += ["", "## JSON / pack.mcmeta", "", *["- `"+p+"`" for p in json_files], "", "build_space_editor.pyは専用アセット28ファイルを有効なルートassets/にも反映します。元のバニラ画像とルートpack.mcmetaは変更しません。", ""]
    (ROOT/"VALIDATION_ASSETS.md").write_text("\n".join(log),encoding="utf-8")
    bundle=ROOT/"dist/SpaceEditor-1.0.zip"
    with zipfile.ZipFile(bundle,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file(): z.write(p,p.relative_to(out.parent).as_posix())
    print("\n".join(checks))
    print(f"Distribution: {bundle}")


if __name__=="__main__":
    main()
