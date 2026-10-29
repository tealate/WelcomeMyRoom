"""Stage 05 SpaceLink groups. Called after the existing 05 -> 04 -> 03 chain.

All transactions stage complete Region records before publishing any change.
Old pair rows remain as compatibility/Action references, never as membership.
Bounded, shallow queue dispatch avoids recursive depth proportional to members.
"""


def generate(s):
    global fn, F, R, D, write, message
    fn, F, R, D, write, message = s.fn, s.F, s.R, s.D, s.write, s.message
    persistence()
    editing()
    runtime()
    ui(s)


def prepend(name, lines):
    p = F / (name + '.mcfunction')
    write(p, '\n'.join(lines) + '\n' + p.read_text(encoding='utf-8'))


def replace(name, old, new):
    p = F / (name + '.mcfunction')
    content = p.read_text(encoding='utf-8')
    if old not in content:
        raise ValueError(f'Missing integration point: {name}: {old}')
    write(p, content.replace(old, new))


def drain(name, queue, step, capacity=4096):
    # 16 x 16 x 16 bounded dispatch, at most three stack levels. The operational
    # command budget is configurable by the server, not an artificial 64-member cap.
    fn(name + '_16', [f'execute unless data {R} {queue}[0] run return 0'] +
       [f'execute if data {R} {queue}[0] run function space_editor:{step}'] * 16)
    fn(name + '_256', [f'execute unless data {R} {queue}[0] run return 0'] +
       [f'execute if data {R} {queue}[0] run function space_editor:{name}_16'] * 16)
    unit, count = ('16', 4) if capacity == 64 else ('256', 16)
    fn(name, [f'execute if data {R} {queue}[0] run function space_editor:{name}_{unit}'] * count)


