"""Generate the small, inspectable mcfunction pack. Does not operate a world.

Edit SITES for origins; edit build_site for geometry. Runtime setup waits for
every reserved chunk before building. All world coordinates derive from origins.
"""
from pathlib import Path
import json
import shutil
import os
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'datapacks/spatial_prototype'
FUN = PACK / 'data/prototype/function'
SITES = {'hub': (0, 64, 0), **{f'p{i:02}': (i * 128, 64, 0) for i in range(1, 6)}}
MASK_BLOCK = 'waxed_oxidized_cut_copper'
TITLES = {'p01': '01 Directional wall', 'p02': '02 Bigger inside',
          'p03': '03 Two viewpoints', 'p04': '04 Upside-down room',
          'p05': '05 Culling corridor', 'hub': 'Spatial prototypes / hub'}


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8', newline='\n')


def js(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def fn(name, lines):
    write(FUN / (name + '.mcfunction'), '\n'.join(lines) + '\n')


def pos(p):
    return ' '.join('~' + (str(v) if v else '') for v in p)


def fill(a, b, block):
    return f'fill {pos(a)} {pos(b)} minecraft:{block}'


def block(p, name):
    return f'setblock {pos(p)} minecraft:{name}'


def display(site, p, name, scale=(1, 1, 1), mask=False, inverted=False):
    # Targets remain visually opaque; only the masking volume is nearly invisible.
    if mask:
        name = MASK_BLOCK
    # Positive scale + proper 180-degree rotation preserves face winding.
    rotation = '[0f,0f,1f,0f]' if inverted else '[0f,0f,0f,1f]'
    tags = ['prototype.entity', f'prototype.{site}', 'prototype.mask' if mask else 'prototype.decor']
    nbt = ('{Tags:' + json.dumps(tags) + ',block_state:{Name:"minecraft:' + name + '"},'
           'brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,'
           'transformation:{translation:[0f,0f,0f],left_rotation:' + rotation + ',scale:[' +
           ','.join(str(v) + 'f' for v in scale) + '],right_rotation:[0f,0f,0f,1f]}}')
    return f'summon minecraft:block_display {pos(p)} {nbt}'


def label(site, p, text):
    return ('summon minecraft:text_display ' + pos(p) + ' {Tags:["prototype.entity","prototype.' + site +
            '"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:' +
            json.dumps(text, ensure_ascii=False) + '}')


def room(x0, z0, x1, z1, height=6, wall='stone_bricks'):
    return [fill((x0, 0, z0), (x1, height, z1), wall),
            fill((x0+1, 1, z0+1), (x1-1, height-1, z1-1), 'air'),
            fill((x0+1, 0, z0+1), (x1-1, 0, z1-1), 'smooth_quartz'),
            fill((x0+1, height, z0+1), (x1-1, height, z1-1), 'sea_lantern')]


def build_site(s):
    lines = [fill((-12, 0, -12), (27, 0, 59), 'smooth_stone'),
             fill((-12, 0, -12), (27, 0, -12), 'sea_lantern'),
             label(s, (5, 4, -9), TITLES[s]),
             label(s, (5, 2, -10), '/function prototype:goto/hub'),
             'summon minecraft:marker ~ ~1 ~ {Tags:["prototype.entity","prototype.' + s + '","prototype.origin"]}']
    if s == 'hub':
        lines += [label(s, (5, 3, 0), '/function prototype:goto/01 ... 05'),
                  label(s, (5, 2, 2), 'boot: rebuild all / reset: remove experiments'),
                  label(s, (5, 2, 4), 'Targets: smooth_basalt = smooth stone / calcite = oak')]
        for i in range(1, 6):
            lines += [fill((i*4-10, 0, 8), (i*4-8, 0, 10), 'gold_block'),
                      label(s, (i*4-9, 2, 9), f'{i:02} / stand on gold')]
        return lines
    if s == 'p01':
        lines += room(-5, 8, 15, 22)
        lines += [fill((-4, 1, 8), (14, 5, 8), 'smooth_basalt'),
                  display(s, (2, 1, 7.7), 'smooth_basalt', (5, 4, .12), True),
                  fill((-1, 1, 14), (1, 3, 17), 'red_concrete'),
                  fill((8, 1, 17), (10, 4, 19), 'blue_concrete'),
                  fill((4, 0, 0), (5, 0, 4), 'gold_block'),
                  label(s, (5, 2, -3), 'Front gold line: compare center / side / back'),
                  label(s, (5, 7, 8), 'Placed wall + thin display in FRONT of wall')]
    elif s == 'p02':
        # A small shell surrounds a wider preview hall. The target shell is
        # masked; ordinary solid hall geometry supplies the visible background.
        lines += room(-5, 8, 15, 25, 7)
        lines += room(2, 2, 8, 8, 5, 'calcite')
        lines += [fill((4, 1, 2), (6, 3, 2), 'air'),
                  display(s, (3, 1, 6.7), 'calcite', (5, 4, .15), True),
                  fill((4, 0, 3), (6, 0, 7), 'gold_block'),
                  fill((4, 1, 8), (6, 3, 8), 'air')]
        # Same hall silhouette and decorations at +32 Z for traversable interior.
        lines += room(-5, 40, 15, 57, 7)
        lines += [fill((4, 1, 40), (6, 3, 40), 'air')]
        for dz in (0, 32):
            for x in (-2, 12):
                lines += [fill((x, 1, 12+dz), (x, 5, 12+dz), 'quartz_pillar'),
                          fill((x, 1, 21+dz), (x, 5, 21+dz), 'quartz_pillar')]
            lines += [fill((3, 1, 23+dz), (7, 2, 23+dz), 'emerald_block')]
        lines += [label(s, (5, 3, -3), 'Small shell -> gold threshold -> full-size hall'),
                  label(s, (5, 3, 45), 'Return through front door / preserves position and look')]
    elif s == 'p03':
        lines += room(-8, 7, 18, 23)
        lines += [fill((-7, 1, 7), (17, 5, 7), 'smooth_basalt'),
                  fill((5, 1, 8), (5, 5, 22), 'stone_bricks'),
                  fill((-7, 1, 22), (4, 5, 22), 'red_concrete'),
                  fill((6, 1, 22), (17, 5, 22), 'blue_concrete'),
                  fill((-4, 1, 14), (-2, 3, 16), 'gold_block'),
                  fill((11, 1, 14), (13, 4, 16), 'diamond_block'),
                  display(s, (-3, 1, 6.75), 'smooth_basalt', (3, 4, .12), True),
                  display(s, (10, 1, 6.75), 'smooth_basalt', (3, 4, .12), True),
                  fill((-2, 0, 1), (-1, 0, 3), 'red_concrete'),
                  fill((11, 0, 1), (12, 0, 3), 'blue_concrete'),
                  label(s, (5, 3, -3), 'Move left/right: red room / blue room'),
                  label(s, (5, 7, 7), 'Static paired apertures + solid divider; no view swapping')]
    elif s == 'p04':
        lines += room(-4, 7, 14, 24, 9)
        lines += [fill((-3, 1, 7), (13, 7, 7), 'calcite'),
                  display(s, (0, 1, 6.75), 'calcite', (10, 6, .12), True),
                  display(s, (11, 7, 12), 'oak_planks', (12, .4, 9), inverted=True),
                  display(s, (3, 6.6, 14), 'oak_planks', (3, .5, 3), inverted=True)]
        for x in (1, 3):
            for z in (14, 16):
                lines += [display(s, (x, 6.1, z), 'oak_log', (.35, 1.7, .35), inverted=True)]
        lines += [display(s, (10, 6.6, 18), 'red_concrete', (3, 1, 2), inverted=True),
                  display(s, (10, 5.6, 18), 'white_concrete', (1, .4, 2), inverted=True),
                  fill((4, 0, 0), (6, 0, 3), 'gold_block'),
                  label(s, (5, 3, -3), 'Upside-down furniture beyond masked wall'),
                  label(s, (5, 11, 12), 'Visual diorama only / ordinary gravity')]
    else:
        for x, kind in [(-8, 'touching'), (2, 'gap'), (12, 'display')]:
            if kind == 'touching':
                lines += [fill((x, 1, 8), (x+3, 4, 11), 'smooth_basalt')]
            elif kind == 'gap':
                for z in (8, 10):
                    lines += [fill((x, 1, z), (x+3, 4, z), 'smooth_basalt')]
            else:
                # Adjacent displays retain their model faces; no block-neighbor culling.
                for dx in range(4):
                    for dy in range(4):
                        for dz in range(4):
                            lines += [display(s, (x+dx, 1+dy, 8+dz), 'smooth_basalt')]
            lines += [display(s, (x+.25, 1, 7.7), 'smooth_basalt', (3.5, 4, .12), True),
                      fill((x, 1, 15), (x+3, 4, 15), 'lime_concrete'),
                      label(s, (x+1.5, 6, 9), kind)]
        lines += [label(s, (5, 3, -3), 'Compare depth / internal faces from front and sides'),
                  fill((-8, 1, 24), (-5, 4, 24), 'smooth_stone'),
                  fill((2, 1, 24), (5, 4, 24), 'smooth_basalt'),
                  display(s, (-7.75, 1, 23.7), 'smooth_basalt', (3.5, 4, .12), True),
                  display(s, (2.25, 1, 23.7), 'smooth_basalt', (3.5, 4, .12), True),
                  label(s, (-6.5, 6, 24), 'Solid smooth-stone control'),
                  label(s, (3.5, 6, 24), 'Same RGB / translucent target')]
    return lines


def write_mask_texture():
    """Create the explicitly requested alpha-1 body, verifying before replace.

    The existing one-pixel marker is for targets and must not be changed to
    perform this different operation. Keep RGB identical to the source here.
    """
    target = ROOT / 'assets/prototype/textures/block/mask_body.png'
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(ROOT / 'assets/minecraft/textures/block/smooth_stone.png') as source:
        before = source.convert('RGBA')
    after = before.copy()
    after.putalpha(1)
    with tempfile.NamedTemporaryFile(dir=target.parent, suffix='.png', delete=False) as handle:
        temp = Path(handle.name)
    try:
        after.save(temp, format='PNG')
        with Image.open(temp) as saved:
            check = saved.convert('RGBA')
            assert check.size == before.size
            assert all(a[:3] == b[:3] and b[3] == 1 for a, b in
                       zip(before.get_flattened_data(), check.get_flattened_data()))
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)


