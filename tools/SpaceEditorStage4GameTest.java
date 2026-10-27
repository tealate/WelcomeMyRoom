// Isolated runtime checks for stage-4 persistent Mask objects.
import java.nio.file.*;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.nbt.*;

public class SpaceEditorStage4GameTest {
    static GameTestHelper helper;
    static CommandSourceStack source;
    static net.minecraft.server.level.ServerPlayer player;
    static int step, waitTicks;
    static final int rx=0, ry=80, rz=0;
    static boolean finished;
    static final Identifier DOCUMENT=Identifier.parse("space_editor:document");
    static final Identifier RUNTIME=Identifier.parse("space_editor:runtime");

    static CompoundTag document(){return helper.getLevel().getServer().getCommandStorage().get(DOCUMENT);}
    static CompoundTag runtime(){return helper.getLevel().getServer().getCommandStorage().get(RUNTIME);}
    static ListTag regions(){return document().getListOrEmpty("regions");}
    static ListTag masks(){return document().getListOrEmpty("masks");}
    static void cmd(String value){helper.getLevel().getServer().getCommands().performPrefixedCommand(source,value);}
    static void pcmd(String value){helper.getLevel().getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS),value);}
    static void check(boolean ok,String message){if(!ok)throw new AssertionError(message+" DOCUMENT="+document()+" RUNTIME="+runtime());}
    static long count(String tag){long result=0;for(var entity:helper.getLevel().getAllEntities())if(entity.entityTags().contains(tag))result++;return result;}
    static net.minecraft.world.entity.Entity entity(String tag){for(var entity:helper.getLevel().getAllEntities())if(entity.entityTags().contains(tag))return entity;return null;}

    static void test(GameTestHelper h){
        helper=h;source=h.getLevel().getServer().createCommandSourceStack();step=0;waitTicks=0;finished=false;
        h.onEachTick(()->{
            if(finished)return;
            try{
                if(step==0){
                    cmd("function space_editor:load");
                    cmd("forceload add -16 -16 16 16");
                    player=h.makeMockServerPlayerInLevel();player.setNoGravity(true);player.setPos(rx+.5,ry+2,rz-2.5);
                    step++;
                }else if(step==1){
                    cmd("data remove storage space_editor:runtime stage4.chunkLoaded");
                    cmd("execute if loaded 0 80 0 run data modify storage space_editor:runtime stage4.chunkLoaded set value 1b");
                    if(!runtime().getCompoundOrEmpty("stage4").getBooleanOr("chunkLoaded",false)){
                        if(++waitTicks>100)throw new AssertionError("fixed test chunk did not load");
                        return;
                    }
                    cmd("data modify storage space_editor:runtime selection set value {a:[I;"+rx+","+ry+","+rz+"],b:[I;"+rx+","+ry+","+rz+"],dimension:\"minecraft:overworld\"}");
                    cmd("function space_editor:region/create");
                    check(regions().size()==1,"one-block Region created in loaded test chunk");
                    cmd("data modify storage space_editor:runtime cursorTest set value {dimension:\"minecraft:overworld\",x:0,y:81,z:0}");
                    cmd("function space_editor:preview/selection_candidate with storage space_editor:runtime cursorTest");
                    var cursor=entity("space_editor.selection_candidate");
                    check(cursor!=null,"selection cursor spawned once");
                    var cursorId=cursor.getUUID();
                    cmd("function space_editor:preview/selection_candidate with storage space_editor:runtime cursorTest");
                    check(count("space_editor.selection_candidate")==1 && entity("space_editor.selection_candidate").getUUID().equals(cursorId),"unchanged cursor reuses entity");
                    cmd("data modify storage space_editor:runtime cursorTest.x set value 1");
                    cmd("function space_editor:preview/selection_candidate with storage space_editor:runtime cursorTest");
                    cursor=entity("space_editor.selection_candidate");
                    check(cursor.getUUID().equals(cursorId),"moved cursor preserves entity UUID old="+cursorId+" new="+cursor.getUUID());
                    check(Math.abs(cursor.getX()-1.5)<.000001,"moved cursor reaches target block center x="+cursor.getX());
                    cmd("function space_editor:preview/remove_selection_candidate");
                    check(count("space_editor.selection_candidate")==0,"unused cursor removed");
                    pcmd("function space_editor:start");
                    pcmd("execute store result storage space_editor:runtime stage4.maskWands int 1 run clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"mask\"}}] 0");
                    check(runtime().getCompoundOrEmpty("stage4").getIntOr("maskWands",0)==1,"dedicated Mask wand issued");
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
                    pcmd("function space_editor:mask/create_selected");
                    step++;
                }else if(step==2){
                    check(masks().size()==1,"Mask persisted in Document");
                    var mask=masks().getCompoundOrEmpty(0);
                    check(mask.getIntOr("regionId",0)==1 && mask.getStringOr("material","").equals("mask_default"),"Mask references Region and logical material");
                    check(mask.getIntArray("offset").orElseThrow()[0]==0 && mask.getIntArray("expand").orElseThrow()[0]==0,"default corrections are exact zero");
                    long bodies=count("space_editor.mask_body"),guides=count("space_editor.mask_guide");
                    check(bodies==1 && guides==1,"body and edit-only guide spawned separately body="+bodies+" guide="+guides);
                    check(document().getListOrEmpty("actions").size()==1,"Mask create Action recorded");
                    cmd("data remove storage space_editor:runtime stage4.bodyState");
                    cmd("execute as @e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1] run data modify storage space_editor:runtime stage4.bodyState set from entity @s block_state.Name");
                    check(runtime().getCompoundOrEmpty("stage4").getStringOr("bodyState","").equals("minecraft:waxed_oxidized_cut_copper"),"configured low-alpha Mask body used");
                    pcmd("function space_editor:play");
                    check(count("space_editor.mask_body")==1 && count("space_editor.mask_guide")==0 && count("space_editor.region")==0,"play hides guides but preserves Mask body");
                    pcmd("function space_editor:mask/set_offset {id:1,x:-0.01,y:0,z:-0.01}");
                    pcmd("function space_editor:mask/set_expand {id:1,x:0.1,y:0,z:0}");
                    step++;
                }else if(step==3){
                    var mask=masks().getCompoundOrEmpty(0);
                    int[] offset=mask.getIntArray("offset").orElseThrow();
                    int[] expand=mask.getIntArray("expand").orElseThrow();
                    check(offset[0]==-10 && offset[2]==-10 && expand[0]==100,"offset and expand stored as exact milliblocks");
                    double bodyX=999,bodyZ=999;
                    for(var entity:h.getLevel().getAllEntities())if(entity.entityTags().contains("space_editor.mask_body")){bodyX=entity.getX();bodyZ=entity.getZ();}
                    check(Math.abs(bodyX-(rx-.11))<.000001 && Math.abs(bodyZ-(rz-.01))<.000001,"Mask pivot applies offset and symmetric expand without implicit centering");
                    cmd("execute store result storage space_editor:runtime stage4.scaleX int 1 run data get entity @e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1] transformation.scale[0] 1000");
                    check(runtime().getCompoundOrEmpty("stage4").getIntOr("scaleX",0)==1200,"Mask scale includes expand on both sides");
                    pcmd("function space_editor:mask/set_expand {id:1,x:-1,y:0,z:0}");
                    check(masks().getCompoundOrEmpty(0).getIntArray("expand").orElseThrow()[0]==100,"non-positive Mask size rejected without mutation");
                    pcmd("function space_editor:mask/rename {id:1,name:\"entrance\"}");
                    check(masks().getCompoundOrEmpty(0).getStringOr("name","").equals("entrance"),"Mask rename persisted");
                    pcmd("function space_editor:start");
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
                    pcmd("function space_editor:region/resize_all");
                    step++;
                }else if(step==4){
                    cmd("execute store result storage space_editor:runtime stage4.scaleAfterResize int 1 run data get entity @e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1] transformation.scale[0] 1000");
                    int scaleAfterResize=runtime().getCompoundOrEmpty("stage4").getIntOr("scaleAfterResize",0);
                    check(scaleAfterResize>=1399 && scaleAfterResize<=1401,"Region resize updates Mask transformation");
                    check(document().getListOrEmpty("actions").size()==5,"create, offset, expand, rename, and Region-sync Actions recorded");
                    cmd("function space_editor:load");
                    check(masks().size()==1 && count("space_editor.mask_body")==1 && count("space_editor.mask_guide")==1,"reload rebuilds exactly one body and guide");
                    cmd("data modify storage space_editor:runtime activeTool set value \"delete\"");
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
                    pcmd("function space_editor:region/apply_hit");
                    check(masks().isEmpty() && regions().size()==1 && count("space_editor.mask_body")==0,"delete wand removes Mask first and preserves Region");
                    cmd("data modify storage space_editor:runtime activeTool set value \"delete\"");
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
                    pcmd("function space_editor:region/apply_hit");
                    check(regions().isEmpty(),"second delete removes now-unmasked Region");
                    System.out.println("SPACE_EDITOR_STAGE4_RUNTIME_PASS: reused selection cursor spawn/stay/move/remove, Mask wand, persistent Region reference, low-alpha body, edit-only guide, play visibility, exact offset/expand, invalid-size rejection, rename, Region resize following, Action records, reload rebuild, delete ordering");
                    finished=true;h.succeed();
                }
            }catch(Throwable ex){finished=true;ex.printStackTrace();h.fail(ex.getMessage());}
        });
    }

    public static void main(String[] args)throws Exception{
        SharedConstants.tryDetectVersion();
        TestFunctionLoader.registerLoader(new TestFunctionLoader(){
            public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register){
                register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorStage4GameTest::test);
            }
        });
        Path universe=Path.of(args[0]).toAbsolutePath().normalize();
        Path allowed=Path.of("build/test-server").toAbsolutePath().normalize();
        if(!universe.startsWith(allowed)||Files.exists(universe))throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/stage4-runtime-report.xml").toAbsolutePath().toString()},ignored->{});
    }
}
