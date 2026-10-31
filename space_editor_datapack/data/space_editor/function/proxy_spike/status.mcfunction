function space_editor:proxy_spike/select
tellraw @s [{text:"[06-1] owner="},{score:{name:"@s",objective:"sp.owner"}},{text:" follow="},{score:{name:"@s",objective:"sp.follow"}},{text:" flip="},{score:{name:"@s",objective:"sp.flip"}},{text:" name(0..4)="},{score:{name:"@s",objective:"sp.name"}}]
tellraw @s [{text:"offset / flip Y / label height (milliblocks): "},{score:{name:"@s",objective:"sp.x"}},{text:" / "},{score:{name:"@s",objective:"sp.y"}},{text:" / "},{score:{name:"@s",objective:"sp.z"}},{text:" / "},{score:{name:"@s",objective:"sp.fy"}},{text:" / "},{score:{name:"@s",objective:"sp.normal"}},{text:" / "},{score:{name:"@s",objective:"sp.inverted"}},{text:" / "}]
data get entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1]
