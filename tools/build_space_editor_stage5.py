"""Stage 05: additive paired Regions and teleport, layered on Stage 04."""
from __future__ import annotations

import re

import build_space_editor_stage4 as stage4

F = stage4.F
write = stage4.write
append = stage4.append
insert_before = stage4.insert_before
message = stage4.message
dimensions = stage4.dimensions
R = "storage space_editor:runtime"
D = "storage space_editor:document"


def fn(name: str, lines: list[str]) -> None:
    """Write Stage 05 commands without integer X/Z block-center coercion.

    Macro doubles such as 22.0 expand to `22`. Relative coordinates from an
    explicit origin retain exact real coordinates for TP and display entities.
    """
    coords = r'(\$\([\w]+\)) (\$\([\w]+\)) (\$\([\w]+\))'
    result = []
    for line in lines:
        line = re.sub(r'positioned ' + coords, r'positioned 0.0 0.0 0.0 positioned ~\1 ~\2 ~\3', line)
        line = re.sub(r'run tp @s ' + coords, r'positioned 0.0 0.0 0.0 run tp @s ~\1 ~\2 ~\3', line)
        line = re.sub(r'run summon (minecraft:[\w]+) ' + coords,
                      r'positioned 0.0 0.0 0.0 run summon \1 ~\2 ~\3 ~\4', line)
        result.append(line)
    stage4.fn(name, result)


def basis(rotation: int, flip: int) -> tuple[tuple[int, int], ...]:
    """World components (local axis, sign); positive yaw matches Minecraft."""
    horizontal = {0: ((0, 1), (2, 1)), 90: ((2, -1), (0, 1)),
                  180: ((0, -1), (2, -1)), 270: ((2, 1), (0, -1))}
    x, z = horizontal[rotation]
    return x, (1, -1 if flip else 1), z


def read_fixed(path: str, score: str, factor: int = 2000, scale: float = 0.0005, nbt_type: str = "double") -> list[str]:
    # data-get floors. Recover exact fixed-point values produced by this module
    # when IEEE multiplication places them just below the integral score.
    return [f"execute store result score {score} se.v run data get {R} {path} {factor}",
            f"scoreboard players operation #quant_next se.v = {score} se.v",
            "scoreboard players add #quant_next se.v 1",
            f"execute store result {R} quantized {nbt_type} {scale} run scoreboard players get #quant_next se.v",
            f"execute store success score #quant_diff se.v run data modify {R} quantized set from {R} {path}",
            f"execute if score #quant_diff se.v matches 0 run scoreboard players operation {score} se.v = #quant_next se.v"]


def generate_transform() -> None:
    # map.source / target: Region records. point is world coordinates, vector
    # is optional. Points use half-milliblocks internally so centers never round.
    lines = [f"data remove {R} map.result", "scoreboard players set #map_ok se.v 1"]
    for end in ("source", "target"):
        lines += [f"execute unless data {R} map.{end}.rotationY run data modify {R} map.{end}.rotationY set value 0",
                  f"execute unless data {R} map.{end}.flipY run data modify {R} map.{end}.flipY set value 0b"]
        for axis in "xyz":
            lines += [f"execute store result score #map_{end}_{axis} se.v run data get {R} map.{end}.{axis}1m 1",
                      f"execute store result score #map_tmp se.v run data get {R} map.{end}.{axis}2m 1",
                      f"scoreboard players operation #map_{end}_{axis} se.v += #map_tmp se.v"]
    for i, axis in enumerate("xyz"):
        lines += [*read_fixed(f"map.point[{i}]", f"#map_p{axis}"),
                  f"scoreboard players operation #map_p{axis} se.v -= #map_source_{axis} se.v"]
    for rot in (0, 90, 180, 270):
        for flip in (0, 1):
            b = basis(rot, flip)
            inverse, forward = [], []
            for world, (local, sign) in enumerate(b):
                wa, la = "xyz"[world], "xyz"[local]
                inverse += [f"scoreboard players operation #map_l{la} se.v = #map_p{wa} se.v"]
                forward += [f"scoreboard players operation #map_o{wa} se.v = #map_l{la} se.v"]
                if sign < 0:
                    inverse += [f"scoreboard players operation #map_l{la} se.v *= #minus_one se.v"]
                    forward += [f"scoreboard players operation #map_o{wa} se.v *= #minus_one se.v"]
            fn(f"mapping/inverse_{rot}_{flip}", inverse)
            fn(f"mapping/forward_{rot}_{flip}", forward)
    dispatch = []
    for end, direction in (("source", "inverse"), ("target", "forward")):
        dispatch += [f"execute if data {R} map.{end}{{rotationY:{rot},flipY:{flip}b}} run function space_editor:mapping/{direction}_{rot}_{flip}"
                     for rot in (0, 90, 180, 270) for flip in (0, 1)]
    fn("mapping/vector_scores", dispatch)
    lines += ["function space_editor:mapping/vector_scores", f'data modify {R} map.result set value {{point:[0d,0d,0d],vector:[0d,0d,0d],yaw:0f,pitch:0f}}',
              f"data modify {R} map.result.dimension set from {R} map.target.dimension"]
    for i, axis in enumerate("xyz"):
        lines += [f"scoreboard players operation #map_o{axis} se.v += #map_target_{axis} se.v",
                  f"execute store result {R} map.result.point[{i}] double 0.0005 run scoreboard players get #map_o{axis} se.v",
                  f"execute store result {R} map.result.{axis} double 0.0005 run scoreboard players get #map_o{axis} se.v"]
    lines += [f"execute if data {R} map.vector run function space_editor:mapping/vector",
              f"execute if data {R} map.yaw run function space_editor:mapping/look"]
    fn("mapping/position", lines)
    fn("mapping/vector", [
        *[line for i, axis in enumerate("xyz") for line in read_fixed(f"map.vector[{i}]", f"#map_p{axis}")],
        "function space_editor:mapping/vector_scores",
        *[f"execute store result {R} map.result.vector[{i}] double 0.0005 run scoreboard players get #map_o{axis} se.v" for i, axis in enumerate("xyz")],
    ])
    fn("mapping/look", [
        f"execute unless data {R} map.pitch run data modify {R} map.pitch set value 0f",
        *read_fixed("map.yaw", "#map_yaw", 1000, 0.001, "float"),
        *read_fixed("map.pitch", "#map_pitch", 1000, 0.001, "float"),
        f"execute store result score #map_angle se.v run data get {R} map.source.rotationY 1000",
        "scoreboard players operation #map_yaw se.v -= #map_angle se.v",
        f"execute store result score #map_angle se.v run data get {R} map.target.rotationY 1000",
        "scoreboard players operation #map_yaw se.v += #map_angle se.v",
        "scoreboard players set #map_circle se.v 360000",
        "scoreboard players add #map_yaw se.v 180000",
        "scoreboard players operation #map_yaw se.v %= #map_circle se.v",
        "scoreboard players remove #map_yaw se.v 180000",
        f"execute if data {R} map.source{{flipY:1b}} run scoreboard players operation #map_pitch se.v *= #minus_one se.v",
        f"execute if data {R} map.target{{flipY:1b}} run scoreboard players operation #map_pitch se.v *= #minus_one se.v",
        f"execute store result {R} map.result.yaw float 0.001 run scoreboard players get #map_yaw se.v",
        f"execute store result {R} map.result.pitch float 0.001 run scoreboard players get #map_pitch se.v",
    ])


