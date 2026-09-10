"""Static checks for the generated subset; not a Minecraft command parser."""
from pathlib import Path
import json
import math
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'datapacks/spatial_prototype'
FUN = PACK / 'data/prototype/function'


def balanced(text):
    stack, quote, escape = [], None, False
    for c in text:
        if quote:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == quote:
                quote = None
        elif c in '\"\'':
            quote = c
        elif c in '[{(':
            stack.append(c)
        elif c in ']})':
            assert stack and stack.pop() == {']': '[', '}': '{', ')': '('}[c], text
    assert not stack and not quote, text


def snbt(text):
    # This pack emits only compounds, lists, strings, booleans, and numeric
    # scalars. Tokenize before conversion so quoted text cannot be rewritten.
    token = re.compile(r'\s*("(?:\\.|[^"\\])*"|[{}\[\],:]|[^\s{}\[\],:]+)')
    tokens = [m.group(1) for m in token.finditer(text)]
    i = 0

    def value():
        nonlocal i
        t = tokens[i]
        i += 1
        if t == '{':
            out = {}
            while tokens[i] != '}':
                key = tokens[i]
                i += 1
                key = json.loads(key) if key.startswith('"') else key
                assert tokens[i] == ':'
                i += 1
                assert key not in out, key
                out[key] = value()
                if tokens[i] != ',':
                    break
                i += 1
            assert tokens[i] == '}'
            i += 1
            return out
        if t == '[':
            out = []
            while tokens[i] != ']':
                out.append(value())
                if tokens[i] != ',':
                    break
                i += 1
            assert tokens[i] == ']'
            i += 1
            return out
        if t.startswith('"'):
            return json.loads(t)
        if t in ('true', 'false'):
            return t == 'true'
        assert re.fullmatch(r'-?\d+(?:\.\d+)?[bBsSlLfFdD]?', t), t
        return float(t.rstrip('bBsSlLfFdD'))

    result = value()
    assert i == len(tokens), text
    return result