def main():
    js(PACK / 'pack.mcmeta', {'pack': {'description': 'Spatial mask prototypes | Java 26.1',
                                      'min_format': [101, 1], 'max_format': [101, 1]}})
    js(PACK / 'data/prototype/dimension/lab.json', {'type': 'minecraft:overworld', 'generator': {
        'type': 'minecraft:flat', 'settings': {'biome': 'minecraft:the_void', 'features': False,
        'lakes': False, 'layers': [{'block': 'minecraft:air', 'height': 1}], 'structure_overrides': []}}})
    js(PACK / 'data/minecraft/tags/function/load.json', {'values': ['prototype:load']})
    js(PACK / 'data/minecraft/tags/function/tick.json', {'values': ['prototype:tick']})
    js(PACK / 'sites.json', {s: {'origin': xyz, 'bounds_relative': [[-16, -1, -16], [31, 20, 63]]}
                            for s, xyz in SITES.items()})
    fn('init', ['scoreboard objectives add proto.state dummy', 'scoreboard objectives add proto.cd dummy',
                'data modify storage prototype:state initialized set value 1b'])
    fn('load', ['execute unless data storage prototype:state initialized run function prototype:init'])
    boot = ['function prototype:load', 'scoreboard players set #boot proto.state 1']
    tick = ['scoreboard players remove @a[scores={proto.cd=1..}] proto.cd 1']
    reset = ['function prototype:load', 'scoreboard players set #boot proto.state 0',
             'function prototype:hub/setup',
             'execute in prototype:lab as @a[distance=0..] run tag @s add prototype.to_hub']
    for s, (x, y, z) in SITES.items():
        anchor = f'execute in prototype:lab positioned {x} {y} {z}'
        boot.append(f'function prototype:{s}/setup')
        fn(f'{s}/setup', ['function prototype:load',
                         f'{anchor} run forceload add ~-16 ~-16 ~31 ~63',
                         f'scoreboard players set #{s}.built proto.state 0',
                         f'scoreboard players set #{s} proto.state 1'])
        # Checking every chunk avoids builds partially succeeding at cold starts.
        loaded = ' '.join(f'if loaded {pos((cx, 0, cz))}' for cx in (-16, 0, 16) for cz in (-16, 0, 16, 32, 48))
        tick += [f'{anchor} if score #{s} proto.state matches 1 {loaded} run function prototype:{s}/build']
        clear = [f'kill @e[tag=prototype.{s}]']
        # 48*22*16 = 16896 blocks per fill: below the default limit.
        clear += [fill((-16, -1, cz), (31, 20, cz+15), 'air') for cz in (-16, 0, 16, 32, 48)]
        fn(f'{s}/clear', clear)
        fn(f'{s}/build', [f'function prototype:{s}/clear'] + build_site(s) + [
            f'scoreboard players set #{s} proto.state 0', f'scoreboard players set #{s}.built proto.state 1',
            f'tellraw @a {{"text":"[prototype] {s} ready","color":"green"}}'])
        goto = 'hub' if s == 'hub' else s[1:]
        fn(f'goto/{goto}', [f'execute unless score #{s}.built proto.state matches 1 run tellraw @s {{"text":"Run /function prototype:{s}/setup and wait for ready.","color":"yellow"}}',
                            f'execute if score #{s}.built proto.state matches 1 run scoreboard players set @s proto.cd 20',
                            f'execute if score #{s}.built proto.state matches 1 in prototype:lab run tp @s {x+5.5} {y+1} {z-6.5} 0 0'])
        if s != 'hub':
            reset += [f'{anchor} run forceload add ~-16 ~-16 ~31 ~63',
                      f'scoreboard players set #{s}.built proto.state 0',
                      f'scoreboard players set #{s} proto.state -1']
            tick += [f'{anchor} if score #{s} proto.state matches -1 {loaded} if score #hub.built proto.state matches 1 run function prototype:{s}/remove']
            fn(f'{s}/remove', [f'function prototype:{s}/clear', 'forceload remove ~-16 ~-16 ~31 ~63',
                               f'scoreboard players set #{s} proto.state 0'])
    # The hub remains as a safe landing place during reset; no player is sent into void.
    tick += ['execute if score #hub.built proto.state matches 1 as @a[tag=prototype.to_hub] run function prototype:goto/hub',
             'execute if score #hub.built proto.state matches 1 run tag @a[tag=prototype.to_hub] remove prototype.to_hub']
    all_ready = ' '.join(f'if score #{s}.built proto.state matches 1' for s in SITES)
    tick += [f'execute if score #boot proto.state matches 1 {all_ready} run function prototype:ready',
             'execute in prototype:lab as @a[distance=0..] run scoreboard players add @s proto.cd 0',
             'execute in prototype:lab if score #p02.built proto.state matches 1 run function prototype:p02/tick',
             'execute in prototype:lab if score #hub.built proto.state matches 1 run function prototype:hub/tick']
    boot += ['execute in prototype:lab as @a[distance=0..] run tag @s add prototype.to_hub',
             'tellraw @s {"text":"[prototype] Building in prototype:lab. Wait for ALL READY, then /function prototype:goto/hub","color":"yellow"}']
    fn('boot', boot)
    fn('reset', reset + ['tellraw @s {"text":"[prototype] Removing experiments after chunks load. Safety hub is retained.","color":"yellow"}'])
    fn('ready', ['scoreboard players set #boot proto.state 0', 'tellraw @a {"text":"[prototype] ALL READY: /function prototype:goto/hub","color":"green"}'])
    fn('tick', tick)
    # Teleports run at each player, so fractional position and look are retained.
    # An arrival beyond the destination trigger plus cooldown prevents ping-pong.
    x, y, z = SITES['p02']
    fn('p02/tick', [
        f'execute as @a[x={x+4},y={y+1},z={z+6},dx=2,dy=2,dz=1,scores={{proto.cd=0}}] at @s run function prototype:p02/enter',
        f'execute as @a[x={x+4},y={y+1},z={z+39},dx=2,dy=2,dz=1,scores={{proto.cd=0}}] at @s run function prototype:p02/leave'])
    fn('p02/enter', ['scoreboard players set @s proto.cd 20', 'tp @s ~ ~ ~35'])
    fn('p02/leave', ['scoreboard players set @s proto.cd 20', 'tp @s ~ ~ ~-36'])
    x, y, z = SITES['hub']
    fn('hub/tick', [f'execute as @a[x={x+i*4-10},y={y+1},z={z+8},dx=2,dy=1,dz=2,scores={{proto.cd=0}}] run function prototype:goto/{i:02}' for i in range(1, 6)])
    for source, alias, block_id in [('smooth_stone', 'mask_stone', 'smooth_basalt'), ('oak_planks', 'mask_oak', 'calcite')]:
        target = ROOT / f'assets/prototype/textures/block/{alias}.png'
        target.parent.mkdir(parents=True, exist_ok=True)
        # Copy only on first generation: alpha marking is a separate verified step.
        if not target.exists():
            shutil.copyfile(ROOT / f'assets/minecraft/textures/block/{source}.png', target)
        js(ROOT / f'assets/prototype/models/block/{alias}.json', {
            'parent': 'minecraft:block/cube_all', 'textures': {'all': f'prototype:block/{alias}'}})
        js(ROOT / f'assets/minecraft/blockstates/{block_id}.json', {
            'variants': {'': {'model': f'prototype:block/{alias}'}}})
    write_mask_texture()
    js(ROOT / 'assets/prototype/models/block/mask_body.json', {
        'parent': 'minecraft:block/cube_all', 'textures': {'all': 'prototype:block/mask_body'}})
    js(ROOT / f'assets/minecraft/blockstates/{MASK_BLOCK}.json', {
        'variants': {'': {'model': 'prototype:block/mask_body'}}})
    print(f'Generated {len(list(FUN.rglob("*.mcfunction")))} functions in {PACK}')


if __name__ == '__main__':
    main()