def generate_frames() -> None:
    # Scratch frame is normalized in one place, retaining all unknown fields.
    normalize = ["scoreboard players set #frame_ok se.v 1",
                 f"execute unless data {R} frame.rotationY run data modify {R} frame.rotationY set value 0",
                 f"execute unless data {R} frame.flipY run data modify {R} frame.flipY set value 0b",
                 f"data modify {R} frame.localSize set value [I;0,0,0]",
                 f"data modify {R} frame.min set value [0d,0d,0d]",
                 f"data modify {R} frame.maxExclusive set value [0d,0d,0d]"]
    for i, axis in enumerate("xyz"):
        normalize += [f"execute store result score #f{axis}1 se.v run data get {R} frame.{axis}1m 1",
                      f"execute store result score #f{axis}2 se.v run data get {R} frame.{axis}2m 1",
                      f"scoreboard players operation #fs{axis} se.v = #f{axis}2 se.v",
                      f"scoreboard players operation #fs{axis} se.v -= #f{axis}1 se.v",
                      f"execute unless score #fs{axis} se.v matches 100..32000 run scoreboard players set #frame_ok se.v 0",
                      # Keep doubled point arithmetic within signed scoreboard range.
                      f"execute unless score #f{axis}1 se.v matches -500000000..500000000 run scoreboard players set #frame_ok se.v 0",
                      f"execute unless score #f{axis}2 se.v matches -500000000..500000000 run scoreboard players set #frame_ok se.v 0",
                      f"execute store result {R} frame.{axis}1 double 0.001 run scoreboard players get #f{axis}1 se.v",
                      f"execute store result {R} frame.{axis}2 double 0.001 run scoreboard players get #f{axis}2 se.v",
                      f"execute store result {R} frame.min[{i}] double 0.001 run scoreboard players get #f{axis}1 se.v",
                      f"execute store result {R} frame.maxExclusive[{i}] double 0.001 run scoreboard players get #f{axis}2 se.v",
                      f"execute store result {R} frame.s{axis} double 0.001 run scoreboard players get #fs{axis} se.v",
                      f"execute store result {R} frame.s{axis}m int 1 run scoreboard players get #fs{axis} se.v",
                      f"scoreboard players operation #fc{axis} se.v = #f{axis}1 se.v",
                      f"scoreboard players operation #fc{axis} se.v += #f{axis}2 se.v",
                      f"execute store result {R} frame.c{axis} double 0.0005 run scoreboard players get #fc{axis} se.v"]
    normalize += [
        f'execute if data {R} frame{{dimension:"minecraft:overworld"}} unless score #fy1 se.v matches -64000..319900 run scoreboard players set #frame_ok se.v 0',
        f'execute if data {R} frame{{dimension:"minecraft:overworld"}} unless score #fy2 se.v matches -63900..320000 run scoreboard players set #frame_ok se.v 0',
        f'execute unless data {R} frame{{dimension:"minecraft:overworld"}} unless score #fy1 se.v matches 0..255900 run scoreboard players set #frame_ok se.v 0',
        f'execute unless data {R} frame{{dimension:"minecraft:overworld"}} unless score #fy2 se.v matches 100..256000 run scoreboard players set #frame_ok se.v 0',
    ]
    for rot in (0, 90, 180, 270):
        for world, (local, _) in enumerate(basis(rot, 0)):
            normalize += [f"execute if data {R} frame{{rotationY:{rot}}} store result {R} frame.localSize[{local}] int 1 run scoreboard players get #fs{'xyz'[world]} se.v"]
    fn("pair/frame", normalize)
    # Rotate about the original center using new pose + old local dimensions.
    pose = []
    for axis in "xyz":
        pose += [f"execute store result score #fc{axis} se.v run data get {R} frame.{axis}1m 1",
                 f"execute store result score #ft se.v run data get {R} frame.{axis}2m 1",
                 f"scoreboard players operation #fc{axis} se.v += #ft se.v"]
    for rot in (0, 90, 180, 270):
        for world, (local, _) in enumerate(basis(rot, 0)):
            pose += [f"execute if data {R} frame{{rotationY:{rot}}} store result score #fs{'xyz'[world]} se.v run data get {R} frame.localSize[{local}] 1"]
    pose += ["scoreboard players set #pose_ok se.v 1"]
    for axis in "xyz":
        pose += [f"scoreboard players operation #f{axis}1 se.v = #fc{axis} se.v",
                 f"scoreboard players operation #f{axis}1 se.v -= #fs{axis} se.v",
                 f"scoreboard players operation #ft se.v = #f{axis}1 se.v",
                 "scoreboard players operation #ft se.v %= #two se.v",
                 "execute unless score #ft se.v matches 0 run scoreboard players set #pose_ok se.v 0",
                 f"scoreboard players operation #f{axis}1 se.v /= #two se.v",
                 f"scoreboard players operation #f{axis}2 se.v = #f{axis}1 se.v",
                 f"scoreboard players operation #f{axis}2 se.v += #fs{axis} se.v",
                 *[f"execute store result {R} frame.{axis}{edge}m int 1 run scoreboard players get #f{axis}{edge} se.v" for edge in (1, 2)]]
    pose += ["function space_editor:pair/frame",
             "execute unless score #pose_ok se.v matches 1 run scoreboard players set #frame_ok se.v 0"]
    fn("pair/pose_bounds", pose)


def generate_pairs() -> None:
    generate_frames()
    insert_before(F / "load.mcfunction", "function space_editor:mask/rebuild_all", [
        f"execute unless data {D} regionPairs run data modify {D} regionPairs set value []",
        f"execute unless data {D} nextPairId run data modify {D} nextPairId set value 1",
        "function space_editor:pair/cancel",
    ])
    fn("pair/load", [
        f"data remove {R} pair", f"data remove {R} editA", f"data remove {R} editB",
        f'$data modify {R} pair set from {D} regionPairs[{{id:$(pairId)}}]',
        f"execute if data {R} pair.id run function space_editor:pair/load_members with {R} pair",
    ])
    fn("pair/load_members", [
        f'$data modify {R} editA set from {D} regions[{{id:$(a)}}]',
        f'$data modify {R} editB set from {D} regions[{{id:$(b)}}]',
    ])
    # Explicit source id and candidate Region record are also the 06 API.
    fn("pair/create", [
        "scoreboard players set #pair_ok se.v 0",
        f"data remove {R} editA",
        f'$data modify {R} editA set from {D} regions[{{id:$(source)}}]',
        f'execute unless data {R} editA.id run return 0',
        f'execute if data {R} editA.pairId run return run ' + message("このRegionは既にペアに属しています。", "red"),
        f'execute if data {R} editA{{kind:"proxy_existence"}} run return 0',
        f'$data modify {R} pair set value {{id:0,a:$(source),b:0,kind:"$(kind)",localSize:[I;0,0,0],groupId:0,roomA:"",roomB:"",direction:"both",cooldownTicks:20}}',
        f'execute unless data {R} pair{{kind:"teleport"}} unless data {R} pair{{kind:"space_link"}} run return 0',
        f"data modify {R} frame set from {R} editA", "function space_editor:pair/frame",
        "execute unless score #frame_ok se.v matches 1 run return 0",
        f"data modify {R} editA set from {R} frame",
        f"data modify {R} pair.localSize set from {R} frame.localSize",
        f"data modify {R} frame set from {R} pairCandidate", "function space_editor:pair/frame",
        "execute unless score #frame_ok se.v matches 1 run return run " + message("配置先がRegionの範囲制限を超えています。", "red"),
        "scoreboard players set #different_size se.v 0",
        f"execute store success score #different_size se.v run data modify {R} frame.localSize set from {R} pair.localSize",
        "execute if score #different_size se.v matches 1 run return run " + message("ローカルサイズが一致しません。", "red"),
        f"data modify {R} editB set from {R} frame",
        f"execute store result {R} pair.id int 1 run data get {D} nextPairId 1",
        f"execute store result {R} pair.b int 1 run data get {D} nextId 1",
        f"data modify {R} editB.id set from {R} pair.b",
        f"function space_editor:pair/identify with {R} pair",
        f"data modify {R} pairBefore set value {{}}",
        f"data modify {R} pairOperation set value \"create\"",
        f"function space_editor:pair/store with {R} pair",
        f"data modify {D} regionPairs append from {R} pair",
        f"execute store result score #pair_next se.v run data get {D} nextPairId 1",
        "scoreboard players add #pair_next se.v 1",
        f"execute store result {D} nextPairId int 1 run scoreboard players get #pair_next se.v",
        f"execute store result score #pair_next se.v run data get {D} nextId 1",
        "scoreboard players add #pair_next se.v 1",
        f"execute store result {D} nextId int 1 run scoreboard players get #pair_next se.v",
        "function space_editor:pair/action", "function space_editor:pair/cancel", "function space_editor:preview/resync",
        "scoreboard players set #pair_ok se.v 1",
    ])
    fn("pair/identify", [
        *[f'$data modify {R} edit{side}.pairId set value $(id)' for side in ("A", "B")],
        *[f'$data modify {R} edit{side}.kind set value "$(kind)"' for side in ("A", "B")],
        f'$data modify {R} editA.partnerId set value $(b)', f'$data modify {R} editB.partnerId set value $(a)',
        f'data modify {R} editA.side set value "A"', f'data modify {R} editB.side set value "B"',
        f'$data modify {R} editB.idText set value "region_$(b)"',
        *[f'execute unless data {R} edit{side}.roomId run data modify {R} edit{side}.roomId set value ""' for side in ("A", "B")],
    ])
    fn("pair/store", [
        f'$data modify {D} regions[{{id:$(a)}}] set from {R} editA',
        f'$execute if data {D} regions[{{id:$(b)}}] run data modify {D} regions[{{id:$(b)}}] set from {R} editB',
        f'$execute unless data {D} regions[{{id:$(b)}}] run data modify {D} regions append from {R} editB',
        f'$execute if data {D} regionPairs[{{id:$(id)}}] run data modify {D} regionPairs[{{id:$(id)}}] set from {R} pair',
    ])
    fn("pair/snapshot", [
        f"data modify {R} pairBefore set value {{}}",
        *[f"data modify {R} pairBefore.{key} set from {R} {value}" for key, value in (("pair", "pair"), ("a", "editA"), ("b", "editB"))],
    ])
    fn("pair/action", [
        f'execute store result score #pair_action se.v run data get {D} nextActionId 1',
        f'data modify {R} pairAction set value {{type:"pair_edit",id:0,order:0}}',
        *[f'execute store result {R} pairAction.{key} int 1 run scoreboard players get #pair_action se.v' for key in ("id", "order")],
        f'data modify {R} pairAction.operation set from {R} pairOperation',
        f'data modify {R} pairAction.before set from {R} pairBefore',
        f'data modify {R} pairAction.after set value {{}}',
        *[f'data modify {R} pairAction.after.{key} set from {R} {value}' for key, value in (("pair", "pair"), ("a", "editA"), ("b", "editB"))],
        f'execute if data {R} {{pairOperation:"delete"}} run data modify {R} pairAction.after set value {{}}',
        f'data modify {D} actions append from {R} pairAction',
        'scoreboard players add #pair_action se.v 1',
        f'execute store result {D} nextActionId int 1 run scoreboard players get #pair_action se.v',
    ])
    generate_pair_edits()
    generate_pair_ui()


