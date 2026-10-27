// Runtime checks for Space Editor phase 3 on Minecraft Java 26.1.
import java.nio.file.*;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.nbt.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.properties.*;

public class SpaceEditorStage3GameTest {
    static GameTestHelper helper;
    static CommandSourceStack source;
    static net.minecraft.server.level.ServerPlayer player;
    static boolean finished;
    static int step, waitTicks, pasteIndex, stairPasteIndex;
    static final int AX=20000064, AY=-63, AZ=20000000;
    static final int TY=80;
    static final int[] ROT={0,90,180,270,0,90,180,270};
    static final int[] FLIP={0,0,0,0,1,1,1,1};
    static final String[] CUBE={"minecraft:stone","minecraft:dirt","minecraft:oak_planks","minecraft:bricks","minecraft:gold_block","minecraft:diamond_block","minecraft:emerald_block","minecraft:redstone_block"};
    static final StairsShape[] STAIR_SHAPES={StairsShape.STRAIGHT,StairsShape.INNER_LEFT,StairsShape.INNER_RIGHT,StairsShape.OUTER_LEFT,StairsShape.OUTER_RIGHT};
    static final Identifier DOCUMENT=Identifier.parse("space_editor:document");
    static final Identifier RUNTIME=Identifier.parse("space_editor:runtime");