def persistence():
    # Run before the older pair/Room consistency check, without resetting Document.
    prepend('link/validate_groups', ['function space_editor:space_group/migrate'])
    fn('space_group/migrate', [
        f'execute unless data {D} spaceLinkGroups run data modify {D} spaceLinkGroups set value []',
        f'execute unless data {D} nextSpaceLinkGroupId run data modify {D} nextSpaceLinkGroupId set value 1',
        f'data modify {R} spaceLinkWarnings set value []',
        f'data modify {R} sgMigrateQueue set from {D} regionPairs',
        'function space_editor:space_group/migrate_scan',
        f'execute if data {R} sgMigrateQueue[0] run data modify {R} spaceLinkWarnings append value {{reason:"migration_scan_limit_4096"}}',
        f'execute if data {R} spaceLinkWarnings[0] run ' + message('SpaceLink移行警告: /data get storage space_editor:runtime spaceLinkWarnings', 'yellow', target='@a'),
    ])
    drain('space_group/migrate_scan', 'sgMigrateQueue', 'space_group/migrate_next', 4096)
    fn('space_group/migrate_next', [
        f'data modify {R} sgLegacy set from {R} sgMigrateQueue[0]',
        f'execute if data {R} sgLegacy{{kind:"space_link"}} unless data {R} sgLegacy.spaceLinkGroupId run function space_editor:space_group/migrate_pair with {R} sgLegacy',
        f'data remove {R} sgMigrateQueue[0]',
    ])
    fn('space_group/migration_warning', [
        f'data modify {R} sgWarning set value {{reason:"invalid_or_conflicting_legacy_pair_unchanged"}}',
        f'data modify {R} sgWarning.pairId set from {R} sgLegacy.id',
        f'data modify {R} spaceLinkWarnings append from {R} sgWarning',
    ])
    fn('space_group/migrate_pair', [
        f'data modify {R} sg set value {{group:{{members:[]}},before:{{}},after:[]}}',
        'scoreboard players set #sg_unique se.v 1',
        *[line for key, path in (('pair', 'regionPairs[{id:$(id)}]'), ('a', 'regions[{id:$(a)}]'), ('b', 'regions[{id:$(b)}]'))
          for line in (f'data modify {R} sgUnique set value []',
                       f'$data modify {R} sgUnique append from {D} {path}',
                       f'execute store result score #sg_n se.v run data get {R} sgUnique',
                       'execute unless score #sg_n se.v matches 1 run scoreboard players set #sg_unique se.v 0')],
        'execute unless score #sg_unique se.v matches 1 run return run function space_editor:space_group/migration_warning',
        f'data remove {R} sgA', f'data remove {R} sgB',
        f'$data modify {R} sgA set from {D} regions[{{id:$(a),kind:"space_link",pairId:$(id),partnerId:$(b)}}]',
        f'$data modify {R} sgB set from {D} regions[{{id:$(b),kind:"space_link",pairId:$(id),partnerId:$(a)}}]',
        f'execute unless data {R} sgA.id run return run function space_editor:space_group/migration_warning',
        f'execute unless data {R} sgB.id run return run function space_editor:space_group/migration_warning',
        f'execute if data {R} sgA.spaceLinkGroupId run return run function space_editor:space_group/migration_warning',
        f'execute if data {R} sgB.spaceLinkGroupId run return run function space_editor:space_group/migration_warning',
        f'$execute if data {R} sgA{{id:$(b)}} run return run function space_editor:space_group/migration_warning',
        f'data modify {R} frame set from {R} sgA', 'function space_editor:pair/frame',
        'execute unless score #frame_ok se.v matches 1 run return run function space_editor:space_group/migration_warning',
        f'data modify {R} sg.group.localSize set from {R} frame.localSize',
        'scoreboard players set #sg_ok se.v 1',
        'function space_editor:space_group/validate_frame',
        f'data modify {R} frame set from {R} sgB',
        'function space_editor:space_group/validate_frame',
        'execute unless score #sg_ok se.v matches 1 run return run function space_editor:space_group/migration_warning',
        f'data modify {R} sg.before.legacyPair set from {R} sgLegacy',
        f'data modify {R} sg.before.regions set value []',
        *[f'data modify {R} sg.before.regions append from {R} sg{x}' for x in ('A', 'B')],
        'function space_editor:space_group/allocate',
        'execute unless score #sg_ok se.v matches 1 run return run function space_editor:space_group/migration_warning',
        f'$data modify {R} sg.group.members set value [$(a),$(b)]',
        f'data modify {R} sg.after set from {R} sg.before.regions',
        f'data modify {R} sg.operation set value "migrate"',
        'function space_editor:space_group/identify_all',
        'function space_editor:space_group/store',
        f'$data modify {D} regionPairs[{{id:$(id)}}].spaceLinkGroupId set from {R} sg.group.id',
        'function space_editor:space_group/action',
    ])
    # Max(existing IDs, next ID) + 1, so imported mixed documents cannot collide.
    fn('space_group/allocate', [
        f'execute store result score #sg_id se.v run data get {D} nextSpaceLinkGroupId 1',
        'execute unless score #sg_id se.v matches 1..2147483646 run scoreboard players set #sg_id se.v 1',
        f'data modify {R} sgIds set from {D} spaceLinkGroups',
        'function space_editor:space_group/id_scan',
        f'execute if data {R} sgIds[0] run scoreboard players set #sg_ok se.v 0',
        'execute unless score #sg_id se.v matches 1..2147483646 run scoreboard players set #sg_ok se.v 0',
        f'execute store result {R} sg.group.id int 1 run scoreboard players get #sg_id se.v',
    ])
    drain('space_group/id_scan', 'sgIds', 'space_group/id_next', 4096)
    fn('space_group/id_next', [
        f'execute store result score #sg_existing se.v run data get {R} sgIds[0].id 1',
        'execute if score #sg_existing se.v >= #sg_id se.v run scoreboard players operation #sg_id se.v = #sg_existing se.v',
        'execute if score #sg_existing se.v = #sg_id se.v run scoreboard players add #sg_id se.v 1',
        f'data remove {R} sgIds[0]',
    ])
    fn('space_group/load', [
        f'data modify {R} sg set value {{before:{{regions:[]}},after:[]}}',
        'scoreboard players set #sg_ok se.v 0',
        f'data modify {R} sgUnique set value []',
        f'$data modify {R} sgUnique append from {D} spaceLinkGroups[{{id:$(spaceLinkGroupId)}}]',
        f'execute store result score #sg_n se.v run data get {R} sgUnique',
        'execute unless score #sg_n se.v matches 1 run return 0',
        f'$data modify {R} sg.group set from {D} spaceLinkGroups[{{id:$(spaceLinkGroupId)}}]',
        f'data modify {R} sg.before.group set from {R} sg.group',
        'scoreboard players set #sg_ok se.v 0',
        f'execute unless data {R} sg.group.id run return 0',
        f'execute store result score #sg_count se.v run data get {R} sg.group.members',
        'execute unless score #sg_count se.v matches 2..4096 run return 0',
        'scoreboard players set #sg_ok se.v 1',
        f'data modify {R} sg.queue set from {R} sg.group.members',
        'function space_editor:space_group/load_scan',
    ])
    drain('space_group/load_scan', 'sg.queue', 'space_group/load_next')
    fn('space_group/load_next', [
        f'data modify {R} sgRef.id set from {R} sg.queue[0]',
        f'data modify {R} sgRef.groupId set from {R} sg.group.id',
        f'function space_editor:space_group/load_member with {R} sgRef',
        f'data remove {R} sg.queue[0]',
    ])
    fn('space_group/load_member', [
        f'data modify {R} sgUnique set value []',
        f'$data modify {R} sgUnique append from {D} regions[{{id:$(id)}}]',
        f'execute store result score #sg_n se.v run data get {R} sgUnique',
        'execute unless score #sg_n se.v matches 1 run return run scoreboard players set #sg_ok se.v 0',
        f'data remove {R} frame',
        f'$data modify {R} frame set from {D} regions[{{id:$(id),spaceLinkGroupId:$(groupId),kind:"space_link"}}]',
        f'execute unless data {R} frame.id run return run scoreboard players set #sg_ok se.v 0',
        f'$execute if data {R} sg.before.regions[{{id:$(id)}}] run return run scoreboard players set #sg_ok se.v 0',
        f'data modify {R} sg.before.regions append from {R} frame',
        'function space_editor:space_group/validate_frame',
    ])
    fn('space_group/validate_frame', [
        f'execute unless data {R} frame.x1m run return run scoreboard players set #sg_ok se.v 0',
        *[f'execute unless data {R} frame.{a}{e}m run return run scoreboard players set #sg_ok se.v 0' for a in 'xyz' for e in (1, 2)],
        # Custom dimensions need explicit build heights; fail closed, never assume Nether bounds.
        f'execute unless data {R} frame{{dimension:"minecraft:overworld"}} unless data {R} frame{{dimension:"minecraft:the_nether"}} unless data {R} frame{{dimension:"minecraft:the_end"}} run return run scoreboard players set #sg_ok se.v 0',
        'function space_editor:pair/frame',
        'execute unless score #frame_ok se.v matches 1 run scoreboard players set #sg_ok se.v 0',
        f'execute unless data {R} frame{{rotationY:0}} unless data {R} frame{{rotationY:90}} unless data {R} frame{{rotationY:180}} unless data {R} frame{{rotationY:270}} run scoreboard players set #sg_ok se.v 0',
        f'execute unless data {R} frame{{flipY:0b}} unless data {R} frame{{flipY:1b}} run scoreboard players set #sg_ok se.v 0',
        f'data modify {R} sgSize set from {R} frame.localSize',
        f'execute store success score #sg_diff se.v run data modify {R} sgSize set from {R} sg.group.localSize',
        'execute if score #sg_diff se.v matches 1 run scoreboard players set #sg_ok se.v 0',
    ])
    fn('space_group/identify_all', [
        f'data modify {R} sg.queue set from {R} sg.after', f'data modify {R} sg.after set value []',
        'function space_editor:space_group/identify_scan',
    ])
    drain('space_group/identify_scan', 'sg.queue', 'space_group/identify_next')
    fn('space_group/identify_next', [
        f'data modify {R} frame set from {R} sg.queue[0]',
        'function space_editor:pair/frame',
        f'execute if data {R} frame.pairId run data modify {R} frame.legacyPairId set from {R} frame.pairId',
        *[f'data remove {R} frame.{key}' for key in ('pairId', 'partnerId', 'side')],
        f'data modify {R} frame.kind set value "space_link"',
        f'data modify {R} frame.spaceLinkGroupId set from {R} sg.group.id',
        f'execute unless data {R} frame.roomId run data modify {R} frame.roomId set value ""',
        f'data modify {R} sg.after append from {R} frame', f'data remove {R} sg.queue[0]',
    ])
    fn('space_group/store', [
        f'data modify {R} sg.queue set from {R} sg.after',
        'function space_editor:space_group/store_scan',
        f'function space_editor:space_group/store_group with {R} sg.group',
    ])
    drain('space_group/store_scan', 'sg.queue', 'space_group/store_next')
    fn('space_group/store_next', [
        f'function space_editor:space_group/store_member with {R} sg.queue[0]', f'data remove {R} sg.queue[0]',
    ])
    fn('space_group/store_member', [
        f'$execute unless data {D} regions[{{id:$(id)}}] run data modify {D} regions append from {R} sg.queue[0]',
        f'$data modify {D} regions[{{id:$(id)}}] set from {R} sg.queue[0]',
    ])
    fn('space_group/store_group', [
        f'$execute unless data {D} spaceLinkGroups[{{id:$(id)}}] run data modify {D} spaceLinkGroups append from {R} sg.group',
        f'$data modify {D} spaceLinkGroups[{{id:$(id)}}] set from {R} sg.group',
        f'execute store result score #sg_id se.v run data get {R} sg.group.id 1',
        'scoreboard players add #sg_id se.v 1',
        f'execute store result score #sg_next se.v run data get {D} nextSpaceLinkGroupId 1',
        f'execute if score #sg_id se.v > #sg_next se.v store result {D} nextSpaceLinkGroupId int 1 run scoreboard players get #sg_id se.v',
    ])
    fn('space_group/action', [
        f'data modify {R} sgAction set value {{type:"space_link_group_edit",after:{{}}}}',
        f'data modify {R} sgAction.operation set from {R} sg.operation',
        f'data modify {R} sgAction.before set from {R} sg.before',
        f'data modify {R} sgAction.after.group set from {R} sg.group',
        f'data modify {R} sgAction.after.regions set from {R} sg.after',
        f'execute store result score #sg_action se.v run data get {D} nextActionId 1',
        *[f'execute store result {R} sgAction.{key} int 1 run scoreboard players get #sg_action se.v' for key in ('id', 'order')],
        f'data modify {D} actions append from {R} sgAction',
        'scoreboard players add #sg_action se.v 1',
        f'execute store result {D} nextActionId int 1 run scoreboard players get #sg_action se.v',
    ])