def generate_pair_edits() -> None:
    # Stage 01 has already constructed a candidate hit but has not written it.
    insert_before(F / "region/save_resize.mcfunction", "function space_editor:region/store_hit", [
        f"execute if data {R} hit.pairId run return run function space_editor:pair/edit_bounds",
    ])
    fn("pair/edit_bounds", [
        f"function space_editor:pair/load with {R} hit",
        f"execute unless data {R} editA.id run return 0", f"execute unless data {R} editB.id run return 0",
        "function space_editor:pair/snapshot",
        f'data modify {R} pairOperation set from {R} activeTool',
        f'data modify {R} old set from {R} editA', f'data modify {R} partner set from {R} editB',
        f'execute if data {R} hit{{side:"B"}} run data modify {R} old set from {R} editB',
        f'execute if data {R} hit{{side:"B"}} run data modify {R} partner set from {R} editA',
        f'execute unless data {R} {{activeTool:"move"}} run function space_editor:pair/sync_bounds',
        f'data modify {R} frame set from {R} partner', "function space_editor:pair/frame",
        "execute unless score #frame_ok se.v matches 1 run return run " + message("相手側の制限により、両方の変更を取り消しました。", "red"),
        f'data modify {R} partner set from {R} frame',
        f'data modify {R} frame set from {R} hit', "function space_editor:pair/frame",
        "execute unless score #frame_ok se.v matches 1 run return 0",
        f'data modify {R} hit set from {R} frame',
        f'data modify {R} pair.localSize set from {R} frame.localSize',
        f'data modify {R} editA set from {R} hit', f'data modify {R} editB set from {R} partner',
        f'execute if data {R} hit{{side:"B"}} run data modify {R} editB set from {R} hit',
        f'execute if data {R} hit{{side:"B"}} run data modify {R} editA set from {R} partner',
        "function space_editor:pair/commit",
    ])
    lines = []
    for axis in "xyz":
        for edge in (1, 2):
            lines += [f"execute store result score #dw{axis}{edge} se.v run data get {R} hit.{axis}{edge}m 1",
                      f"execute store result score #dt se.v run data get {R} old.{axis}{edge}m 1",
                      f"scoreboard players operation #dw{axis}{edge} se.v -= #dt se.v"]
    for rot in (0, 90, 180, 270):
        for flip in (0, 1):
            inv, out = [], []
            for world, (local, sign) in enumerate(basis(rot, flip)):
                wa, la = "xyz"[world], "xyz"[local]
                for edge in (1, 2):
                    other = edge if sign == 1 else 3 - edge
                    inv += [f"scoreboard players operation #dl{la}{edge} se.v = #dw{wa}{other} se.v"]
                    out += [f"scoreboard players operation #do{wa}{edge} se.v = #dl{la}{other} se.v"]
                    if sign < 0:
                        inv += [f"scoreboard players operation #dl{la}{edge} se.v *= #minus_one se.v"]
                        out += [f"scoreboard players operation #do{wa}{edge} se.v *= #minus_one se.v"]
            fn(f"pair/delta_inverse_{rot}_{flip}", inv)
            fn(f"pair/delta_forward_{rot}_{flip}", out)
    lines += [f"execute if data {R} {record}{{rotationY:{rot},flipY:{flip}b}} run function space_editor:pair/delta_{direction}_{rot}_{flip}"
              for record, direction in (("old", "inverse"), ("partner", "forward")) for rot in (0, 90, 180, 270) for flip in (0, 1)]
    for axis in "xyz":
        for edge in (1, 2):
            lines += [f"execute store result score #dt se.v run data get {R} partner.{axis}{edge}m 1",
                      f"scoreboard players operation #dt se.v += #do{axis}{edge} se.v",
                      f"execute store result {R} partner.{axis}{edge}m int 1 run scoreboard players get #dt se.v"]
    fn("pair/sync_bounds", lines)
    fn("pair/commit", [
        f"function space_editor:pair/store with {R} pair", "function space_editor:pair/action",
        "function space_editor:preview/resync", "scoreboard players set #pair_ok se.v 1",
    ])
    fn("pair/set_pose", [
        "scoreboard players set #pair_ok se.v 0",
        f"data remove {R} hit", f'$data modify {R} hit set from {D} regions[{{id:$(id)}}]',
        f"execute unless data {R} hit.pairId run return 0",
        f"function space_editor:pair/load with {R} hit", "function space_editor:pair/snapshot",
        f"execute unless data {R} editA.id run return 0", f"execute unless data {R} editB.id run return 0",
        f"data modify {R} frame set from {R} hit",
        f'$data modify {R} frame.rotationY set value $(rotationY)', f'$data modify {R} frame.flipY set value $(flipY)b',
        f"execute unless data {R} frame{{rotationY:0}} unless data {R} frame{{rotationY:90}} unless data {R} frame{{rotationY:180}} unless data {R} frame{{rotationY:270}} run return 0",
        f"execute unless data {R} frame{{flipY:0b}} unless data {R} frame{{flipY:1b}} run return 0",
        "function space_editor:pair/pose_bounds",
        "execute unless score #frame_ok se.v matches 1 run return run " + message("中心を保った回転を保存できる範囲ではありません。", "red"),
        f'execute if data {R} frame{{side:"A"}} run data modify {R} editA set from {R} frame',
        f'execute if data {R} frame{{side:"B"}} run data modify {R} editB set from {R} frame',
        f'data modify {R} pairOperation set value "pose"', "function space_editor:pair/commit",
    ])
    # Paired delete takes priority over attached Mask; ordinary Regions retain
    # the Stage 04 two-click Mask-first deletion contract.
    insert_before(F / "region/apply_hit.mcfunction", 'scoreboard players set #mask_deleted', [
        f'execute if data {R} {{activeTool:"delete"}} if data {R} hit.pairId run return run function space_editor:pair/delete with {R} hit',
    ])
    insert_before(F / "region/delete_selected.mcfunction", "execute unless data", [
        f"execute if data {R} hit.pairId run return run function space_editor:pair/delete with {R} hit",
    ])
    fn("pair/delete", [
        '$function space_editor:pair/load {pairId:$(pairId)}',
        f"execute unless data {R} pair.id run return 0", "function space_editor:pair/snapshot",
        f'function space_editor:pair/capture_attached with {R} pair',
        f'data modify {R} pairOperation set value "delete"',
        "function space_editor:pair/action", f"function space_editor:pair/remove with {R} pair",
        f"data remove {R} hit", f'data modify {D} selectedId set value ""',
        "function space_editor:pair/cancel", "function space_editor:preview/resync",
    ])
    fn("pair/remove", [
        *[f'$data remove {D} regions[{{id:$({key})}}]' for key in ("a", "b")],
        *[f'$data remove {D} masks[{{regionId:$({key})}}]' for key in ("a", "b")],
        f'$data remove {D} regionPairs[{{id:$(id)}}]',
    ])
    fn("pair/capture_attached", [
        f'data modify {R} pairBefore.masks set value []',
        *[f'$data modify {R} pairBefore.masks append from {D} masks[{{regionId:$({key})}}]' for key in ("a", "b")],
        f'$data modify {R} pairBefore.group set from {D} linkGroups[{{id:$(groupId)}}]',
    ])