def main():
    files = list(FUN.rglob('*.mcfunction'))
    ids = {'prototype:' + p.relative_to(FUN).with_suffix('').as_posix() for p in files}
    json_files = list(PACK.rglob('*.json')) + [PACK / 'pack.mcmeta']
    json_files += list((ROOT / 'assets/prototype').rglob('*.json'))
    json_files += [ROOT / f'assets/minecraft/blockstates/{b}.json' for b in ('calcite', 'smooth_basalt', 'waxed_oxidized_cut_copper')]
    for p in json_files:
        json.loads(p.read_text(encoding='utf-8'))
    for p in (PACK / 'data/minecraft/tags/function').glob('*.json'):
        assert set(json.loads(p.read_text())['values']) <= ids
    largest, summons = 0, 0
    allowed = {'function', 'fill', 'setblock', 'summon', 'execute', 'scoreboard',
               'data', 'tag', 'tp', 'tellraw', 'kill', 'forceload'}
    bounds = ((-16, 31), (-1, 20), (-16, 63))
    for p in files:
        for number, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
            if not line or line.startswith('#'):
                continue
            try:
                balanced(line)
                assert line.split()[0] in allowed
                for ref in re.findall(r'(?:^|run )function (prototype:[a-z0-9_/]+)', line):
                    assert ref in ids, ref
                command = line.rsplit(' run ', 1)[-1]
                parts = command.split()
                if parts[0] in ('fill', 'setblock', 'summon'):
                    count = 6 if parts[0] == 'fill' else 3
                    start = 2 if parts[0] == 'summon' else 1
                    coords = parts[start:start+count]
                    assert all(re.fullmatch(r'~(?:-?\d+(?:\.\d+)?)?', c) for c in coords), coords
                    values = [float(c[1:] or 0) for c in coords]
                    assert all(bounds[i % 3][0] <= v <= bounds[i % 3][1] for i, v in enumerate(values))
                    if parts[0] == 'fill':
                        volume = math.prod(abs(values[i+3]-values[i])+1 for i in range(3))
                        largest = max(largest, volume)
                        assert volume <= 32768, volume
                    if parts[0] != 'summon':
                        block = parts[start+count].split(':')[1]
                        assert (ROOT / f'assets/minecraft/blockstates/{block}.json').exists(), block
                    else:
                        nbt = snbt(command[command.index('{'):])
                        assert 'prototype.entity' in nbt['Tags']
                        assert f'prototype.{p.parent.name}' in nbt['Tags']
                        if parts[1] == 'minecraft:block_display':
                            block = nbt['block_state']['Name'].split(':')[1]
                            if 'prototype.mask' in nbt['Tags']:
                                assert block == 'waxed_oxidized_cut_copper', 'Mask body must use alpha-1 sprite'
                            else:
                                assert block != 'waxed_oxidized_cut_copper', 'Mask body used for visible decoration'
                            assert (ROOT / f'assets/minecraft/blockstates/{block}.json').exists(), block
                            transform = nbt['transformation']
                            assert len(transform['scale']) == 3
                            assert all(v > 0 for v in transform['scale'])
                            for field in ('left_rotation', 'right_rotation'):
                                assert len(transform[field]) == 4
                                assert abs(sum(v*v for v in transform[field])-1) < .001
                        summons += 1
                elif parts[0] == 'tellraw':
                    json.loads(command[command.index('{'):])
            except Exception as exc:
                raise AssertionError(f'{p.relative_to(ROOT)}:{number}: {line}') from exc
    for source, alias in [('smooth_stone', 'mask_stone'), ('oak_planks', 'mask_oak')]:
        before = list(Image.open(ROOT / f'assets/minecraft/textures/block/{source}.png').convert('RGBA').get_flattened_data())
        after = list(Image.open(ROOT / f'assets/prototype/textures/block/{alias}.png').convert('RGBA').get_flattened_data())
        assert len(before) == len(after)
        assert all(p[3] == 255 for p in before)
        changes = [(a, b) for a, b in zip(before, after) if a != b]
        assert len(changes) == 1 and changes[0][0][:3] == changes[0][1][:3]
        assert changes[0][1][3] == 254
        model = json.loads((ROOT / f'assets/prototype/models/block/{alias}.json').read_text())
        assert model['textures']['all'] == f'prototype:block/{alias}'
        assert model['parent'] == 'minecraft:block/cube_all'
    with Image.open(ROOT / 'assets/prototype/textures/block/mask_body.png') as image:
        body = image.convert('RGBA')
        assert set(body.getchannel('A').get_flattened_data()) == {1}
        with Image.open(ROOT / 'assets/minecraft/textures/block/smooth_stone.png') as source:
            assert body.size == source.size
            assert body.convert('RGB').tobytes() == source.convert('RGB').tobytes()
    body_state = json.loads((ROOT / 'assets/minecraft/blockstates/waxed_oxidized_cut_copper.json').read_text())
    assert body_state['variants']['']['model'] == 'prototype:block/mask_body'
    body_model = json.loads((ROOT / 'assets/prototype/models/block/mask_body.json').read_text())
    assert body_model['textures']['all'] == 'prototype:block/mask_body'
    assert body_model['parent'] == 'minecraft:block/cube_all'
    sites = json.loads((PACK / 'sites.json').read_text())
    occupied = set()
    for name, site in sites.items():
        x, y, z = site['origin']
        chunks = {(cx, cz) for cx in range((x-16)//16, (x+31)//16+1)
                  for cz in range((z-16)//16, (z+63)//16+1)}
        assert not occupied & chunks
        occupied |= chunks
        assert (FUN / f'{name}/setup.mcfunction').exists()
    assert len(occupied) <= 256
    assert (ROOT / 'assets/minecraft/textures/block/dirt.png').read_bytes()
    print(f'PASS: {len(files)} functions, {len(json_files)} JSON/mcmeta, {summons} tagged entities, '
          f'max fill {int(largest)}, {len(occupied)} nonoverlapping chunks, 2 alpha-254 targets + alpha-1 mask body verified.')
    print('Scope: references, generated command forms, SNBT, coordinates and assets. No game execution/render validation.')


if __name__ == '__main__':
    main()