def editing():
    # Public create/append API: pairCandidate is a NEW record, never adopted by ID.
    prepend('pair/create', [
        f'$data modify {R} requestedPairKind set value "$(kind)"',
        f'$execute if data {R} {{requestedPairKind:"space_link"}} run return run function space_editor:space_group/add {{source:$(source)}}',
        f'$execute if data {D} regions[{{id:$(source)}}].spaceLinkGroupId run return 0',
    ])
    fn('space_group/add', [
        'scoreboard players set #pair_ok se.v 0',
        f'data remove {R} sgSource',
        f'$data modify {R} sgSource set from {D} regions[{{id:$(source)}}]',
        f'execute unless data {R} sgSource.id run return 0',
        f'execute if data {R} sgSource.pairId run return run ' + message('旧ペアを先に/reloadで移行してください。', 'red'),
        f'execute if data {R} sgSource.kind unless data {R} sgSource{{kind:"space_link"}} run return 0',
        f'execute if data {R} sgSource.spaceLinkGroupId run function space_editor:space_group/load with {R} sgSource',
        f'execute unless data {R} sgSource.spaceLinkGroupId run function space_editor:space_group/new',
        'execute unless score #sg_ok se.v matches 1 run return run ' + message('グループの参照・サイズ・Dimensionが不正なため変更しません。', 'red'),
        'execute if score #sg_count se.v matches 4096.. run return run ' + message('SpaceLinkの安全走査上限4096 Regionを超えています。', 'red'),
        f'data modify {R} frame set from {R} pairCandidate',
        f'execute if data {R} frame.spaceLinkGroupId run return run ' + message('既存グループのRegionは取り込めません。グループ結合は行いません。', 'red'),
        f'execute if data {R} frame.pairId run return 0',
        'function space_editor:space_group/validate_frame',
        'execute unless score #sg_ok se.v matches 1 run return run ' + message('追加候補のサイズ・位置・姿勢が不正です。', 'red'),
        f'execute store result {R} frame.id int 1 run data get {D} nextId 1',
        f'function space_editor:space_group/new_id with {R} frame',
        'execute unless score #sg_ok se.v matches 1 run return 0',
        f'data modify {R} sg.after set from {R} sg.before.regions',
        f'data modify {R} sg.after append from {R} frame',
        f'data modify {R} sg.group.members append from {R} frame.id',
        f'data modify {R} sg.operation set value "add"',
        'function space_editor:space_group/identify_all',
        'function space_editor:space_group/store',
        'function space_editor:space_group/action',
        f'execute store result score #sg_next se.v run data get {D} nextId 1',
        'scoreboard players add #sg_next se.v 1',
        f'execute store result {D} nextId int 1 run scoreboard players get #sg_next se.v',
        'function space_editor:preview/resync',
        'scoreboard players set #pair_ok se.v 1',
    ])
    fn('space_group/new_id', [
        f'$execute if data {D} regions[{{id:$(id)}}] run scoreboard players set #sg_ok se.v 0',
        f'$data modify {R} frame.idText set value "region_$(id)"',
    ])
    fn('space_group/new', [
        f'data modify {R} sg set value {{group:{{members:[]}},before:{{regions:[]}}}}',
        f'data modify {R} frame set from {R} sgSource',
        'function space_editor:pair/frame',
        f'data modify {R} sg.group.localSize set from {R} frame.localSize',
        'scoreboard players set #sg_ok se.v 1',
        'function space_editor:space_group/validate_frame',
        f'data modify {R} sg.before.regions append from {R} sgSource',
        f'data modify {R} sg.group.members append from {R} sgSource.id',
        'function space_editor:space_group/allocate',
        'scoreboard players set #sg_count se.v 1',
    ])
    # Insert AFTER Stage01 copied edited scores into hit, BEFORE any mutation.
    replace('region/save_resize', f'execute if data {R} hit.pairId',
            f'execute if data {R} hit.spaceLinkGroupId run return run function space_editor:space_group/edit_bounds\nexecute if data {R} hit.pairId')
    fn('space_group/edit_bounds', [
        'scoreboard players set #pair_ok se.v 0',
        f'function space_editor:space_group/load with {R} hit',
        'execute unless score #sg_ok se.v matches 1 run return 0',
        f'function space_editor:space_group/read_old with {R} hit',
        f'data modify {R} frame set from {R} hit', 'function space_editor:pair/frame',
        'execute unless score #frame_ok se.v matches 1 run return 0',
        f'data modify {R} hit set from {R} frame',
        f'data modify {R} sg.group.localSize set from {R} hit.localSize',
        f'data modify {R} sg.operation set from {R} activeTool',
        f'data modify {R} sg.queue set from {R} sg.before.regions',
        'function space_editor:space_group/edit_scan',
        'execute unless score #sg_ok se.v matches 1 run return run ' + message('メンバーの制限によりグループ全体の変更を取り消しました。', 'red'),
        'function space_editor:space_group/commit',
    ])
    fn('space_group/read_old', [f'$data modify {R} old set from {D} regions[{{id:$(id)}}]'])
    drain('space_group/edit_scan', 'sg.queue', 'space_group/edit_next')
    fn('space_group/edit_next', [
        f'data modify {R} partner set from {R} sg.queue[0]',
        f'function space_editor:space_group/edit_member with {R} hit',
        f'data remove {R} sg.queue[0]',
    ])
    fn('space_group/edit_member', [
        f'$execute unless data {R} partner{{id:$(id)}} unless data {R} {{activeTool:"move"}} run function space_editor:pair/sync_bounds',
        f'$execute if data {R} partner{{id:$(id)}} run data modify {R} partner set from {R} hit',
        f'data modify {R} frame set from {R} partner',
        'function space_editor:space_group/validate_frame',
        f'data modify {R} sg.after append from {R} frame',
    ])
    prepend('pair/set_pose', [
        f'$execute if data {D} regions[{{id:$(id)}}].spaceLinkGroupId run return run function space_editor:space_group/set_pose {{id:$(id),rotationY:$(rotationY),flipY:$(flipY)}}',
    ])
    fn('space_group/set_pose', [
        'scoreboard players set #pair_ok se.v 0',
        f'data remove {R} hit', f'$data modify {R} hit set from {D} regions[{{id:$(id)}}]',
        f'function space_editor:space_group/load with {R} hit',
        'execute unless score #sg_ok se.v matches 1 run return 0',
        f'data modify {R} frame set from {R} hit',
        f'$data modify {R} frame.rotationY set value $(rotationY)',
        f'$data modify {R} frame.flipY set value $(flipY)b',
        f'execute unless data {R} frame{{rotationY:0}} unless data {R} frame{{rotationY:90}} unless data {R} frame{{rotationY:180}} unless data {R} frame{{rotationY:270}} run return 0',
        f'execute unless data {R} frame{{flipY:0b}} unless data {R} frame{{flipY:1b}} run return 0',
        'function space_editor:pair/pose_bounds',
        'execute unless score #frame_ok se.v matches 1 run return 0',
        f'data modify {R} sg.after set from {R} sg.before.regions',
        f'$data modify {R} sg.after[{{id:$(id)}}] set from {R} frame',
        f'data modify {R} sg.operation set value "pose"',
        'function space_editor:space_group/commit',
    ])
    fn('space_group/commit', [
        'function space_editor:space_group/store', 'function space_editor:space_group/action',
        f'data modify {R} sgPreviewQueue set from {R} sg.after',
        'function space_editor:space_group/preview_scan',
        f'execute if data {R} hit.id run function space_editor:preview/reload_hit with {R} hit',
        'function space_editor:link/validate_groups',
        'scoreboard players set #pair_ok se.v 1',
    ])
    drain('space_group/preview_scan', 'sgPreviewQueue', 'space_group/preview_next')
    fn('space_group/preview_next', [
        f'function space_editor:preview/update_region with {R} sgPreviewQueue[0]',
        f'data remove {R} sgPreviewQueue[0]',
    ])
    prepend('region/apply_hit', [f'execute if data {R} {{activeTool:"delete"}} if data {R} hit.spaceLinkGroupId run return run function space_editor:space_group/delete with {R} hit'])
    prepend('region/delete_selected', [f'execute if data {R} hit.spaceLinkGroupId run return run function space_editor:space_group/delete with {R} hit'])
    fn('space_group/delete', [
        'scoreboard players set #pair_ok se.v 0',
        f'data remove {R} sgDelete', f'$data modify {R} sgDelete set from {D} regions[{{id:$(id)}}]',
        f'function space_editor:space_group/load with {R} sgDelete',
        'execute unless score #sg_ok se.v matches 1 run return 0',
        f'data modify {R} sg.before.masks set value []',
        f'$data modify {R} sg.before.masks append from {D} masks[{{regionId:$(id)}}]',
        f'data modify {R} sg.before.compatibilityPairs set value []',
        *[f'$data modify {R} sg.before.compatibilityPairs append from {D} regionPairs[{{kind:"space_link",{side}:$(id)}}]' for side in ('a', 'b')],
        f'execute unless data {D} retiredSpaceLinkPairs run data modify {D} retiredSpaceLinkPairs set value []',
        f'data modify {D} retiredSpaceLinkPairs append from {R} sg.before.compatibilityPairs[]',
        f'data modify {R} sg.after set from {R} sg.before.regions',
        f'$data remove {R} sg.after[{{id:$(id)}}]',
        f'data modify {R} sg.group.members set value []',
        f'data modify {R} sg.queue set from {R} sg.after',
        'function space_editor:space_group/member_ids',
        f'execute store result score #sg_left se.v run data get {R} sg.after',
        'execute if score #sg_left se.v matches 1 run function space_editor:space_group/dissolve',
        'execute if score #sg_left se.v matches 2.. run function space_editor:space_group/store',
        f'$data remove {D} regions[{{id:$(id)}}]', f'$data remove {D} masks[{{regionId:$(id)}}]',
        *[f'$data remove {D} regionPairs[{{kind:"space_link",{side}:$(id)}}]' for side in ('a', 'b')],
        *[f'$data remove {R} spaceLinkContacts[{{{side}RegionId:$(id)}}]' for side in ('source', 'target')],
        f'data modify {R} sg.operation set value "delete"',
        'function space_editor:space_group/action',
        'function space_editor:pair/cancel',
        f'data remove {R} hit', f'data modify {D} selectedId set value ""',
        'function space_editor:link/clean_groups', 'function space_editor:link/validate_groups',
        'function space_editor:preview/resync', 'scoreboard players set #pair_ok se.v 1',
    ])
    drain('space_group/member_ids', 'sg.queue', 'space_group/member_id_next')
    fn('space_group/member_id_next', [
        f'data modify {R} sg.group.members append from {R} sg.queue[0].id', f'data remove {R} sg.queue[0]',
    ])
    fn('space_group/dissolve', [
        f'function space_editor:space_group/remove_group with {R} sg.group',
        *[f'data remove {R} sg.after[0].{key}' for key in ('spaceLinkGroupId', 'kind', 'legacyPairId')],
        f'data modify {R} sg.queue set from {R} sg.after',
        'function space_editor:space_group/store_scan', f'data remove {R} sg.group',
    ])
    fn('space_group/remove_group', [f'$data remove {D} spaceLinkGroups[{{id:$(id)}}]'])
    # Legacy pair APIs may not reintroduce pair membership or delete both members.
    prepend('pair/delete', [f'$execute if data {D} regionPairs[{{id:$(pairId)}}].spaceLinkGroupId run return run ' + message('移行済みSpaceLinkはRegionIDを指定してspace_group/deleteを使用してください。', 'red')])
    prepend('pair/configure', [f'$execute if data {D} regionPairs[{{id:$(id)}}].spaceLinkGroupId run return run function space_editor:space_group/configure_legacy {{id:$(id),groupId:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}}'])
    # Room association remains a two-endpoint relation with its own old ID.
    fn('space_group/configure_legacy', [
        f'$data modify {R} sgConfig set from {D} regionPairs[{{id:$(id)}}]',
        f'$data modify {R} sgConfig.groupId set value $(groupId)',
        f'$data modify {R} sgConfig.roomA set value "$(roomA)"', f'$data modify {R} sgConfig.roomB set value "$(roomB)"',
        f'execute store result score #sg_cfg se.v run data get {R} sgConfig.groupId',
        'execute unless score #sg_cfg se.v matches 0.. run return 0',
        f'$execute if score #sg_cfg se.v matches 1.. if data {D} linkGroups[{{id:$(groupId)}}] unless data {D} linkGroups[{{id:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}}] run return 0',
        f'$execute if score #sg_cfg se.v matches 1.. unless data {D} linkGroups[{{id:$(groupId)}}] run data modify {D} linkGroups append value {{id:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}}',
        f'function space_editor:space_group/configure_rooms with {R} sgConfig',
        f'$data modify {D} regionPairs[{{id:$(id)}}] set from {R} sgConfig',
        'function space_editor:link/clean_groups', 'function space_editor:link/validate_groups',
    ])
    fn('space_group/configure_rooms', [
        f'$data modify {D} regions[{{id:$(a)}}].roomId set value "$(roomA)"',
        f'$data modify {D} regions[{{id:$(b)}}].roomId set value "$(roomB)"',
    ])
    fn('space_group/set_room', [
        f'data remove {R} hit', f'$data modify {R} hit set from {D} regions[{{id:$(id)}}]',
        f'execute unless data {R} hit.spaceLinkGroupId run return 0',
        f'function space_editor:space_group/load with {R} hit',
        'execute unless score #sg_ok se.v matches 1 run return 0',
        f'data modify {R} sg.after set from {R} sg.before.regions',
        f'$data modify {R} sg.after[{{id:$(id)}}].roomId set value "$(roomId)"',
        f'data modify {R} sg.operation set value "room"',
        'function space_editor:space_group/commit',
    ])


