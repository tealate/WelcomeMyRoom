"""Stage 05: additive paired Regions and teleport, layered on Stage 04."""
from __future__ import annotations

import build_space_editor_stage4 as stage4

F = stage4.F
fn = stage4.fn
write = stage4.write
append = stage4.append
insert_before = stage4.insert_before
message = stage4.message
dimensions = stage4.dimensions
R = "storage space_editor:runtime"
D = "storage space_editor:document"


def basis(rotation: int, flip: int) -> tuple[tuple[int, int], ...]:
    """World components (local axis, sign); positive yaw matches Minecraft."""
    horizontal = {0: ((0, 1), (2, 1)), 90: ((2, -1), (0, 1)),
                  180: ((0, -1), (2, -1)), 270: ((2, 1), (0, -1))}
    x, z = horizontal[rotation]
    return x, (1, -1 if flip else 1), z


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
        lines += [f"execute store result score #map_p{axis} se.v run data get {R} map.point[{i}] 2000",
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
        *[f"execute store result score #map_p{axis} se.v run data get {R} map.vector[{i}] 2000" for i, axis in enumerate("xyz")],
        "function space_editor:mapping/vector_scores",
        *[f"execute store result {R} map.result.vector[{i}] double 0.0005 run scoreboard players get #map_o{axis} se.v" for i, axis in enumerate("xyz")],
    ])
    fn("mapping/look", [
        f"execute store result score #map_yaw se.v run data get {R} map.yaw 1000",
        f"execute store result score #map_pitch se.v run data get {R} map.pitch 1000",
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


def main() -> None:
    stage4.main()
    generate_transform()
    print(f"Generated stage-5 Space Editor: {len(list(F.rglob('*.mcfunction')))} functions")


if __name__ == "__main__":
    main()