def generate_pair_ui() -> None:
    insert_before(F / "load.mcfunction", "function space_editor:pair/cancel", [
        "scoreboard objectives add se.pheld dummy", "scoreboard objectives add se.pbase dummy",
        "scoreboard objectives add se.prot dummy", "scoreboard objectives add se.pflip dummy",
    ])
    for kind, name, color in (("teleport", "TP接続棒", "aqua"), ("space_link", "SpaceLink接続棒", "green"),
                              ("proxy_existence", "Proxy存在範囲棒", "yellow")):
        append(F / "start.mcfunction", [
            f'execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{{space_editor:{{tool:"{kind}"}}}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={{space_editor:{{tool:"{kind}"}}}},minecraft:item_model="editor:tool_{kind}",minecraft:custom_name={{text:"{name}",color:"{color}",italic:false}},minecraft:lore=[{{text:"右クリック: 対象選択 / 配置確定",italic:false}},{{text:"Shift+右クリック: 基準Yawの左右で回転・上下でFlipY",italic:false}}]]',
        ])
        insert_before(F / "tick.mcfunction", "scoreboard players set @a[scores={se.use=1..}]", [
            f'execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{{space_editor:{{tool:"{kind}"}}}}] run function space_editor:pair/held_{kind}',
            f'execute as @a[tag=space_editor.editing,scores={{se.use=1..,se.cd=0}}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{{space_editor:{{tool:"{kind}"}}}}] run function space_editor:pair/click',
        ])
        fn(f"pair/held_{kind}", [
            f'execute if data {R} pairSession unless data {R} pairSession{{kind:"{kind}"}} run function space_editor:pair/cancel',
            "execute unless score @s se.pheld matches 1 run function space_editor:pair/begin_session",
            f'data modify {R} pairSession.kind set value "{kind}"',
            "function space_editor:pair/read_intent",
            f'execute if data {R} pairPending run function space_editor:pair/track',
            f'execute if data {R} pairSession.selected run title @s actionbar [{{text:"Pair編集: ",color:"aqua"}},{{nbt:"pairSession.kind",storage:"space_editor:runtime"}},{{text:" Region #"}},{{nbt:"pairSession.selected",storage:"space_editor:runtime"}},{{text:" Rot="}},{{score:{{name:"@s",objective:"se.prot"}}}},{{text:" FlipY="}},{{score:{{name:"@s",objective:"se.pflip"}}}}]',
        ])
    insert_before(F / "tick.mcfunction", "scoreboard players set #selection_cursor_active", [
        'execute as @a[scores={se.pheld=1}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"teleport"}}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"space_link"}}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"proxy_existence"}}] run function space_editor:pair/cancel',
    ])
    fn("pair/begin_session", [
        "execute store result score @s se.pbase run data get entity @s Rotation[0] 1",
        "scoreboard players set @s se.pheld 1", "scoreboard players set @s se.prot 0", "scoreboard players set @s se.pflip 0",
        f'data modify {R} pairSession set value {{}}',
    ])
    # Reuse the existing Paste gesture definition, with an independent baseline.
    write(F / "pair/read_intent.mcfunction", (F / "paste_mode/read_intent.mcfunction").read_text(encoding="utf-8").replace("se.pyaw", "se.pbase"))
    fn("pair/cancel", [
        f"data remove {R} pairPending", f"data remove {R} pairSession", f"data remove {R} pairCandidate",
        "scoreboard players set @a se.pheld 0", *dimensions("kill @e[tag=space_editor.pair_pending]"),
    ])
    insert_before(F / "input/delete.mcfunction", "scoreboard players set", [
        f"execute if data {R} pairPending run return run function space_editor:pair/cancel",
    ])
    append(F / "play.mcfunction", ["function space_editor:pair/cancel"])
    insert_before(F / "start.mcfunction", "tag @a remove", ["function space_editor:pair/cancel"])
    fn("pair/click", [
        "scoreboard players set @s se.cd 5",
        f'execute if predicate {{condition:"minecraft:entity_properties",entity:"this",predicate:{{flags:{{is_sneaking:true}}}}}} if data {R} pairSession.selected run return run function space_editor:pair/gesture',
        f"execute if data {R} pairPending run return run function space_editor:pair/confirm",
        f'data modify {R} activeTool set value "pair_select"', f"data remove {R} hit",
        "scoreboard players set #region_ray se.v 0", "execute anchored eyes positioned ^ ^ ^ run function space_editor:region/ray",
    ])
    insert_before(F / "region/apply_hit.mcfunction", "data modify storage space_editor:document selectedId", [
        f'execute if data {R} {{activeTool:"pair_select"}} run return run function space_editor:pair/select',
    ])
    # At equal ray distance preserve list order, but connection wands omit
    # incompatible kinds. They cannot silently re-type another kind's Region.
    insert_before(F / "region/check.mcfunction", "execute store result score #lo", [
        f'execute if data {R} {{activeTool:"pair_select"}} if data {R} candidate.kind run function space_editor:pair/filter',
        f'execute if data {R} {{activeTool:"pair_select"}} if data {R} candidate.kind if score #pair_filter se.v matches 0 run return 0',
    ])
    fn("pair/filter", [
        "scoreboard players set #pair_filter se.v 0",
        *[f'execute if data {R} pairSession{{kind:"{kind}"}} if data {R} candidate{{kind:"{kind}"}} run scoreboard players set #pair_filter se.v 1' for kind in ("teleport", "space_link", "proxy_existence")],
    ])
    fn("pair/select", [
        f'data modify {D} selectedId set from {R} hit.idText',
        f'execute if data {R} pairSession{{kind:"proxy_existence"}} run return run function space_editor:pair/mark_existence',
        f'data modify {R} pairSession.selected set from {R} hit.id',
        f'data modify {R} frame set from {R} hit', "function space_editor:pair/frame",
        f"execute store result score @s se.prot run data get {R} frame.rotationY 1",
        f"execute store result score @s se.pflip run data get {R} frame.flipY 1",
        f"execute if data {R} hit.pairId run return run " + message("選択しました。Shift+右クリックで回転・反転できます。"),
        f'data modify {R} pairPending set value {{}}',
        f'data modify {R} pairPending.source set from {R} hit.id',
        f'data modify {R} pairPending.kind set from {R} pairSession.kind',
        f'data modify {R} pairPending.frame set from {R} frame',
        "function space_editor:pair/track",
    ])
    fn("pair/mark_existence", [
        f"execute if data {R} hit.pairId run return 0",
        f'data modify {R} hit.kind set value "proxy_existence"',
        f'execute unless data {R} hit.roomId run data modify {R} hit.roomId set value ""',
        f"function space_editor:region/store_hit with {R} hit", "function space_editor:preview/resync",
        message("単独のProxy存在範囲として登録しました。", "green"),
    ])
    fn("pair/gesture", [
        "function space_editor:pair/read_intent",
        "execute if score @s se.intent matches 1 run scoreboard players remove @s se.prot 90",
        "execute if score @s se.intent matches 2 run scoreboard players add @s se.prot 90",
        "execute if score @s se.prot matches ..-1 run scoreboard players set @s se.prot 270",
        "execute if score @s se.prot matches 360.. run scoreboard players set @s se.prot 0",
        "execute if score @s se.intent matches 3 run function space_editor:pair/toggle_flip",
        f"execute if data {R} pairPending run return run function space_editor:pair/track",
        f'data modify {R} pairPose set value {{}}',
        f'data modify {R} pairPose.id set from {R} pairSession.selected',
        f'execute store result {R} pairPose.rotationY int 1 run scoreboard players get @s se.prot',
        f'execute store result {R} pairPose.flipY int 1 run scoreboard players get @s se.pflip',
        f'function space_editor:pair/set_pose with {R} pairPose',
    ])
    fn("pair/toggle_flip", [
        "execute if score @s se.pflip matches 0 run return run scoreboard players set @s se.pflip 1",
        "scoreboard players set @s se.pflip 0",
    ])
    # Candidate min comes from the very same hover cell as selection and Paste.
    track = ["function space_editor:selection/track",
             f"data modify {R} frame set from {R} pairPending.frame",
             f"data modify {R} frame.dimension set from {R} hover.dimension",
             f"execute store result {R} frame.rotationY int 1 run scoreboard players get @s se.prot",
             f"execute store result {R} frame.flipY byte 1 run scoreboard players get @s se.pflip"]
    for rot in (0, 90, 180, 270):
        for world, (local, _) in enumerate(basis(rot, 0)):
            track += [f"execute if data {R} frame{{rotationY:{rot}}} store result score #ps{'xyz'[world]} se.v run data get {R} frame.localSize[{local}] 1"]
    for i, axis in enumerate("xyz"):
        track += [f"execute store result score #pp se.v run data get {R} hover.pos[{i}] 1000",
                  f"execute store result {R} frame.{axis}1m int 1 run scoreboard players get #pp se.v",
                  f"scoreboard players operation #pp se.v += #ps{axis} se.v",
                  f"execute store result {R} frame.{axis}2m int 1 run scoreboard players get #pp se.v"]
    track += ["function space_editor:pair/frame", f"data modify {R} pairCandidate set from {R} frame",
              f"data modify {R} pairCandidate.kind set from {R} pairPending.kind",
              f'data modify {R} pairCandidate.side set value "B preview"', f'data modify {R} pairCandidate.pairId set value 0',
              f"function space_editor:pair/preview_pending with {R} pairCandidate"]
    fn("pair/track", track)
    fn("pair/confirm", [f"function space_editor:pair/create with {R} pairPending"])
    generate_pair_preview()