def runtime():
    # The existing tick captures everybody before any contacts or TP.
    fn('link/player', [
        'execute unless entity @s[nbt={DeathTime:0s}] run return 0',
        'function space_editor:teleport/read_snapshot',
        f'execute unless data {R} tpPlayer.point run return 0',
        f'data modify {R} linkQueue set from {D} regions',
        'function space_editor:link/scan',
        f'execute if data {R} linkQueue[0] run data modify {R} spaceLinkRuntimeWarnings append value {{reason:"source_scan_limit_4096"}}',
    ])
    drain('link/scan', 'linkQueue', 'link/scan_next', 4096)
    fn('link/scan_next', [
        f'data modify {R} spatialRegion set from {R} linkQueue[0]',
        f'execute if data {R} spatialRegion{{kind:"space_link"}} if data {R} spatialRegion.spaceLinkGroupId run function space_editor:link/check',
        f'data remove {R} linkQueue[0]',
    ])
    # membership check uses IDs, never RoomID (which need not be unique).
    fn('link/contact', [
        f'data remove {R} contactGroup',
        f'$data modify {R} contactGroup set from {D} spaceLinkGroups[{{id:$(spaceLinkGroupId)}}]',
        f'execute unless data {R} contactGroup.id run return 0',
        f'data modify {R} contactSource set from {R} spatialRegion',
        f'data modify {R} sg.group.localSize set from {R} contactGroup.localSize',
        f'data modify {R} frame set from {R} contactSource',
        'scoreboard players set #sg_ok se.v 1',
        'function space_editor:space_group/validate_frame',
        'execute unless score #sg_ok se.v matches 1 run return 0',
        f'execute store result score #contact_count se.v run data get {R} contactGroup.members',
        'execute unless score #contact_count se.v matches 2..4096 run return 0',
        f'data modify {R} contactMembers set from {R} contactGroup.members',
        'scoreboard players set #source_member se.v 0',
        'function space_editor:link/source_scan',
        'execute unless score #source_member se.v matches 1 run return 0',
        f'data modify {R} contactMembers set from {R} contactGroup.members',
        f'data modify {R} contactSeen set value []',
        'function space_editor:link/target_scan',
    ])
    drain('link/source_scan', 'contactMembers', 'link/source_next')
    fn('link/source_next', [
        f'execute store result score #contact_id se.v run data get {R} contactMembers[0]',
        f'execute store result score #contact_source se.v run data get {R} contactSource.id',
        'execute if score #contact_id se.v = #contact_source se.v run scoreboard players set #source_member se.v 1',
        f'data remove {R} contactMembers[0]',
    ])
    drain('link/target_scan', 'contactMembers', 'link/target_next')
    fn('link/target_next', [
        f'data modify {R} contactRef.id set from {R} contactMembers[0]',
        f'data modify {R} contactRef.groupId set from {R} contactGroup.id',
        f'data modify {R} contactRef.sourceId set from {R} contactSource.id',
        f'function space_editor:link/target with {R} contactRef',
        f'data remove {R} contactMembers[0]',
    ])
    fn('link/target', [
        f'$execute if data {R} contactSource{{id:$(id)}} run return 0',
        f'$execute if data {R} contactSeen[{{id:$(id)}}] run return 0',
        f'$data modify {R} contactSeen append value {{id:$(id)}}',
        f'data modify {R} map set value {{}}',
        f'data modify {R} map.source set from {R} contactSource',
        f'$data modify {R} map.target set from {D} regions[{{id:$(id),spaceLinkGroupId:$(groupId),kind:"space_link"}}]',
        f'execute unless data {R} map.target.id run return run function space_editor:link/invalid_target with {R} contactRef',
        f'data modify {R} sg.group.localSize set from {R} contactGroup.localSize',
        'scoreboard players set #sg_ok se.v 1',
        f'data modify {R} frame set from {R} map.target',
        'function space_editor:space_group/validate_frame',
        'execute unless score #sg_ok se.v matches 1 run return run function space_editor:link/invalid_target with storage space_editor:runtime contactRef',
        f'data modify {R} map.point set from {R} tpPlayer.point',
        f'data modify {R} map.vector set from {R} tpPlayer.vector',
        f'data modify {R} map.yaw set from {R} tpPlayer.rotation[0]',
        f'data modify {R} map.pitch set from {R} tpPlayer.rotation[1]',
        'function space_editor:mapping/position',
        f'data modify {R} linkContact set from {R} tpPlayer',
        f'$data modify {R} linkContact.spaceLinkGroupId set value $(groupId)',
        f'$data modify {R} linkContact.sourceRegionId set value $(sourceId)',
        f'$data modify {R} linkContact.targetRegionId set value $(id)',
        f'data modify {R} linkContact.sourceRoomId set from {R} contactSource.roomId',
        f'data modify {R} linkContact.targetRoomId set from {R} map.target.roomId',
        f'data modify {R} linkContact.destination set from {R} map.result',
        f'$data modify {R} linkContact.projectionPathId set value {{spaceLinkGroupId:$(groupId),sourceRegionId:$(sourceId),targetRegionId:$(id)}}',
        f'data modify {R} linkContact.projectionPathId.uuid set from {R} tpPlayer.uuid',
        f'data modify {R} linkContact.projectionPathId.instanceId set from {R} tpPlayer.instanceId',
        f'data modify {R} spaceLinkContacts append from {R} linkContact',
    ])
    fn('link/invalid_target', [f'$data modify {R} spaceLinkRuntimeWarnings append value {{reason:"invalid_member",spaceLinkGroupId:$(groupId),sourceRegionId:$(sourceId),targetRegionId:$(id)}}'])
    prepend('teleport/tick', [f'data modify {R} spaceLinkRuntimeWarnings set value []'])
    replace('teleport/snapshot', f'data modify {R} snapshot.point', f'data modify {R} snapshot.vector set from entity @s Motion\ndata modify {R} snapshot.point')
    # Explicit group mapping API for 06 after a transfer or after leaving a volume.
    fn('space_group/map', [
        'scoreboard players set #map_ok se.v 0', f'data remove {R} map.result',
        f'data remove {R} map.source', f'data remove {R} map.target',
        f'$data modify {R} map.source set from {D} regions[{{id:$(source),spaceLinkGroupId:$(groupId)}}]',
        f'$data modify {R} map.target set from {D} regions[{{id:$(target),spaceLinkGroupId:$(groupId)}}]',
        f'execute unless data {R} map.source.id run return 0', f'execute unless data {R} map.target.id run return 0',
        f'function space_editor:space_group/load with {R} map.source',
        'execute unless score #sg_ok se.v matches 1 run return 0',
        f'$execute unless data {R} sg.before.regions[{{id:$(source)}}] run return 0',
        f'$execute unless data {R} sg.before.regions[{{id:$(target)}}] run return 0',
        'function space_editor:mapping/position',
    ])