    static CompoundTag document(){return helper.getLevel().getServer().getCommandStorage().get(DOCUMENT);}
    static CompoundTag runtime(){return helper.getLevel().getServer().getCommandStorage().get(RUNTIME);}
    static void cmd(String c){helper.getLevel().getServer().getCommands().performPrefixedCommand(source,c);}
    static void pcmd(String c){helper.getLevel().getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS),c);}
    static int score(String objective){var board=helper.getLevel().getScoreboard();return board.getOrCreatePlayerScore(player,board.getObjective(objective)).get();}
    static void check(boolean ok,String message){if(!ok)throw new AssertionError(message+" DOCUMENT="+document()+" RUNTIME="+runtime());}
    static String jobState(){return document().getCompoundOrEmpty("job").getStringOr("state","");}

    static void startPaste(int id,int rotation,int flip,int x,int y,int z){
        cmd("data modify storage space_editor:runtime targetDimension set value \"minecraft:overworld\"");
        cmd("data modify storage space_editor:runtime targetPos set value [I;"+x+","+y+","+z+"]");
        cmd("data modify storage space_editor:runtime lookup set value {id:"+id+",owner0:0,owner1:0,owner2:0,owner3:0}");
        cmd("data modify storage space_editor:runtime pasteTransform set value {rotation:"+rotation+",flipY:"+flip+"b}");
        pcmd("function space_editor:paste/start {id:"+id+"}");
        check(jobState().equals("running"),"paste job started id="+id+" rot="+rotation+" flip="+flip);
    }

    static void tickJob(){if(jobState().equals("running"))cmd("function space_editor:job/tick");}

    static BlockPos mapped(int originX,int originY,int originZ,int x,int y,int z,int rotation,int flip){
        int tx=x,tz=z;
        if(rotation==90){tx=1-z;tz=x;}
        else if(rotation==180){tx=1-x;tz=1-z;}
        else if(rotation==270){tx=z;tz=1-x;}
        int ty=flip==1?1-y:y;
        return new BlockPos(originX+tx,originY+ty,originZ+tz);
    }

    static void verifyCube(int index){
        int ox=index*5, oz=0, rotation=ROT[index], flip=FLIP[index];
        for(int y=0;y<2;y++)for(int z=0;z<2;z++)for(int x=0;x<2;x++){
            Block expected=BuiltInRegistries.BLOCK.getValue(Identifier.parse(CUBE[x+2*(z+2*y)]));
            check(helper.getLevel().getBlockState(mapped(ox,TY,oz,x,y,z,rotation,flip)).is(expected),
                "cube coordinate map state="+index+" source="+x+","+y+","+z);
        }
        var job=document().getCompoundOrEmpty("job");
        check(job.getIntOr("rotation",-1)==rotation && job.getBooleanOr("flipY",false)==(flip==1),"job persisted transform");
    }

    static void verifyStairShapes(int index){
        int ox=70+index*7, oz=0, rotation=ROT[index];
        Direction expectedFacing=new Direction[]{Direction.NORTH,Direction.EAST,Direction.SOUTH,Direction.WEST}[index];
        for(int x=0;x<STAIR_SHAPES.length;x++){
            int tx=x,tz=0;
            if(rotation==90){tx=0;tz=x;}
            else if(rotation==180){tx=STAIR_SHAPES.length-1-x;}
            else if(rotation==270){tx=0;tz=STAIR_SHAPES.length-1-x;}
            var stair=helper.getLevel().getBlockState(new BlockPos(ox+tx,TY,oz+tz));
            check(stair.is(Blocks.OAK_STAIRS)
                    && stair.getValue(BlockStateProperties.HORIZONTAL_FACING)==expectedFacing
                    && stair.getValue(BlockStateProperties.STAIRS_SHAPE)==STAIR_SHAPES[x],
                "stair shape preserved rot="+rotation+" sourceIndex="+x+" actual="+stair);
        }
    }

    static void verifyPreviewAndMoveTools(){
        cmd("data modify storage space_editor:runtime pastePending set value {targetDimension:\"minecraft:overworld\",x:100,y:80,z:100,sx:2,sy:3,sz:4}");
        cmd("scoreboard players set #px se.v 100000");
        cmd("scoreboard players set #py se.v 81500");
        cmd("scoreboard players set #pz se.v 102000");
        cmd("execute store result storage space_editor:runtime testPasteHit int 1 run function space_editor:paste/check_preview_hit with storage space_editor:runtime pastePending");
        check(runtime().getIntOr("testPasteHit",0)==1 && runtime().getIntOr("hitFace",-1)==0,"paste preview AABB hit and face detected");
        cmd("data modify storage space_editor:runtime activeTool set value \"delete\"");
        pcmd("function space_editor:paste/apply_preview_hit");
        check(!runtime().contains("pastePending"),"delete tool cancelled pending paste preview");

        cmd("data modify storage space_editor:runtime pastePending set value {targetDimension:\"minecraft:overworld\",x:100,y:80,z:100,sx:2,sy:3,sz:4}");
        cmd("data modify storage space_editor:runtime activeTool set value \"move\"");
        cmd("data modify storage space_editor:runtime hitFace set value 1");
        pcmd("function space_editor:paste/apply_preview_hit");
        check(runtime().getCompoundOrEmpty("pastePending").getIntOr("x",0)==101,"move tool shifted paste preview one block toward clicked face");

        cmd("data modify storage space_editor:document regions set value [{id:99,idText:\"99\",dimension:\"minecraft:overworld\",min:[0.0d,80.0d,0.0d],maxExclusive:[2.0d,82.0d,2.0d],x1:0.0d,x2:2.0d,y1:80.0d,y2:82.0d,z1:0.0d,z2:2.0d,sx:2.0d,sy:2.0d,sz:2.0d,x1m:0,x2m:2000,y1m:80000,y2m:82000,z1m:0,z2m:2000,sxm:2000,sym:2000,szm:2000}]");
        cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
        cmd("data modify storage space_editor:runtime hitFace set value 5");
        pcmd("function space_editor:region/move");
        var moved=document().getListOrEmpty("regions").getCompoundOrEmpty(0);
        check(moved.getIntOr("z1m",-1)==1000 && moved.getIntOr("z2m",-1)==3000 && moved.getIntOr("szm",-1)==2000,"move tool shifted persisted region exactly one block without resizing");
    }

    static void setup(GameTestHelper h){
        helper=h; source=h.getLevel().getServer().createCommandSourceStack(); finished=false; step=0; waitTicks=0; pasteIndex=0; stairPasteIndex=0;
        cmd("function space_editor:load");
        cmd("data modify storage space_editor:document templates set value []");
        cmd("data modify storage space_editor:document actions set value []");
        cmd("data modify storage space_editor:document nextActionId set value 1");
        cmd("forceload add "+AX+" "+AZ+" "+(AX+240)+" "+(AZ+8));
        for(int y=0;y<2;y++)for(int z=0;z<2;z++)for(int x=0;x<2;x++)
            cmd("setblock "+(AX+x)+" "+(AY+y)+" "+(AZ+z)+" "+CUBE[x+2*(z+2*y)]);
        cmd("setblock "+(AX+64)+" "+AY+" "+AZ+" minecraft:oak_stairs[facing=north,half=bottom,shape=straight,waterlogged=false] strict");
        cmd("setblock "+(AX+65)+" "+AY+" "+AZ+" minecraft:oak_slab[type=bottom,waterlogged=false] strict");
        cmd("setblock "+(AX+66)+" "+AY+" "+AZ+" minecraft:oak_fence[north=true,east=false,south=true,west=false,waterlogged=false] strict");
        cmd("setblock "+(AX+96)+" "+AY+" "+AZ+" minecraft:oak_stairs[facing=west,half=bottom,shape=straight,waterlogged=false] strict");
        cmd("setblock "+(AX+97)+" "+AY+" "+AZ+" minecraft:stone_slab[type=bottom,waterlogged=false] strict");
        cmd("setblock "+(AX+128)+" "+AY+" "+AZ+" minecraft:chest[facing=north]");
        cmd("fill "+(AX+160)+" "+AY+" "+AZ+" "+(AX+164)+" "+(AY+2)+" "+(AZ+4)+" minecraft:stone");
        for(int x=0;x<STAIR_SHAPES.length;x++)
            cmd("setblock "+(AX+192+x)+" "+AY+" "+AZ+" minecraft:oak_stairs[facing=north,half=bottom,shape="+STAIR_SHAPES[x].getSerializedName()+",waterlogged=false] strict");
        cmd("setblock "+(AX+224)+" "+AY+" "+AZ+" minecraft:oak_fence[north=true,east=false,south=true,west=false,waterlogged=false] strict");
        cmd("setblock "+(AX+225)+" "+AY+" "+AZ+" minecraft:cobblestone_wall[north=low,east=none,south=tall,west=none,up=true,waterlogged=false] strict");
        cmd("data modify storage space_editor:document templates set value ["+
            "{id:1,version:1,archive:{dimension:\"minecraft:overworld\",x:"+AX+",y:"+AY+",z:"+AZ+"},size:[I;2,2,2]},"+
            "{id:2,version:1,archive:{dimension:\"minecraft:overworld\",x:"+(AX+64)+",y:"+AY+",z:"+AZ+"},size:[I;3,1,1]},"+
            "{id:3,version:1,archive:{dimension:\"minecraft:overworld\",x:"+(AX+96)+",y:"+AY+",z:"+AZ+"},size:[I;2,1,1]},"+
            "{id:4,version:1,archive:{dimension:\"minecraft:overworld\",x:"+(AX+128)+",y:"+AY+",z:"+AZ+"},size:[I;1,1,1]},"+
            "{id:5,version:1,archive:{dimension:\"minecraft:overworld\",x:"+(AX+160)+",y:"+AY+",z:"+AZ+"},size:[I;5,3,5]},"+
            "{id:6,version:1,archive:{dimension:\"minecraft:overworld\",x:"+(AX+192)+",y:"+AY+",z:"+AZ+"},size:[I;5,1,1]},"+
            "{id:7,version:1,archive:{dimension:\"minecraft:overworld\",x:"+(AX+224)+",y:"+AY+",z:"+AZ+"},size:[I;2,1,1]}]");
        player=h.makeMockServerPlayerInLevel(); player.setNoGravity(true); player.setPos(0.5,TY+3,0.5);
        startPaste(1,ROT[0],FLIP[0],0,TY,0);
    }

    static void test(GameTestHelper h){
        setup(h);
        h.onEachTick(() -> {
            if(finished)return;
            try{
                if(step==0){
                    tickJob(); waitTicks++;
                    if(!jobState().equals("running")){
                        verifyCube(pasteIndex); pasteIndex++; waitTicks=0;
                        if(pasteIndex<8) startPaste(1,ROT[pasteIndex],FLIP[pasteIndex],pasteIndex*5,TY,0);
                        else {startPaste(2,90,0,45,TY,0);step=1;}
                    } else if(waitTicks>20)throw new AssertionError("cube transform timeout "+pasteIndex);
                } else if(step==1){
                    tickJob(); waitTicks++;
                    if(!jobState().equals("running")){
                        var stair=helper.getLevel().getBlockState(new BlockPos(45,TY,0));
                        var slab=helper.getLevel().getBlockState(new BlockPos(45,TY,1));
                        var fence=helper.getLevel().getBlockState(new BlockPos(45,TY,2));
                        check(stair.is(Blocks.OAK_STAIRS) && stair.getValue(BlockStateProperties.HORIZONTAL_FACING)==Direction.EAST && stair.getValue(BlockStateProperties.HALF)==Half.BOTTOM && stair.getValue(BlockStateProperties.STAIRS_SHAPE)==StairsShape.STRAIGHT,"stair state rotated actual="+stair);
                        check(slab.is(Blocks.OAK_SLAB) && slab.getValue(BlockStateProperties.SLAB_TYPE)==SlabType.BOTTOM,"slab state preserved");
                        check(fence.is(Blocks.OAK_FENCE) && fence.getValue(BlockStateProperties.EAST) && fence.getValue(BlockStateProperties.WEST),"fence connections rotated");
                        startPaste(3,0,1,50,TY,0);step=2;waitTicks=0;
                    } else if(waitTicks>20)throw new AssertionError("state rotation timeout");
                } else if(step==2){
                    tickJob(); waitTicks++;
                    if(!jobState().equals("running")){
                        var stair=helper.getLevel().getBlockState(new BlockPos(50,TY,0));
                        var slab=helper.getLevel().getBlockState(new BlockPos(51,TY,0));
                        check(stair.getValue(BlockStateProperties.HALF)==Half.TOP,"FlipY toggled stair half");
                        check(slab.getValue(BlockStateProperties.SLAB_TYPE)==SlabType.TOP,"FlipY toggled slab type");
                        cmd("setblock 55 "+TY+" 0 minecraft:gold_block");
                        startPaste(4,90,0,55,TY,0);step=3;waitTicks=0;
                    } else if(waitTicks>20)throw new AssertionError("state flip timeout");
                } else if(step==3){
                    tickJob(); waitTicks++;
                    if(!jobState().equals("running")){
                        var skippedJob=document().getCompoundOrEmpty("job");
                        check(skippedJob.getIntOr("unsupportedBlocks",-1)==1 && skippedJob.getIntOr("skippedBlocks",-1)==1,"unsupported chest counted and skipped");
                        check(helper.getLevel().getBlockState(new BlockPos(55,TY,0)).is(Blocks.GOLD_BLOCK),"unsupported transform preserved destination block");
                        var skippedAction=document().getListOrEmpty("actions").getCompoundOrEmpty(10);
                        check(skippedAction.getIntOr("skippedBlocks",-1)==1,"skip warning persisted in action");
                        startPaste(5,90,0,60,TY,0); step=4; waitTicks=0;
                    } else if(waitTicks>20)throw new AssertionError("unsupported preflight timeout");
                } else if(step==4){
                    var job=document().getCompoundOrEmpty("job");
                    if(waitTicks==0){
                        job=document().getCompoundOrEmpty("job");
                        check(jobState().equals("running") && job.getStringOr("phase","").equals("preflight") && job.getIntOr("cursor",-1)==64,"large preflight paused at batch boundary");
                        waitTicks=1;
                    } else if(waitTicks==1){
                        job=document().getCompoundOrEmpty("job");
                        check(jobState().equals("running") && job.getStringOr("phase","").equals("place") && job.getIntOr("cursor",-1)==0,"large preflight transitioned to placement");
                        waitTicks=2;
                    } else if(waitTicks==2){
                        job=document().getCompoundOrEmpty("job");
                        check(jobState().equals("running") && job.getStringOr("phase","").equals("place") && job.getIntOr("cursor",-1)==64 && job.getIntOr("completedBlocks",-1)==64,"large placement paused at batch boundary");
                        cmd("function space_editor:load"); job=document().getCompoundOrEmpty("job");
                        check(jobState().equals("running") && job.getIntOr("cursor",-1)==64,"load preserved transformed cursor");
                        waitTicks=3;
                    } else {
                        check(jobState().equals("done"),"large transformed paste resumed and completed");
                        check(helper.getLevel().getBlockState(new BlockPos(60,TY,0)).is(Blocks.STONE) && helper.getLevel().getBlockState(new BlockPos(64,TY+2,4)).is(Blocks.STONE),"large transformed paste output present");
                        pcmd("item replace entity @s weapon.mainhand with minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"paste\"}}]");
                        player.setYRot(0); player.setXRot(0); pcmd("function space_editor:paste_mode/begin");
                        player.setYRot(-90); pcmd("function space_editor:paste_mode/read_intent");
                        check(score("se.intent")==1,"left look intent detected");
                        pcmd("function space_editor:paste_mode/apply");
                        check(score("se.rot")==270,"shift-left selected left rotation");
                        player.setXRot(-60); pcmd("function space_editor:paste_mode/read_intent");
                        check(score("se.intent")==3,"vertical look intent detected");
                        pcmd("function space_editor:paste_mode/apply");
                        check(score("se.flip")==1,"shift-up toggled FlipY");
                        check(document().getListOrEmpty("actions").size()==12,"successful and partially skipped pastes persisted actions");
                        startPaste(6,ROT[stairPasteIndex],0,70+stairPasteIndex*7,TY,0); step=5; waitTicks=0;
                    }
                } else if(step==5){
                    tickJob(); waitTicks++;
                    if(!jobState().equals("running")){
                        verifyStairShapes(stairPasteIndex); stairPasteIndex++; waitTicks=0;
                        if(stairPasteIndex<4) startPaste(6,ROT[stairPasteIndex],0,70+stairPasteIndex*7,TY,0);
                        else {
                            check(document().getListOrEmpty("actions").size()==16,"stair shape pastes persisted actions");
                            verifyPreviewAndMoveTools();
                            startPaste(7,90,1,110,TY,0); step=6; waitTicks=0;
                        }
                    } else if(waitTicks>20)throw new AssertionError("stair shape rotation timeout "+stairPasteIndex);
                } else if(step==6){
                    tickJob(); waitTicks++;
                    if(!jobState().equals("running")){
                        var fencePos=new BlockPos(110,TY,0); var wallPos=new BlockPos(110,TY,1);
                        var fence=helper.getLevel().getBlockState(fencePos); var wall=helper.getLevel().getBlockState(wallPos);
                        check(fence.is(Blocks.CHERRY_FENCE) && fence.getValue(BlockStateProperties.EAST) && fence.getValue(BlockStateProperties.WEST),"FlipY fence collision carrier and rotated connections");
                        check(wall.is(Blocks.SANDSTONE_WALL)
                                && wall.getValue(BlockStateProperties.EAST_WALL)==WallSide.LOW
                                && wall.getValue(BlockStateProperties.WEST_WALL)==WallSide.TALL,
                                "FlipY wall collision carrier and rotated connections actual="+wall);
                        cmd("data remove storage space_editor:runtime specialTest");
                        cmd("execute positioned 110 "+TY+" 0 if entity @e[type=minecraft:block_display,tag=space_editor.special_fence,distance=..0.1] run data modify storage space_editor:runtime specialTest.fence set value 1b");
                        cmd("execute positioned 110 "+TY+" 1 if entity @e[type=minecraft:block_display,tag=space_editor.special_wall,distance=..0.1] run data modify storage space_editor:runtime specialTest.wall set value 1b");
                        cmd("execute positioned 110 "+TY+" 0 run data modify storage space_editor:runtime specialTest.visual set from entity @e[type=minecraft:block_display,tag=space_editor.special_fence,distance=..0.1,limit=1] block_state.Name");
                        cmd("execute positioned 110 "+TY+" 1 run data modify storage space_editor:runtime specialTest.wallVisual set from entity @e[type=minecraft:block_display,tag=space_editor.special_wall,distance=..0.1,limit=1] block_state.Properties");
                        cmd("execute positioned 110 "+TY+" 0 store result storage space_editor:runtime specialTest.scaleX int 1 run data get entity @e[type=minecraft:block_display,tag=space_editor.special_fence,distance=..0.1,limit=1] transformation.scale[0] 1");
                        cmd("execute positioned 110 "+TY+" 0 store result storage space_editor:runtime specialTest.scaleY int 1 run data get entity @e[type=minecraft:block_display,tag=space_editor.special_fence,distance=..0.1,limit=1] transformation.scale[1] 1");
                        cmd("execute positioned 110 "+TY+" 0 store result storage space_editor:runtime specialTest.translationX int 1 run data get entity @e[type=minecraft:block_display,tag=space_editor.special_fence,distance=..0.1,limit=1] transformation.translation[0] 10");
                        cmd("execute positioned 110 "+TY+" 0 store result storage space_editor:runtime specialTest.translationZ int 1 run data get entity @e[type=minecraft:block_display,tag=space_editor.special_fence,distance=..0.1,limit=1] transformation.translation[2] 10");
                        cmd("execute positioned 110 "+TY+" 0 store success storage space_editor:runtime specialTest.fenceHasBrightness byte 1 run data get entity @e[type=minecraft:block_display,tag=space_editor.special_fence,distance=..0.1,limit=1] brightness");
                        cmd("execute positioned 110 "+TY+" 1 store success storage space_editor:runtime specialTest.wallHasBrightness byte 1 run data get entity @e[type=minecraft:block_display,tag=space_editor.special_wall,distance=..0.1,limit=1] brightness");
                        var specialTest=runtime().getCompoundOrEmpty("specialTest");
                        check(specialTest.getBooleanOr("fence",false) && specialTest.getBooleanOr("wall",false),"FlipY special displays spawned");
                        check(specialTest.getStringOr("visual","").equals("minecraft:oak_fence")
                                && specialTest.getIntOr("scaleX",0)==-1 && specialTest.getIntOr("scaleY",0)==-1,
                                "source visual and front-face-preserving vertical mirror persisted");
                        check(specialTest.getIntOr("translationX",0)==5 && specialTest.getIntOr("translationZ",0)==-5,"block display centered on collision cell");
                        check(!specialTest.getBooleanOr("fenceHasBrightness",true) && !specialTest.getBooleanOr("wallHasBrightness",true),"special displays use ambient world lighting");
                        var wallVisual=specialTest.getCompoundOrEmpty("wallVisual");
                        check(wallVisual.getStringOr("east","").equals("tall") && wallVisual.getStringOr("west","").equals("low"),"display state compensates horizontal axis reflection");
                        check(document().getListOrEmpty("specials").size()==2,"special composite records persisted");
                        pcmd("execute positioned 110 "+TY+" 0 run function space_editor:special/delete_at");
                        check(helper.getLevel().getBlockState(fencePos).isAir() && document().getListOrEmpty("specials").size()==1,"delete wand path removed fence display, collision, and record");
                        pcmd("execute positioned 110 "+TY+" 1 run function space_editor:special/delete_at");
                        check(helper.getLevel().getBlockState(wallPos).isAir() && document().getListOrEmpty("specials").isEmpty(),"delete wand path removed wall display, collision, and record");
                        System.out.println("SPACE_EDITOR_STAGE3_RUNTIME_PASS: 8 coordinate states, all stair shapes at 4 rotations, FlipY fence/wall composite collision displays and deletion, delete-cancelled paste preview, one-block preview/region move, reload-resumed cursor, unsupported skip warning, shift controls");
                        finished=true;h.succeed();
                    } else if(waitTicks>20)throw new AssertionError("FlipY special fence/wall timeout");
                }
            }catch(Throwable ex){finished=true;ex.printStackTrace();h.fail(ex.getMessage());}
        });
    }

    public static void main(String[] args)throws Exception{
        SharedConstants.tryDetectVersion();
        TestFunctionLoader.registerLoader(new TestFunctionLoader(){public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register){register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorStage3GameTest::test);}});
        Path universe=Path.of(args[0]).toAbsolutePath().normalize();
        Path allowed=Path.of("build/test-server").toAbsolutePath().normalize();
        if(!universe.startsWith(allowed)||Files.exists(universe))throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/stage3-runtime-report.xml").toAbsolutePath().toString()},ignored->{});
    }
}