def generate_pair_preview() -> None:
    carrier = stage4.DISPLAY_BLOCKS["guide"]
    # Existing Region frame remains the base. Extra pose indicators are rebuilt
    # only on edits/resume; pending placement updates existing entities in place.
    insert_before(F / "preview/spawn.mcfunction", "summon minecraft:block_display", [
        f"execute if data {R} renderRegion.pairId run return run function space_editor:pair/preview_region",
    ])
    append(F / "preview/spawn.mcfunction", [
        f'execute if data {R} renderRegion{{kind:"proxy_existence"}} run function space_editor:pair/preview_existence with {R} renderRegion',
    ])
    fn("pair/preview_existence", [
        '$execute in $(dimension) positioned $(cx) $(cy) $(cz) run summon minecraft:text_display ~ ~0.5 ~ {Tags:["space_editor.preview","space_editor.label"],text:{text:"ProxyExistence #$(id)",color:"yellow"},billboard:"center",see_through:1b}',
    ])
    fn("pair/preview_region", [
        f"data modify {R} frame set from {R} renderRegion", "function space_editor:pair/frame",
        f"function space_editor:pair/spawn_frame with {R} frame",
        "function space_editor:pair/direction_points", f"function space_editor:pair/spawn_directions with {R} frame",
    ])
    fn("pair/spawn_frame", [
        f'$execute in $(dimension) run summon minecraft:block_display $(x1) $(y1) $(z1) {{Tags:["space_editor.preview","space_editor.region","space_editor.pair_frame_new"],block_state:{{Name:"{stage4.DISPLAY_BLOCKS["selection"]}"}},transformation:{{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}},brightness:{{block:15,sky:15}},width:64f,height:64f}}',
        '$execute in $(dimension) run scoreboard players set @e[tag=space_editor.pair_frame_new] se.id $(id)',
        '$execute in $(dimension) run tag @e[tag=space_editor.pair_frame_new] remove space_editor.pair_frame_new',
    ])
    points = []
    for rot, quat in ((0, "[0f,0f,0f,1f]"), (90, "[0f,-0.70710677f,0f,0.70710677f]"),
                      (180, "[0f,1f,0f,0f]"), (270, "[0f,0.70710677f,0f,0.70710677f]")):
        points += [f'execute if data {R} frame{{rotationY:{rot}}} run data modify {R} frame.frontRotation set value {quat}']
    for flip, quat in ((0, "[-0.70710677f,0f,0f,0.70710677f]"), (1, "[0.70710677f,0f,0f,0.70710677f]")):
        points += [f'execute if data {R} frame{{flipY:{flip}b}} run data modify {R} frame.upRotation set value {quat}']
    for label in ("front", "up"):
        for axis in "xyz":
            points += [f"scoreboard players operation #arrow_{label}_{axis} se.v = #fc{axis} se.v"]
    for rot in (0, 90, 180, 270):
        for world, (local, sign) in enumerate(basis(rot, 0)):
            if local == 2:
                points += [f"execute if data {R} frame{{rotationY:{rot}}} run scoreboard players {'add' if sign > 0 else 'remove'} #arrow_front_{'xyz'[world]} se.v 1600"]
    points += [f"execute if data {R} frame{{flipY:0b}} run scoreboard players add #arrow_up_y se.v 1600",
               f"execute if data {R} frame{{flipY:1b}} run scoreboard players remove #arrow_up_y se.v 1600"]
    for label in ("front", "up"):
        for axis in "xyz":
            points += [f"execute store result {R} frame.{label}{axis} double 0.0005 run scoreboard players get #arrow_{label}_{axis} se.v"]
    fn("pair/direction_points", points)
    direction_lines = []
    for label, glyph, color in (("front", "➤ 前 +Z", "green"), ("up", "➤ 上 +Y", "yellow")):
        direction_lines += [f'$execute in $(dimension) positioned $({label}x) $({label}y) $({label}z) run summon minecraft:text_display ~ ~ ~ {{Tags:["space_editor.preview","space_editor.label"],text:{{text:"{glyph}",color:"{color}"}},billboard:"center",see_through:1b,shadow:1b,background:0}}']
        direction_lines += [f'$execute in $(dimension) run summon minecraft:item_display $(cx) $(cy) $(cz) {{Tags:["space_editor.preview","space_editor.label","space_editor.direction_{label}"],item:{{id:"minecraft:stick",count:1,components:{{"minecraft:item_model":"editor:direction_{label}"}}}},item_display:"none",transformation:{{translation:[0f,0f,0f],scale:[0.7f,0.7f,0.7f],left_rotation:$({label}Rotation),right_rotation:[0f,0f,0f,1f]}},brightness:{{block:15,sky:15}}}}']
    direction_lines += ['$execute in $(dimension) positioned $(cx) $(cy) $(cz) run summon minecraft:text_display ~ ~0.25 ~ {Tags:["space_editor.preview","space_editor.label"],text:{text:"$(kind) Pair #$(pairId) / $(side) / Rot $(rotationY) / Flip $(flipY)",color:"aqua"},billboard:"center",see_through:1b,shadow:1b}']
    fn("pair/spawn_directions", direction_lines)
    pending = [
        *[f'execute unless data {R} pairCandidate{{dimension:"minecraft:{dim}"}} in minecraft:{dim} run kill @e[tag=space_editor.pair_pending,distance=0..]' for dim in ("overworld", "the_nether", "the_end")],
        f'$execute in $(dimension) unless entity @e[tag=space_editor.pair_pending_box,distance=0..] run summon minecraft:block_display $(x1) $(y1) $(z1) {{Tags:["space_editor.preview","space_editor.pair_pending","space_editor.pair_pending_box"],block_state:{{Name:"{carrier}"}},transformation:{{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}},brightness:{{block:15,sky:15}},width:64f,height:64f}}',
        '$execute in $(dimension) as @e[tag=space_editor.pair_pending_box] run tp @s $(x1) $(y1) $(z1)',
        '$execute in $(dimension) as @e[tag=space_editor.pair_pending_box] run data merge entity @s {transformation:{scale:[$(sx)f,$(sy)f,$(sz)f]}}',
        "function space_editor:pair/direction_points",
        f"function space_editor:pair/pending_directions with {R} frame",
    ]
    fn("pair/preview_pending", pending)
    pending_dir = []
    for label, glyph, color in (("front", "➤ 前 +Z", "green"), ("up", "➤ 上 +Y", "yellow")):
        pending_dir += [f'$execute in $(dimension) unless entity @e[tag=space_editor.pair_pending_{label}] run summon minecraft:text_display $({label}x) $({label}y) $({label}z) {{Tags:["space_editor.preview","space_editor.pair_pending","space_editor.pair_pending_{label}"],text:{{text:"{glyph}",color:"{color}"}},billboard:"center",see_through:1b,shadow:1b}}',
                        f'$execute in $(dimension) as @e[tag=space_editor.pair_pending_{label}] run tp @s $({label}x) $({label}y) $({label}z)']
        pending_dir += [f'$execute in $(dimension) unless entity @e[tag=space_editor.pending_arrow_{label},distance=0..] run summon minecraft:item_display $(cx) $(cy) $(cz) {{Tags:["space_editor.preview","space_editor.pair_pending","space_editor.pending_arrow_{label}"],item:{{id:"minecraft:stick",count:1,components:{{"minecraft:item_model":"editor:direction_{label}"}}}},item_display:"none",transformation:{{translation:[0f,0f,0f],scale:[0.7f,0.7f,0.7f],left_rotation:$({label}Rotation),right_rotation:[0f,0f,0f,1f]}},brightness:{{block:15,sky:15}}}}',
                        f'$execute in $(dimension) as @e[tag=space_editor.pending_arrow_{label}] run tp @s $(cx) $(cy) $(cz)',
                        f'$execute in $(dimension) as @e[tag=space_editor.pending_arrow_{label}] run data merge entity @s {{transformation:{{left_rotation:$({label}Rotation)}}}}']
    fn("pair/pending_directions", pending_dir)