def ui(s):
    # Existing editor is intentionally single-owner; reject takeover before reset.
    guard = 'execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run ' + message('別プレイヤーが編集中です。終了後に開始してください。', 'red')
    prepend('start', [guard])
    prepend('play', [guard])
    for name in ('pair/held_teleport', 'pair/held_space_link', 'pair/held_proxy_existence', 'pair/click', 'pair/select', 'pair/gesture', 'pair/confirm'):
        prepend(name, [guard])
    # Session ownership is UUID based, not a shared "held" flag.
    prepend('pair/begin_session', ['function space_editor:pair/cancel'])
    s.append(F / 'pair/begin_session.mcfunction', [f'data modify {R} pairSession.owner set from entity @s UUID'])
    fn('space_group/check_owner', [
        'scoreboard players set #session_owner se.v 0',
        f'data modify {R} ownerLookup.uuid set from entity @s UUID',
        f'function space_editor:space_group/owner_match with {R} ownerLookup',
    ])
    fn('space_group/owner_match', [f'$execute if data {R} pairSession{{owner:$(uuid)}} run scoreboard players set #session_owner se.v 1'])
    for kind in ('teleport', 'space_link', 'proxy_existence'):
        prepend('pair/held_' + kind, [
            'function space_editor:space_group/check_owner',
            f'execute if data {R} pairSession.owner unless score #session_owner se.v matches 1 run return 0',
        ])
    # Expire disconnected/stale owners before evaluating any player's tools.
    prepend('tick', ['function space_editor:space_group/session_tick'])
    fn('space_group/session_tick', [
        'scoreboard players set #session_live se.v 0',
        f'execute as @a[tag=space_editor.editing] if data {R} pairSession.owner run function space_editor:space_group/session_player',
        f'execute if data {R} pairSession.owner unless score #session_live se.v matches 1 run function space_editor:pair/cancel',
    ])
    fn('space_group/session_player', [
        'function space_editor:space_group/check_owner',
        'execute unless score #session_owner se.v matches 1 run return 0',
        'scoreboard players set #session_live se.v 1',
    ])
    # Ordinary click selects an existing group and starts ADD; Shift first-click
    # selects POSE. Subsequent Shift only edits the chosen mode's target.
    prepend('pair/select', [f'execute if data {R} pairSession{{kind:"space_link"}} run return run function space_editor:space_group/select'])
    fn('space_group/select', [
        f'execute if data {R} hit.pairId run return run ' + message('旧ペアを先に/reloadで移行してください。', 'red'),
        f'data modify {D} selectedId set from {R} hit.idText',
        f'data modify {R} pairSession.selected set from {R} hit.id',
        f'data modify {R} pairSession.mode set value "add"',
        f'data modify {R} pairSession.groupId set value 0',
        f'execute if data {R} hit.spaceLinkGroupId run data modify {R} pairSession.groupId set from {R} hit.spaceLinkGroupId',
        f'data modify {R} frame set from {R} hit', 'function space_editor:pair/frame',
        f'execute store result score @s se.prot run data get {R} frame.rotationY',
        f'execute store result score @s se.pflip run data get {R} frame.flipY',
        f'execute if data {R} hit.spaceLinkGroupId if predicate {{condition:"minecraft:entity_properties",entity:"this",predicate:{{flags:{{is_sneaking:true}}}}}} run return run function space_editor:space_group/select_pose',
        'function space_editor:space_group/start_add',
    ])
    fn('space_group/select_id', [
        guard,
        'execute unless entity @s[tag=space_editor.editing] run return 0',
        f'$execute unless data {D} regions[{{id:$(id)}}] run return 0',
        f'$execute if data {D} regions[{{id:$(id)}}].kind unless data {D} regions[{{id:$(id),kind:"space_link"}}] run return 0',
        'function space_editor:pair/cancel', 'function space_editor:pair/held_space_link',
        f'$data modify {R} hit set from {D} regions[{{id:$(id)}}]',
        'function space_editor:space_group/select',
    ])
    fn('space_group/select_pose', [
        f'data remove {R} pairPending', f'data modify {R} pairSession.mode set value "pose"',
        message('既存Regionの姿勢編集。Shift+右クリック: 回転/FlipY。通常クリック: 連続追加へ。', 'green'),
    ])
    fn('space_group/start_add', [
        f'data modify {R} pairSession.mode set value "add"',
        f'data modify {R} pairPending set value {{kind:"space_link"}}',
        f'data modify {R} pairPending.source set from {R} pairSession.selected',
        f'function space_editor:space_group/refresh_source with {R} pairPending',
        'function space_editor:pair/track',
    ])
    fn('space_group/refresh_source', [
        f'$data modify {R} pairPending.frame set from {D} regions[{{id:$(source)}}]',
        f'data modify {R} frame set from {R} pairPending.frame', 'function space_editor:pair/frame',
        f'data modify {R} pairPending.frame set from {R} frame',
        *[f'data remove {R} pairPending.frame.{key}' for key in ('spaceLinkGroupId', 'legacyPairId', 'pairId', 'partnerId', 'side')],
    ])
    prepend('pair/confirm', [f'execute if data {R} pairPending{{kind:"space_link"}} run return run function space_editor:space_group/confirm'])
    fn('space_group/confirm', [
        # Preview-only pairId must never reach the persistent group API.
        f'data remove {R} pairCandidate.pairId', f'data remove {R} pairCandidate.side',
        f'function space_editor:space_group/add with {R} pairPending',
        'execute unless score #pair_ok se.v matches 1 run return 0',
        f'data modify {R} pairSession.groupId set from {R} sg.group.id',
        'function space_editor:space_group/start_add',
    ])
    # Existing pair/click handles Shift before confirm. Pose mode normal-click
    # resumes add; ordinary add confirmation is never mistaken for selection.
    replace('pair/click', f'execute if data {R} pairPending run return run function space_editor:pair/confirm',
            f'execute if data {R} pairSession{{kind:"space_link",mode:"pose"}} run return run function space_editor:space_group/start_add\nexecute if data {R} pairPending run return run function space_editor:pair/confirm')
    replace('pair/held_space_link', 'Pair編集: ', 'SpaceLink編集: ')
    s.append(F / 'pair/held_space_link.mcfunction', [
        f'execute if data {R} pairSession.selected run title @s actionbar [{{text:"SpaceLink Group #",color:"green"}},{{nbt:"pairSession.groupId",storage:"space_editor:runtime"}},{{text:" / Source Region #"}},{{nbt:"pairSession.selected",storage:"space_editor:runtime"}},{{text:" / 対象="}},{{nbt:"pairSession.mode",storage:"space_editor:runtime"}},{{text:" (add=新規候補 / pose=既存) Rot="}},{{score:{{name:"@s",objective:"se.prot"}}}},{{text:" Flip="}},{{score:{{name:"@s",objective:"se.pflip"}}}}]',
    ])
    # Reuse frame and arrow rendering, changing only the temporary label fields.
    prepend('preview/spawn', [f'execute if data {R} renderRegion.spaceLinkGroupId run return run function space_editor:space_group/preview'])
    fn('space_group/preview', [
        f'data modify {R} frame set from {R} renderRegion', 'function space_editor:pair/frame',
        f'data modify {R} frame.pairId set from {R} frame.spaceLinkGroupId',
        f'data modify {R} frame.side set from {R} frame.idText',
        'function space_editor:pair/spawn_frame with storage space_editor:runtime frame',
        'function space_editor:pair/direction_points',
        'function space_editor:space_group/spawn_directions with storage space_editor:runtime frame',
    ])
    write(F / 'space_group/spawn_directions.mcfunction', (F / 'pair/spawn_directions.mcfunction').read_text(encoding='utf-8').replace('Pair #$(pairId)', 'Group #$(spaceLinkGroupId)'))
    s.append(F / 'pair/help.mcfunction', [
        message('SpaceLink: 通常クリックでグループ選択→連続追加。持ち替えで未確定候補を終了。'),
        message('SpaceLink: Shiftで最初に選択すると既存Regionの姿勢編集。通常クリックで追加へ。'),
        message('SpaceLink削除は選択Regionのみ。残り1個は通常Regionとして残します。'),
    ])
    replace('pair/help', '削除はペア両方。', 'TP削除はペア両方。SpaceLink削除は選択Regionのみ。')
    # Keep guards before the newly inserted SpaceLink dispatch branches too.
    for name in ('pair/select', 'pair/confirm'):
        prepend(name, [guard])
