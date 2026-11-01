"""SearchArea authoring and player-local mode toggle, layered on common editor APIs."""
R = 'storage space_editor:runtime'
D = 'storage space_editor:document'


def generate(g):
    sizes = g.SIZES
    regular = sizes['normal']
    search = sizes['searchArea']
    gap = g.stage4.stage3.stage2.stage1.BLOCK_CONFIG['modeSwitchGapTicks']
    cooldown = g.INPUT_CD
    def item(tool):
        return f'minecraft:carrot_on_a_stick[minecraft:custom_data~{{space_editor:{{tool:"{tool}"}}}}]'
    for tool, name, color, lore in (
        ('search_area', '検索エリア棒', 'blue', f'右クリック2回: A/Bで検索エリア作成（各辺最大{search}）'),
        ('mode_toggle', 'モード切替棒', 'light_purple', '右クリック: 編集 / プレイ切替（長押し防止あり）'),
    ):
        g.append(g.F / 'start.mcfunction', [f'execute unless items entity @s container.* {item(tool)} run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={{space_editor:{{tool:"{tool}"}}}},minecraft:item_model="editor:tool_{tool}",minecraft:custom_name={{text:"{name}",color:"{color}",italic:false}},minecraft:lore=[{{text:"{lore}",italic:false}}]]'])
    g.append(g.F / 'load.mcfunction', ['scoreboard objectives add se.mode_gap dummy'])
    # Use an idle-gap debounce, refreshed on EVERY use event, including rejected
    # ones. Held right click cannot retrigger every time the usual cooldown ends.
    g.insert_before(g.F / 'tick.mcfunction', 'scoreboard players set #selection_cursor_active', [
        'scoreboard players add @a se.mode_gap 0',
        'scoreboard players remove @a[scores={se.mode_gap=1..}] se.mode_gap 1',
        f'execute as @a[scores={{se.use=1..}}] at @s if items entity @s weapon.mainhand {item("mode_toggle")} run function space_editor:input/mode_toggle',
    ])
    g.fn('input/mode_toggle', [
        'scoreboard players set @s se.use 0',
        f'execute if score @s se.mode_gap matches 1.. run return run scoreboard players set @s se.mode_gap {gap}',
        f'scoreboard players set @s se.mode_gap {gap}', f'scoreboard players set @s se.cd {cooldown}',
        'execute if entity @s[tag=space_editor.editing] run return run function space_editor:play',
        'function space_editor:start',
    ])
    g.insert_before(g.F / 'tick.mcfunction', 'scoreboard players set @a[scores={se.use=1..}]', [
        f'execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand {item("search_area")} run function space_editor:selection/track',
        f'execute as @a[tag=space_editor.editing,scores={{se.use=1..,se.cd=0}}] at @s if items entity @s weapon.mainhand {item("search_area")} run function space_editor:input/search_area',
    ])
    regular_input = (g.F / 'input/region.mcfunction').read_text(encoding='utf-8')
    g.write(g.F / 'input/search_area.mcfunction', f'execute unless data {R} selection{{kind:"search_area"}} run data remove {R} selection\ndata modify {R} selectionKind set value "search_area"\n' + regular_input)
    g.write(g.F / 'input/region.mcfunction', f'execute if data {R} selection{{kind:"search_area"}} run data remove {R} selection\ndata modify {R} selectionKind set value "generic"\n' + regular_input)
    g.insert_before(g.F / 'selection/set_a.mcfunction', 'data modify storage space_editor:runtime selection.dimension', [f'data modify {R} selection.kind set from {R} selectionKind'])
    path = g.F / 'region/create.mcfunction'
    text = path.read_text(encoding='utf-8')
    text = f'scoreboard players set #region_max se.v {regular}\n' + f'execute if data {R} selection{{kind:"search_area"}} run scoreboard players set #region_max se.v {search}\n' + text
    for a in 'xyz':
        text = text.replace(f'unless score #size{a} se.v matches 1..{regular}', f'if score #size{a} se.v > #region_max se.v')
    text = text.replace(f'各辺は1〜{regular}ブロックにしてください。', f'各辺は通常1〜{regular}、検索エリア1〜{search}ブロックにしてください。')
    text = text.replace(f'data modify {D} regions append', f'execute if data {R} selection{{kind:"search_area"}} run data modify {R} region.kind set value "search_area"\ndata modify {D} regions append')
    g.write(path, text)
    for name in ('region/resize_all', 'region/resize_face'):
        path = g.F / (name + '.mcfunction')
        text = path.read_text(encoding='utf-8')
        text = f'scoreboard players set #region_max se.v {regular * 1000}\n' + ''.join(f'execute if data {R} hit{{kind:"{kind}"}} run scoreboard players set #region_max se.v {sizes[key] * 1000}\n' for kind, key in (('space_link', 'spaceLink'), ('proxy_existence', 'proxyExistence'), ('search_area', 'searchArea'))) + text
        lines = []
        for line in text.splitlines():
            if f'matches 100..{regular * 1000}' in line:
                lines += [line.replace(f'matches 100..{regular * 1000}', 'matches 100..'), line.replace('unless score', 'if score').replace(f'matches 100..{regular * 1000}', '> #region_max se.v').replace(f'0.1〜{regular}ブロック', f'通常0.1〜{regular}、SpaceLink0.1〜{sizes["spaceLink"]}、Proxy存在範囲0.1〜{sizes["proxyExistence"]}、検索エリア0.1〜{search}ブロック')]
            else:
                lines.append(line)
        g.write(path, '\n'.join(lines) + '\n')
    g.append(g.F / 'preview/spawn.mcfunction', [f'execute if data {R} renderRegion{{kind:"search_area"}} run function space_editor:search/preview with {R} renderRegion'])
    g.fn('search/preview', ['$execute in $(dimension) positioned $(cx) $(cy) $(cz) run summon minecraft:text_display ~ ~0.75 ~ {Tags:["space_editor.preview","space_editor.label"],text:{text:"SearchArea #$(id) / 検索最適化",color:"blue"},billboard:"center",see_through:1b}'])