def generate_teleport() -> None:
    stage4.stage3.stage2.stage1.js(stage4.DP / "data/space_editor/tags/function/before_teleport.json", {"values": []})
    stage4.stage3.stage2.stage1.js(stage4.DP / "data/space_editor/tags/function/after_teleport.json", {"values": []})
    insert_before(F / "load.mcfunction", "function space_editor:pair/cancel", [
        "scoreboard objectives add se.tp_lock dummy", "scoreboard objectives add se.tp_cd dummy",
        "scoreboard objectives add se.instance dummy",
    ])
    append(F / "tick.mcfunction", ["function space_editor:teleport/tick"])
    fn("teleport/tick", [
        "scoreboard players add @a se.tp_lock 0", "scoreboard players add @a se.tp_cd 0",
        "scoreboard players add @a se.instance 0",
        "scoreboard players remove @a[scores={se.tp_cd=1..}] se.tp_cd 1",
        f"data modify {R} playerSnapshots set value []", f"data modify {R} spaceLinkContacts set value []",
        f"data modify {R} transfers set value []",
        "execute as @a at @s run function space_editor:teleport/snapshot",
        f"execute if data {D} {{editMode:1b}} run return 0",
        "execute as @a[gamemode=!spectator] at @s run function space_editor:link/player",
        "function #space_editor:before_teleport",
        "execute as @a[gamemode=!spectator] at @s run function space_editor:teleport/player",
        "function #space_editor:after_teleport",
    ])
    fn("teleport/snapshot", [
        f'data modify {R} snapshot set value {{uuid:[I;0,0,0,0],point:[0d,0d,0d],rotation:[0f,0f],instanceId:0}}',
        f'data modify {R} snapshot.uuid set from entity @s UUID',
        f'data modify {R} snapshot.point set from entity @s Pos',
        f'data modify {R} snapshot.rotation set from entity @s Rotation',
        f'execute store result {R} snapshot.instanceId int 1 run scoreboard players get @s se.instance',
        f'data modify {R} snapshot.dimension set from entity @s Dimension',
        f'data modify {R} playerSnapshots append from {R} snapshot',
    ])
    # Player Dimension is present in saved entity NBT. Keep a vanilla fallback
    # for fake players used by the test harness and for the editing MVP.
    insert_before(F / "teleport/snapshot.mcfunction", "data modify storage space_editor:runtime playerSnapshots", [
        *[f'execute if dimension minecraft:{dim} run data modify {R} snapshot.dimension set value "minecraft:{dim}"' for dim in ("overworld", "the_nether", "the_end")],
    ])
    fn("teleport/read_snapshot", [
        f'data modify {R} playerLookup.uuid set from entity @s UUID', f'data remove {R} tpPlayer',
        f'function space_editor:teleport/find_snapshot with {R} playerLookup',
        *[line for i, axis in enumerate("xyz") for line in read_fixed(f"tpPlayer.point[{i}]", f"#sp{axis}")],
    ])
    fn("teleport/find_snapshot", [f'$data modify {R} tpPlayer set from {R} playerSnapshots[{{uuid:$(uuid)}}]'])
    contains = ["scoreboard players set #inside se.v 0", '$execute unless dimension $(dimension) run return 0']
    for axis in "xyz":
        contains += [f'execute store result score #bound se.v run data get {R} spatialRegion.{axis}1m 2',
                     f'execute if score #sp{axis} se.v < #bound se.v run return 0',
                     f'execute store result score #bound se.v run data get {R} spatialRegion.{axis}2m 2',
                     f'execute if score #sp{axis} se.v >= #bound se.v run return 0']
    contains += ["scoreboard players set #inside se.v 1"]
    fn("mapping/contains", contains)
    fn("teleport/player", [
        f"execute if data {D} {{editMode:1b}} run return 0",
        'execute if entity @s[tag=space_editor.editing] run return 0',
        'execute if entity @s[gamemode=spectator] run return 0',
        'execute unless entity @s[nbt={DeathTime:0s}] run return 0',
        "function space_editor:teleport/read_snapshot",
        f"execute unless data {R} tpPlayer.point run return 0",
        "scoreboard players set #still_locked se.v 0", f"data remove {R} tpHit",
        f"data modify {R} tpQueue set from {D} regions",
        f"execute if data {R} tpQueue[0] run function space_editor:teleport/scan",
        "execute if score #still_locked se.v matches 0 run scoreboard players set @s se.tp_lock 0",
        "execute if score @s se.tp_lock matches 1.. run return 0",
        "execute if score @s se.tp_cd matches 1.. run return 0",
        f"execute unless data {R} tpHit run return 0",
        f"function space_editor:teleport/resolve with {R} tpHit",
    ])
    fn("teleport/scan", [
        f"data modify {R} spatialRegion set from {R} tpQueue[0]",
        f'execute if data {R} spatialRegion{{kind:"teleport"}} run function space_editor:teleport/check',
        f"data remove {R} tpQueue[0]",
        f"execute if data {R} tpQueue[0] run function space_editor:teleport/scan",
    ])
    fn("teleport/check", [
        f"function space_editor:mapping/contains with {R} spatialRegion",
        "execute unless score #inside se.v matches 1 run return 0",
        f"execute store result score #tp_pair se.v run data get {R} spatialRegion.pairId 1",
        "execute if score @s se.tp_lock = #tp_pair se.v run scoreboard players set #still_locked se.v 1",
        f"execute unless data {R} tpHit run data modify {R} tpHit set from {R} spatialRegion",
    ])
    fn("teleport/resolve", [
        f"data remove {R} tpTarget", f"data remove {R} tpPair",
        f'$data modify {R} tpTarget set from {D} regions[{{id:$(partnerId)}}]',
        f'$data modify {R} tpPair set from {D} regionPairs[{{id:$(pairId),kind:"teleport"}}]',
        f"execute unless data {R} tpTarget.id run return 0", f"execute unless data {R} tpPair.id run return 0",
        f'execute if data {R} tpPair{{direction:"one_way"}} if data {R} tpHit{{side:"B"}} run return 0',
        f'data modify {R} map set value {{}}',
        f'data modify {R} map.source set from {R} tpHit', f'data modify {R} map.target set from {R} tpTarget',
        f'data modify {R} map.point set from {R} tpPlayer.point',
        f'data modify {R} map.yaw set from {R} tpPlayer.rotation[0]', f'data modify {R} map.pitch set from {R} tpPlayer.rotation[1]',
        "function space_editor:mapping/position",
        "scoreboard players set #tp_safe se.v 0",
        f"function space_editor:teleport/check_destination with {R} map.result",
        "execute unless score #tp_safe se.v matches 1 run return 0",
        "scoreboard players set #tp_success se.v 0",
        f"function space_editor:teleport/perform with {R} map.result",
        "execute unless score #tp_success se.v matches 1 run return 0",
        f"execute store result score @s se.tp_lock run data get {R} tpPair.id 1",
        f"execute store result score @s se.tp_cd run data get {R} tpPair.cooldownTicks 1",
        f'data modify {R} transfer set from {R} tpPlayer',
        f'data modify {R} transfer.pairId set from {R} tpPair.id',
        f'data modify {R} transfer.sourceRegionId set from {R} tpHit.id',
        f'data modify {R} transfer.targetRegionId set from {R} tpTarget.id',
        f'data modify {R} transfer.sourceRoomId set from {R} tpHit.roomId',
        f'data modify {R} transfer.targetRoomId set from {R} tpTarget.roomId',
        f'data modify {R} transfer.destination set from {R} map.result',
        f'data modify {R} transfers append from {R} transfer',
    ])
    # Conservative upright body envelope. No terrain clearing or automatic
    # force-loading; pending arrival is retried while the source is occupied.
    safety = []
    for x in (-0.3, 0.299999):
        for z in (-0.3, 0.299999):
            for y in (0, 0.9, 1.799999):
                safety += [f'$execute in $(dimension) positioned $(x) $(y) $(z) unless loaded ~{x} ~{y} ~{z} run return 0',
                           f'$execute in $(dimension) positioned $(x) $(y) $(z) unless block ~{x} ~{y} ~{z} #space_editor:ray_pass run return 0']
    fn("teleport/check_destination", safety + ["scoreboard players set #tp_safe se.v 1"])
    fn("teleport/perform", ['$execute in $(dimension) store success score #tp_success se.v run tp @s $(x) $(y) $(z) $(yaw) $(pitch)'])
    fn("link/player", [
        'execute unless entity @s[nbt={DeathTime:0s}] run return 0',
        "function space_editor:teleport/read_snapshot",
        f"data modify {R} linkQueue set from {D} regions",
        f"execute if data {R} linkQueue[0] run function space_editor:link/scan",
    ])
    fn("link/scan", [
        f"data modify {R} spatialRegion set from {R} linkQueue[0]",
        f'execute if data {R} spatialRegion{{kind:"space_link"}} run function space_editor:link/check',
        f"data remove {R} linkQueue[0]",
        f"execute if data {R} linkQueue[0] run function space_editor:link/scan",
    ])
    fn("link/check", [
        f"function space_editor:mapping/contains with {R} spatialRegion",
        "execute unless score #inside se.v matches 1 run return 0",
        f"function space_editor:link/contact with {R} spatialRegion",
    ])
    fn("link/contact", [
        f'data modify {R} map set value {{}}',
        f'data modify {R} map.source set from {R} spatialRegion',
        f'$data modify {R} map.target set from {D} regions[{{id:$(partnerId)}}]',
        f'execute unless data {R} map.target.id run return 0',
        f'data modify {R} map.point set from {R} tpPlayer.point',
        f'data modify {R} map.yaw set from {R} tpPlayer.rotation[0]', f'data modify {R} map.pitch set from {R} tpPlayer.rotation[1]',
        'function space_editor:mapping/position',
        f'data modify {R} linkContact set from {R} tpPlayer',
        f'$data modify {R} linkContact.pairId set value $(pairId)',
        f'$data modify {R} linkContact.sourceRegionId set value $(id)',
        f'$data modify {R} linkContact.targetRegionId set value $(partnerId)',
        f'data modify {R} linkContact.sourceRoomId set from {R} spatialRegion.roomId',
        f'data modify {R} linkContact.targetRoomId set from {R} map.target.roomId',
        f'data modify {R} linkContact.destination set from {R} map.result',
        f'data modify {R} spaceLinkContacts append from {R} linkContact',
    ])


def generate_link_contract() -> None:
    insert_before(F / "load.mcfunction", "function space_editor:pair/cancel", [
        f"execute unless data {D} linkGroups run data modify {D} linkGroups set value []",
        "function space_editor:link/validate_groups",
    ])
    fn("pair/configure", [
        '$function space_editor:pair/load {pairId:$(id)}',
        f"execute unless data {R} editA.id run return 0", f"execute unless data {R} editB.id run return 0",
        "function space_editor:pair/snapshot",
        f'$data modify {R} pair.groupId set value $(groupId)',
        f'$data modify {R} pair.roomA set value "$(roomA)"', f'$data modify {R} pair.roomB set value "$(roomB)"',
        f'$data modify {R} pair.direction set value "$(direction)"', f'$data modify {R} pair.cooldownTicks set value $(cooldownTicks)',
        f"execute store result score #config_group se.v run data get {R} pair.groupId 1",
        f"execute store result score #config_cool se.v run data get {R} pair.cooldownTicks 1",
        "execute unless score #config_group se.v matches 0.. run return 0",
        "execute unless score #config_cool se.v matches 0..1200 run return 0",
        f'execute unless data {R} pair{{direction:"both"}} unless data {R} pair{{direction:"one_way"}} run return 0',
        f'$execute if score #config_group se.v matches 1.. if data {D} linkGroups[{{id:$(groupId)}}] unless data {D} linkGroups[{{id:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}}] run return run ' + message("GroupのRoom対応が一致しません。", "red"),
        f'$execute if score #config_group se.v matches 1.. unless data {D} linkGroups[{{id:$(groupId)}}] run data modify {D} linkGroups append value {{id:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}}',
        f'data modify {R} editA.roomId set from {R} pair.roomA', f'data modify {R} editB.roomId set from {R} pair.roomB',
        f'data modify {R} pairOperation set value "configure"', "function space_editor:pair/commit",
        "function space_editor:link/clean_groups",
    ])
    fn("proxy_existence/set_room", [
        f'$execute unless data {D} regions[{{id:$(id),kind:"proxy_existence"}}] run return 0',
        f'$data modify {D} regions[{{id:$(id)}}].roomId set value "$(roomId)"',
    ])
    append(F / "pair/commit.mcfunction", ["function space_editor:link/validate_groups"])
    append(F / "pair/delete.mcfunction", ["function space_editor:link/clean_groups", "function space_editor:link/validate_groups"])
    fn("link/clean_groups", [
        f"data modify {R} cleanGroups set from {D} linkGroups",
        f"execute if data {R} cleanGroups[0] run function space_editor:link/clean_next",
    ])
    fn("link/clean_next", [
        f"function space_editor:link/clean_one with {R} cleanGroups[0]",
        f"data remove {R} cleanGroups[0]", f"execute if data {R} cleanGroups[0] run function space_editor:link/clean_next",
    ])
    fn("link/clean_one", [f'$execute unless data {D} regionPairs[{{groupId:$(id)}}] run data remove {D} linkGroups[{{id:$(id)}}]'])
    fn("link/validate_groups", [
        f"data modify {R} linkWarnings set value []", f"data modify {R} validationPairs set from {D} regionPairs",
        f"execute if data {R} validationPairs[0] run function space_editor:link/validate_next",
        f"execute if data {R} linkWarnings[0] run " + message("TP / SpaceLinkの範囲または変換に不整合があります。/function space_editor:link/status で確認してください。", "yellow"),
    ])
    fn("link/validate_next", [
        f"data modify {R} validationPair set from {R} validationPairs[0]",
        f'execute if data {R} validationPair{{kind:"teleport"}} unless data {R} validationPair{{groupId:0}} run function space_editor:link/validate_pair with {R} validationPair',
        f"data remove {R} validationPairs[0]", f"execute if data {R} validationPairs[0] run function space_editor:link/validate_next",
    ])
    fn("link/validate_pair", [
        # Filter a queue so several peers are supported.
        f"data modify {R} comparePeers set from {D} regionPairs",
        f"execute if data {R} comparePeers[0] run function space_editor:link/compare_next with {R} validationPair",
    ])
    fn("link/compare_next", [
        f'data modify {R} peerPair set from {R} comparePeers[0]',
        f'$execute if data {R} peerPair{{groupId:$(groupId),kind:"space_link"}} run function space_editor:link/compare',
        f'data remove {R} comparePeers[0]', f'execute if data {R} comparePeers[0] run function space_editor:link/compare_next with {R} validationPair',
    ])
    for record, prefix in (("validationPair", "tp"), ("peerPair", "sl")):
        fn(f"link/load_{prefix}", [
            *[f'$data modify {R} {prefix}{side} set from {D} regions[{{id:$({side.lower()})}}]' for side in ("A", "B")],
        ])
    compare = [f"function space_editor:link/load_tp with {R} validationPair",
               f"function space_editor:link/load_sl with {R} peerPair",
               "scoreboard players set #link_mismatch se.v 0"]
    for prefix in ("tp", "sl"):
        compare += [f'data modify {R} map set value {{point:[0d,0d,0d],vector:[1d,2d,3d]}}',
                    f'data modify {R} map.source set from {R} {prefix}A', f'data modify {R} map.target set from {R} {prefix}B',
                    "function space_editor:mapping/position"]
        if prefix == "tp":
            compare += [f'data modify {R} expectedMapping set from {R} map.result']
        else:
            compare += [f'execute store success score #link_mismatch se.v run data modify {R} expectedMapping set from {R} map.result']
    for side in ("A", "B"):
        compare += [f'data modify {R} compareDimension set from {R} tp{side}.dimension',
                    f'execute store success score #dimension_diff se.v run data modify {R} compareDimension set from {R} sl{side}.dimension',
                    'execute if score #dimension_diff se.v matches 1 run scoreboard players set #link_mismatch se.v 1']
        for axis in "xyz":
            for edge, op in ((1, "<"), (2, ">")):
                compare += [f'execute store result score #inner se.v run data get {R} tp{side}.{axis}{edge}m 1',
                            f'execute store result score #outer se.v run data get {R} sl{side}.{axis}{edge}m 1',
                            f'execute if score #inner se.v {op} #outer se.v run scoreboard players set #link_mismatch se.v 1']
    compare += [f'data modify {R} linkWarning set value {{reason:"transform_or_containment_mismatch"}}',
                f'data modify {R} linkWarning.teleportPairId set from {R} validationPair.id',
                f'data modify {R} linkWarning.spaceLinkPairId set from {R} peerPair.id',
                f'execute if score #link_mismatch se.v matches 1 run data modify {R} linkWarnings append from {R} linkWarning']
    fn("link/compare", compare)
    fn("link/status", [
        "function space_editor:link/validate_groups",
        'tellraw @s [{text:"Link warnings: ",color:"yellow"},{nbt:"linkWarnings",storage:"space_editor:runtime"}]',
    ])
    append(F / "load.mcfunction", [message("第5段階: ペアRegion編集・TP。/function space_editor:pair/help", target="@a")])
    append(F / "status.mcfunction", ['tellraw @s [{text:"Region pairs: ",color:"aqua"},{nbt:"regionPairs",storage:"space_editor:document"}]'])
    append(F / "menu.mcfunction", [message("ペアRegion: TP / SpaceLink接続棒。操作: /function space_editor:pair/help")])
    fn("pair/help", [
        message("接続棒で元Regionを選択 → 視線で相手を配置 → 右クリックで確定。"),
        message("Shift+右クリック: 作業開始方向から左右で90度回転、上下でFlipY。配置後も接続棒でA/Bを選択して編集。"),
        message("面伸縮は対応ローカル面が連動。移動・回転・反転は選択側のみ。削除はペア両方。"),
        message("TP開始: /function space_editor:play。SpaceLinkは本人を転送しません。"),
        message("Proxy存在範囲棒: 単独Regionを存在範囲として登録。模倣生成は06で追加します。"),
    ])


def generate_region_edit_fix() -> None:
    # A ray's sampled coordinates are monotone on each axis. Binary-search
    # each AABB's first occupied sample instead of scanning every AABB at all
    # 513 points. Keep milliblock comparisons, list-order ties, and the existing
    # per-sample Paste/special-block priority and nearest-face implementation.
    ray = (F / "region/ray.mcfunction").read_text(encoding="utf-8")
    ray = ray.replace(
        f"data modify {R} candidates set from {D} regions\n"
        f"execute if data {R} candidates[0] run function space_editor:region/check_next",
        "execute if score #region_ray se.v = #ray_best se.v run function space_editor:region/ray_hit",
    ).replace("run function space_editor:region/ray\n", "run function space_editor:region/ray_step\n")
    fn("region/ray_step", ray.splitlines())
    fn("region/ray", [
        f"data remove {R} rayHit",
        "scoreboard players set #ray_best se.v 513",
        'summon minecraft:marker ~ ~ ~ {Tags:["space_editor.ray_probe"]}',
        f"data modify {R} rayPos set from entity @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] Pos",
        *[f"execute store result score #ray_origin_{axis} se.v run data get {R} rayPos[{i}] 1000" for i, axis in enumerate("xyz")],
        "execute positioned ^ ^ ^12.8 run tp @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] ~ ~ ~",
        f"data modify {R} rayPos set from entity @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] Pos",
        *[line for i, axis in enumerate("xyz") for line in (
            f"execute store result score #ray_end_{axis} se.v run data get {R} rayPos[{i}] 1000",
            f"scoreboard players set #ray_sign_{axis} se.v 1",
            f"execute if score #ray_end_{axis} se.v < #ray_origin_{axis} se.v run scoreboard players set #ray_sign_{axis} se.v -1",
        )],
        f"data modify {R} rayQueue set from {D} regions",
        f"execute if data {R} rayQueue[0] run function space_editor:region/ray_next",
        "kill @e[type=minecraft:marker,tag=space_editor.ray_probe]",
        "function space_editor:region/ray_step",
    ])
    fn("region/ray_next", [
        f"data modify {R} candidate set from {R} rayQueue[0]",
        f"function space_editor:region/ray_check with {R} candidate",
        f"data remove {R} rayQueue[0]",
        # An origin hit cannot be beaten, including by a later overlapping box.
        f"execute if score #ray_best se.v matches 1.. if data {R} rayQueue[0] run function space_editor:region/ray_next",
    ])
    fn("region/ray_check", [
        '$execute unless dimension $(dimension) run return 0',
        f'execute if data {R} {{activeTool:"pair_select"}} if data {R} candidate.kind run function space_editor:pair/filter',
        f'execute if data {R} {{activeTool:"pair_select"}} if data {R} candidate.kind if score #pair_filter se.v matches 0 run return 0',
        *[f"execute store result score #ray_{edge}_{axis} se.v run data get {R} candidate.{axis}{number}m 1"
          for axis in "xyz" for edge, number in (("lo", 1), ("hi", 2))],
        "scoreboard players set #ray_low se.v 0",
        "scoreboard players operation #ray_high se.v = #ray_best se.v",
        "scoreboard players remove #ray_high se.v 1",
        "scoreboard players set #ray_found se.v 513",
        "function space_editor:region/ray_search",
        f"execute if score #ray_found se.v < #ray_best se.v run data modify {R} rayHit set from {R} candidate",
        "scoreboard players operation #ray_best se.v < #ray_found se.v",
    ])
    fn("region/ray_search", [
        "scoreboard players operation #ray_mid se.v = #ray_low se.v",
        "scoreboard players operation #ray_mid se.v += #ray_high se.v",
        "scoreboard players operation #ray_mid se.v /= #two se.v",
        f"execute store result {R} rayDistance double 0.025 run scoreboard players get #ray_mid se.v",
        f"function space_editor:region/ray_probe with {R}",
        "scoreboard players set #ray_before se.v 0",
        "scoreboard players set #ray_after se.v 0",
        *[line for axis in "xyz" for line in (
            f"execute if score #p{axis} se.v < #ray_lo_{axis} se.v if score #ray_sign_{axis} se.v matches 1 run scoreboard players set #ray_before se.v 1",
            f"execute if score #p{axis} se.v >= #ray_hi_{axis} se.v if score #ray_sign_{axis} se.v matches -1 run scoreboard players set #ray_before se.v 1",
            f"execute if score #p{axis} se.v < #ray_lo_{axis} se.v if score #ray_sign_{axis} se.v matches -1 run scoreboard players set #ray_after se.v 1",
            f"execute if score #p{axis} se.v >= #ray_hi_{axis} se.v if score #ray_sign_{axis} se.v matches 1 run scoreboard players set #ray_after se.v 1",
        )],
        # Opposing constraints at one point mean the three slab intervals
        # cannot overlap. Constant axes obey the same monotone comparisons.
        "execute if score #ray_before se.v matches 1 if score #ray_after se.v matches 1 run return 0",
        "execute if score #ray_before se.v matches 0 if score #ray_after se.v matches 0 run scoreboard players operation #ray_found se.v = #ray_mid se.v",
        "execute if score #ray_before se.v matches 1 run scoreboard players operation #ray_low se.v = #ray_mid se.v",
        "execute if score #ray_before se.v matches 1 run scoreboard players add #ray_low se.v 1",
        "execute if score #ray_before se.v matches 0 run scoreboard players operation #ray_high se.v = #ray_mid se.v",
        "execute if score #ray_before se.v matches 0 run scoreboard players remove #ray_high se.v 1",
        "execute if score #ray_low se.v <= #ray_high se.v run function space_editor:region/ray_search",
    ])
    fn("region/ray_probe", [
        '$execute positioned ^ ^ ^$(rayDistance) run tp @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] ~ ~ ~',
        f"data modify {R} rayPos set from entity @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] Pos",
        *[f"execute store result score #p{axis} se.v run data get {R} rayPos[{i}] 1000" for i, axis in enumerate("xyz")],
    ])
    fn("region/ray_hit", [f"data modify {R} hit set from {R} rayHit", "function space_editor:region/face"])

    # All persistent Region decorations need the existing se.id association;
    # pair labels/directions previously had none because resync killed all.
    for name in ("pair/spawn_directions", "pair/preview_existence"):
        path = F / f"{name}.mcfunction"
        text = path.read_text(encoding="utf-8").replace('"space_editor.label"', '"space_editor.label","space_editor.new"')
        write(path, text)
        append(path, [
            '$execute in $(dimension) run scoreboard players set @e[tag=space_editor.new] se.id $(id)',
            '$execute in $(dimension) run tag @e[tag=space_editor.new] remove space_editor.new',
        ])
    append(F / "preview/highlight.mcfunction", [f'$data modify {R} highlightedRegion set value {{id:$(id),dimension:"$(dimension)"}}'])
    fn("preview/clear_highlight", [
        '$execute in $(dimension) as @e[tag=space_editor.region,scores={se.id=$(id)}] run data merge entity @s {block_state:{Name:"' + stage4.DISPLAY_BLOCKS["selection"] + '"}}',
    ])
    fn("preview/update_hit", [
        f"execute if data {R} highlightedRegion run function space_editor:preview/clear_highlight with {R} highlightedRegion",
        f"function space_editor:preview/update_region with {R} hit",
        f"execute if data {D} {{editMode:1b}} if data {D} settings{{regionsVisible:1b}} run function space_editor:preview/highlight with {R} hit",
    ])
    fn("preview/update_region", [
        # Restrict by both type tag and ID: Mask IDs are a separate sequence.
        *[f'$execute in minecraft:{dim} run kill @e[tag=space_editor.{tag},scores={{se.id=$(id)}}]'
          for dim in ("overworld", "the_nether", "the_end") for tag in ("region", "label")],
        f"data remove {R} renderRegion",
        f'$data modify {R} renderRegion set from {D} regions[{{id:$(id)}}]',
        f"execute if data {R} renderRegion.id if data {D} {{editMode:1b}} if data {D} settings{{regionsVisible:1b}} run function space_editor:preview/prepare",
        f"execute if data {R} renderRegion.id if data {D} {{editMode:1b}} if data {D} settings{{regionsVisible:1b}} run function space_editor:preview/spawn with {R} renderRegion",
        f"data remove {R} currentMask",
        f'$data modify {R} currentMask set from {D} masks[{{regionId:$(id)}}]',
        f"execute if data {R} currentMask.id run function space_editor:mask/update_region with {R} currentMask",
    ])
    fn("mask/update_region", [
        "function space_editor:mask/prepare",
        *[f'$execute in minecraft:{dim} run kill @e[tag=space_editor.{tag},scores={{se.id=$(id)}}]'
          for dim in ("overworld", "the_nether", "the_end") for tag in ("mask_body", "mask_guide")],
        f"execute if score #mask_valid se.v matches 1 run function space_editor:mask/spawn with {R} maskRender",
    ])
    path = F / "region/save_resize.mcfunction"
    write(path, path.read_text(encoding="utf-8").replace("function space_editor:preview/resync", "function space_editor:preview/update_hit"))
    path = F / "pair/commit.mcfunction"
    write(path, path.read_text(encoding="utf-8").replace("function space_editor:preview/resync", "function space_editor:preview/update_pair"))
    fn("preview/update_pair", [
        # Pose's hit still contains the old bounds; reload the committed record.
        f"function space_editor:preview/reload_hit with {R} hit",
        "function space_editor:preview/update_hit",
        f'execute unless data {R} {{pairOperation:"move"}} unless data {R} {{pairOperation:"pose"}} run function space_editor:preview/update_partner with {R} hit',
    ])
    fn("preview/reload_hit", [f'$data modify {R} hit set from {D} regions[{{id:$(id)}}]'])
    fn("preview/update_partner", ['$function space_editor:preview/update_region {id:$(partnerId)}'])


def main() -> None:
    stage4.main()
    generate_transform()
    generate_pairs()
    generate_teleport()
    generate_link_contract()
    generate_region_edit_fix()
    import build_space_link_groups
    build_space_link_groups.generate(__import__(__name__))
    import build_space_editor_stage6_1
    build_space_editor_stage6_1.generate()
    import build_space_editor_stage6
    build_space_editor_stage6.generate(__import__(__name__))
    print(f"Generated stage-5 Space Editor: {len(list(F.rglob('*.mcfunction')))} functions")


if __name__ == "__main__":
    main()
