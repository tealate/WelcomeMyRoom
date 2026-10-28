// Runtime contract tests against Minecraft 26.1, not a second math implementation.
import java.nio.file.*;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.nbt.*;

public class SpaceEditorStage5GameTest {
    static GameTestHelper helper;
    static CommandSourceStack source;
    static net.minecraft.server.level.ServerPlayer player;
    static final Identifier DOCUMENT=Identifier.parse("space_editor:document");
    static final Identifier RUNTIME=Identifier.parse("space_editor:runtime");
    static CompoundTag document(){return helper.getLevel().getServer().getCommandStorage().get(DOCUMENT);}
    static CompoundTag runtime(){return helper.getLevel().getServer().getCommandStorage().get(RUNTIME);}
    static void cmd(String value){helper.getLevel().getServer().getCommands().performPrefixedCommand(source,value);}
    static void pcmd(String value){helper.getLevel().getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS),value);}
    static ListTag regions(){return document().getListOrEmpty("regions");}
    static CompoundTag region(int id){for(var value:regions())if(value instanceof CompoundTag r && r.getIntOr("id",0)==id)return r;throw new AssertionError("Missing Region "+id);}
    static void check(boolean ok,String message){if(!ok)throw new AssertionError(message+" DOCUMENT="+document()+" RUNTIME="+runtime());}
    static void near(double actual,double expected,String message){check(Math.abs(actual-expected)<0.00001,message+" actual="+actual+" expected="+expected);}
    static String frame(int rotation,int flip,int offset){
        return "{dimension:\"minecraft:overworld\",rotationY:"+rotation+",flipY:"+flip+"b,x1m:"+(-3000+offset)+",x2m:"+(1000+offset)+",y1m:80000,y2m:83000,z1m:-2500,z2m:3500}";
    }
    static void mappingTests(){
        for(int a=0;a<4;a++)for(int af=0;af<2;af++)for(int b=0;b<4;b++)for(int bf=0;bf<2;bf++){
            cmd("data modify storage space_editor:runtime map set value {source:"+frame(a*90,af,0)+",target:"+frame(b*90,bf,20000)+",point:[-2.125d,80.25d,2.375d],vector:[0.125d,-0.25d,0.5d],yaw:15f,pitch:25f}");
            cmd("function space_editor:mapping/position");
            var result=runtime().getCompoundOrEmpty("map").getCompoundOrEmpty("result");
            // Independent relative rotation oracle: clockwise quarter turns.
            double dx=-1.125,dz=1.875;
            for(int turn=0;turn<(b-a+4)%4;turn++){double old=dx;dx=-dz;dz=old;}
            near(result.getListOrEmpty("point").getDoubleOr(0,999),19+dx,"mapped x");
            near(result.getListOrEmpty("point").getDoubleOr(1,999),81.5+(af==bf?-1.25:1.25),"mapped y");
            near(result.getListOrEmpty("point").getDoubleOr(2,999),.5+dz,"mapped z");
            cmd("data modify storage space_editor:runtime map.point set from storage space_editor:runtime map.result.point");
            cmd("data modify storage space_editor:runtime map.vector set from storage space_editor:runtime map.result.vector");
            cmd("data modify storage space_editor:runtime map.yaw set from storage space_editor:runtime map.result.yaw");
            cmd("data modify storage space_editor:runtime map.pitch set from storage space_editor:runtime map.result.pitch");
            cmd("data modify storage space_editor:runtime map.source set value "+frame(b*90,bf,20000));
            cmd("data modify storage space_editor:runtime map.target set value "+frame(a*90,af,0));
            cmd("function space_editor:mapping/position");
            result=runtime().getCompoundOrEmpty("map").getCompoundOrEmpty("result");
            double[] point={-2.125,80.25,2.375},vector={.125,-.25,.5};
            for(int i=0;i<3;i++){
                near(result.getListOrEmpty("point").getDoubleOr(i,999),point[i],"inverse point");
                near(result.getListOrEmpty("vector").getDoubleOr(i,999),vector[i],"inverse vector");
            }
            near(result.getFloatOr("yaw",999),15,"inverse yaw");
            near(result.getFloatOr("pitch",999),25,"inverse pitch");
        }
        // Odd milliblock endpoints: center is exactly a half-milliblock.
        cmd("data modify storage space_editor:runtime map set value {source:"+frame(0,0,0)+",target:"+frame(90,1,20000)+",point:[-2.125d,80.25d,2.375d]}");
        cmd("data modify storage space_editor:runtime map.target.x1m set value 17001");
        cmd("function space_editor:mapping/position");
        near(runtime().getCompoundOrEmpty("map").getCompoundOrEmpty("result").getDoubleOr("x",999),17.1255,"half-milliblock center");
        cmd("data modify storage space_editor:runtime map.point set value [-0.5005d,80.1235d,0.1005d]");
        cmd("data modify storage space_editor:runtime map.yaw set value -0.1f");
        cmd("data modify storage space_editor:runtime map.pitch set value 30.123f");
        for(int n=0;n<32;n++){
            cmd("function space_editor:mapping/position");
            cmd("data modify storage space_editor:runtime map.point set from storage space_editor:runtime map.result.point");
            cmd("data modify storage space_editor:runtime map.yaw set from storage space_editor:runtime map.result.yaw");
            cmd("data modify storage space_editor:runtime map.pitch set from storage space_editor:runtime map.result.pitch");
            cmd("data modify storage space_editor:runtime tempFrame set from storage space_editor:runtime map.source");
            cmd("data modify storage space_editor:runtime map.source set from storage space_editor:runtime map.target");
            cmd("data modify storage space_editor:runtime map.target set from storage space_editor:runtime tempFrame");
        }
        var repeated=runtime().getCompoundOrEmpty("map").getListOrEmpty("point");
        near(repeated.getDoubleOr(0,999),-.5005,"repeated negative mapping has no quantization drift");
        near(repeated.getDoubleOr(1,999),80.1235,"repeated fractional mapping has no drift");
        near(repeated.getDoubleOr(2,999),.1005,"repeated z mapping has no drift");
        near(runtime().getCompoundOrEmpty("map").getFloatOr("yaw",999),-.1,"repeated fractional yaw has no drift");
        near(runtime().getCompoundOrEmpty("map").getFloatOr("pitch",999),30.123,"repeated fractional pitch has no drift");
    }
    static int plain(){
        cmd("data modify storage space_editor:runtime selection set value {a:[I;0,80,0],b:[I;2,83,4],dimension:\"minecraft:overworld\"}");
        cmd("function space_editor:region/create");
        return regions().getCompoundOrEmpty(regions().size()-1).getIntOr("id",0);
    }
    static int pair(String kind){
        int pairsBefore=document().getListOrEmpty("regionPairs").size();
        int a=plain();
        cmd("data modify storage space_editor:runtime pairCandidate set from storage space_editor:document regions[{id:"+a+"}]");
        cmd("data modify storage space_editor:runtime pairCandidate.x1m set value 20000");
        cmd("data modify storage space_editor:runtime pairCandidate.x2m set value 23000");
        cmd("function space_editor:pair/create {source:"+a+",kind:\""+kind+"\"}");
        check(region(a).contains("pairId"),"pair committed");
        check(document().getListOrEmpty("regionPairs").size()==pairsBefore+1,"exactly one pair record per creation");
        return a;
    }
    static void pose(int id,int rotation,int flip){cmd("function space_editor:pair/set_pose {id:"+id+",rotationY:"+rotation+",flipY:"+flip+"}");}
    static void select(int id,String tool,int face){
        cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:"+id+"}]");
        cmd("data modify storage space_editor:runtime activeTool set value \""+tool+"\"");
        cmd("data modify storage space_editor:runtime hitFace set value "+face);
    }
    static int[] turn(int[] v,int r,boolean flip){
        v=v.clone();for(int i=0;i<(r+4)%4;i++){int x=v[0];v[0]=-v[2];v[2]=x;}if(flip)v[1]=-v[1];return v;
    }
    static void pairTests(){
        for(int ar=0;ar<4;ar++)for(int af=0;af<2;af++)for(int br=0;br<4;br++)for(int bf=0;bf<2;bf++){
            for(int face=0;face<6;face++){
                cmd("data modify storage space_editor:document regions set value []");
                cmd("data modify storage space_editor:document regionPairs set value []");
                cmd("data modify storage space_editor:document actions set value []");
                int a=pair("teleport"),b=region(a).getIntOr("partnerId",0);
                pose(a,ar*90,af);pose(b,br*90,bf);
                var beforeA=region(a).copy();var beforeB=region(b).copy();
                select(a,"resize_face",face);pcmd("function space_editor:region/resize_face");
                int[] n={0,0,0};n[face/2]=face%2==0?-1:1;
                int[] mapped=turn(turn(n,-ar,af==1),br,bf==1);
                for(int axis=0;axis<3;axis++)for(int edge=1;edge<=2;edge++){
                    String key="xyz".charAt(axis)+""+edge+"m";
                    int da=(axis==face/2 && edge==face%2+1)?(face%2==0?-100:100):0;
                    int db=(mapped[axis]<0 && edge==1)?-100:(mapped[axis]>0 && edge==2)?100:0;
                    check(region(a).getIntOr(key,0)==beforeA.getIntOr(key,0)+da,"selected face/opposite face "+ar+" "+af+" "+br+" "+bf+" "+face);
                    check(region(b).getIntOr(key,0)==beforeB.getIntOr(key,0)+db,"partner local face/opposite face "+ar+" "+af+" "+br+" "+bf+" "+face);
                }
                check(java.util.Arrays.equals(region(a).getIntArray("localSize").orElseThrow(),region(b).getIntArray("localSize").orElseThrow()),"local dimensions synchronized");
            }
        }
        int a=pair("space_link"),b=region(a).getIntOr("partnerId",0);
        var partner=region(b).copy();
        pose(a,90,1);check(region(b).equals(partner),"pose does not move partner");
        near(region(a).getDoubleOr("cx",999),1.5,"3x5 rotated center x");
        near(region(a).getDoubleOr("cz",999),2.5,"rotated center z");
        for(int rot:new int[]{180,270,0})pose(a,rot,0);
        check(region(a).getIntOr("x1m",999)==0 && region(a).getIntOr("z1m",999)==0,"four turns do not drift");
        select(a,"move",1);pcmd("function space_editor:region/move");
        check(region(b).equals(partner),"move does not move partner");
        cmd("data modify storage space_editor:document regions[{id:"+b+"}].y1m set value 316000");
        cmd("data modify storage space_editor:document regions[{id:"+b+"}].y2m set value 320000");
        var before=document().copy();
        select(a,"resize_face",3);pcmd("function space_editor:region/resize_face");
        check(document().equals(before),"partner height limit rolls back entire edit and action");
        int c=pair("teleport"),d=region(c).getIntOr("partnerId",0),exist=plain();
        select(exist,"pair_select",0);pcmd("function space_editor:pair/mark_existence");
        cmd("data modify storage space_editor:document legacyUnknown set value {keep:42}");
        var preserved=region(c).copy();
        cmd("function space_editor:load");
        check(region(c).equals(preserved) && document().getCompoundOrEmpty("legacyUnknown").getIntOr("keep",0)==42,"reload preserves metadata and unknown data");
        select(a,"delete",0);pcmd("function space_editor:region/apply_hit");
        check(region(c).equals(preserved) && region(d).contains("pairId") && region(exist).getStringOr("kind","").equals("proxy_existence"),"pair deletion isolates other pair kinds and existence Regions");
        for(var value:regions()){var r=(CompoundTag)value;check(r.getIntOr("id",0)!=a && r.getIntOr("id",0)!=b,"both pair members removed");}
        var actions=document().getListOrEmpty("actions");
        check(actions.getCompoundOrEmpty(actions.size()-1).getStringOr("operation","").equals("delete"),"pair delete is one snapshot action");
        int mixed=plain();
        cmd("data modify storage space_editor:document regions[{id:"+mixed+"}].z2m set value 4000");
        cmd("data modify storage space_editor:runtime pairCandidate set from storage space_editor:document regions[{id:"+mixed+"}]");
        cmd("data modify storage space_editor:runtime pairCandidate.x1m set value 20000");
        cmd("data modify storage space_editor:runtime pairCandidate.x2m set value 23000");
        cmd("function space_editor:pair/create {source:"+mixed+",kind:\"space_link\"}");
        pose(mixed,90,0);
        near(region(mixed).getDoubleOr("x1",999),-.5,"mixed parity center rotation");
        near(region(mixed).getListOrEmpty("min").getDoubleOr(0,999),-.5,"legacy min retains fractional boundary");
        near(region(mixed).getDoubleOr("z1",999),.5,"mixed parity z boundary");
        var exact=region(mixed).copy();
        select(mixed,"resize_all",0);pcmd("function space_editor:region/resize_all");
        player.setShiftKeyDown(true);player.setPose(net.minecraft.world.entity.Pose.CROUCHING);
        select(mixed,"resize_all",0);pcmd("function space_editor:region/resize_all");
        player.setShiftKeyDown(false);player.setPose(net.minecraft.world.entity.Pose.STANDING);
        check(region(mixed).equals(exact),"expand/shrink round trip preserves every boundary");
    }
    static void uiTests(){
        pcmd("function space_editor:start");
        player.setPos(.5,82,-2.5);player.setYRot(0);player.setXRot(0);
        int a=plain();
        pcmd("function space_editor:pair/held_teleport");
        select(a,"pair_select",0);pcmd("function space_editor:pair/select");
        check(runtime().contains("pairPending") && !region(a).contains("pairId"),"first click stages a preview without mutating source");
        pcmd("scoreboard players set @s se.prot 90");pcmd("scoreboard players set @s se.pflip 1");
        pcmd("function space_editor:pair/track");
        var candidate=runtime().getCompoundOrEmpty("pairCandidate");
        check(candidate.getIntOr("sxm",0)==5000 && candidate.getIntOr("szm",0)==3000,"preview rotates local size");
        var entity=helper.getLevel().getAllEntities().iterator();
        java.util.UUID preview=null;
        while(entity.hasNext()){var e=entity.next();if(e.entityTags().contains("space_editor.pair_pending_box"))preview=e.getUUID();}
        check(preview!=null,"placement preview spawned");
        int arrows=0;for(var e:helper.getLevel().getAllEntities())if(e.entityTags().contains("space_editor.pending_arrow_front") || e.entityTags().contains("space_editor.pending_arrow_up"))arrows++;
        check(arrows==2,"both 3D orientation arrows spawned");
        pcmd("execute as @e[tag=space_editor.pending_arrow_front,limit=1] run data modify storage space_editor:runtime testArrow set from entity @s transformation.left_rotation");
        check(runtime().getListOrEmpty("testArrow").getFloatOr(1,0)<-.7,"front arrow rotates toward world -X at yaw 90");
        pcmd("execute as @e[tag=space_editor.pending_arrow_up,limit=1] run data modify storage space_editor:runtime testArrow set from entity @s transformation.left_rotation");
        check(runtime().getListOrEmpty("testArrow").getFloatOr(0,0)>.7,"FlipY arrow points downward");
        pcmd("function space_editor:pair/track");
        boolean same=false;for(var e:helper.getLevel().getAllEntities())if(e.entityTags().contains("space_editor.pair_pending_box") && e.getUUID().equals(preview))same=true;
        check(same,"placement preview reuses entity");
        pcmd("function space_editor:pair/confirm");
        check(region(a).contains("pairId") && !runtime().contains("pairPending"),"second click commits pair and clears preview");
        int b=region(a).getIntOr("partnerId",0);
        check(region(b).getIntOr("rotationY",0)==90 && region(b).getBooleanOr("flipY",false),"preview pose persisted");
        pcmd("function space_editor:play");
        for(var e:helper.getLevel().getAllEntities())check(!e.entityTags().contains("space_editor.preview"),"play hides every edit indicator");
    }
    static void config(int regionId,int group){
        cmd("function space_editor:pair/configure {id:"+region(regionId).getIntOr("pairId",0)+",groupId:"+group+",roomA:\"room_a\",roomB:\"room_b\",direction:\"both\",cooldownTicks:20}");
    }
    static void snapshot(){
        cmd("data modify storage space_editor:runtime playerSnapshots set value []");
        pcmd("function space_editor:teleport/snapshot");
    }
    static net.minecraft.server.level.ServerPlayer namedPlayer(String name){
        var server=helper.getLevel().getServer();
        var cookie=net.minecraft.server.network.CommonListenerCookie.createInitial(new com.mojang.authlib.GameProfile(java.util.UUID.randomUUID(),name),false);
        var p=new net.minecraft.server.level.ServerPlayer(server,helper.getLevel(),cookie.gameProfile(),cookie.clientInformation()){
            public net.minecraft.world.level.GameType gameMode(){return net.minecraft.world.level.GameType.CREATIVE;}
        };
        var connection=new net.minecraft.network.Connection(net.minecraft.network.protocol.PacketFlow.SERVERBOUND);
        new io.netty.channel.embedded.EmbeddedChannel(connection);
        server.getPlayerList().placeNewPlayer(connection,p,cookie);
        return p;
    }
    static void teleportTests(){
        cmd("data modify storage space_editor:document regions set value []");
        cmd("data modify storage space_editor:document regionPairs set value []");
        cmd("data modify storage space_editor:document actions set value []");
        int tp=pair("teleport"),dest=region(tp).getIntOr("partnerId",0),sl=pair("space_link");
        config(tp,1);config(sl,1);
        check(runtime().getListOrEmpty("linkWarnings").isEmpty(),"matching independent pairs validate");
        pose(dest,90,1);
        check(runtime().getListOrEmpty("linkWarnings").size()==1,"independent pair pose mismatch warns");
        pose(region(sl).getIntOr("partnerId",0),90,1);
        check(runtime().getListOrEmpty("linkWarnings").isEmpty(),"matching new poses clear warning");
        var links=document().getListOrEmpty("linkGroups").copy();
        cmd("function space_editor:load");
        check(document().getListOrEmpty("linkGroups").equals(links),"group survives reload");
        pcmd("function space_editor:play");
        pcmd("scoreboard players set @s se.tp_cd 0");pcmd("scoreboard players set @s se.tp_lock 0");pcmd("scoreboard players set @s se.instance 7");
        player.setPos(.5,80.5,1.5);player.setYRot(15);player.setXRot(25);
        cmd("fill 18 78 -2 26 88 8 air");
        snapshot();pcmd("function space_editor:teleport/player");
        near(player.getX(),22.5,"TP position x");near(player.getY(),83.5,"TP FlipY position y");near(player.getZ(),1.5,"TP rotation z");
        near(player.getYRot(),105,"TP yaw");near(player.getXRot(),-25,"TP pitch");
        cmd("function space_editor:load");snapshot();pcmd("function space_editor:teleport/player");near(player.getX(),22.5,"reload retains per-player arrival lock");
        for(int i=0;i<30;i++){pcmd("scoreboard players set @s se.tp_cd 0");snapshot();pcmd("function space_editor:teleport/player");}
        near(player.getX(),22.5,"destination dwell never bounces even after cooldown");
        player.setPos(40.5,80.5,1.5);snapshot();pcmd("function space_editor:teleport/player");
        player.setPos(22.5,83.5,1.5);snapshot();pcmd("function space_editor:teleport/player");
        near(player.getX(),.5,"reverse after exit/re-entry x");near(player.getY(),80.5,"reverse y");near(player.getYRot(),15,"reverse yaw");
        pcmd("scoreboard players set @s se.tp_cd 0");pcmd("scoreboard players set @s se.tp_lock 0");
        cmd("setblock 22 84 1 stone");snapshot();pcmd("function space_editor:teleport/player");
        near(player.getX(),.5,"obstructed arrival refuses TP");cmd("setblock 22 84 1 air");
        cmd("data modify storage space_editor:runtime destinationBackup set from storage space_editor:document regions[{id:"+dest+"}]");
        cmd("data modify storage space_editor:document regions[{id:"+dest+"}].x1m set value 99998000");
        cmd("data modify storage space_editor:document regions[{id:"+dest+"}].x2m set value 100003000");
        snapshot();pcmd("function space_editor:teleport/player");near(player.getX(),.5,"unloaded target refuses TP");
        cmd("data modify storage space_editor:document regions[{id:"+dest+"}] set from storage space_editor:runtime destinationBackup");
        player.setPos(3,80.5,1.5);snapshot();pcmd("function space_editor:teleport/player");near(player.getX(),3,"maxExclusive is excluded");
        player.setPos(.5,80.5,1.5);pcmd("function space_editor:start");snapshot();pcmd("function space_editor:teleport/player");near(player.getX(),.5,"editing never teleports");pcmd("function space_editor:play");
        player.deathTime=1;snapshot();pcmd("function space_editor:teleport/player");near(player.getX(),.5,"dead player is not transferred");player.deathTime=0;
        var other=namedPlayer("pair-test-two");other.setNoGravity(true);other.setPos(1,81,2);other.setYRot(0);other.setXRot(0);
        check(!other.getUUID().equals(player.getUUID()),"two distinct player UUIDs");
        var list=helper.getLevel().getServer().getPlayerList().getPlayers();
        boolean addFirst=!list.contains(player),addSecond=!list.contains(other);
        if(addFirst)list.add(player);if(addSecond)list.add(other);
        try{
            pcmd("scoreboard players set @s se.tp_cd 0");pcmd("scoreboard players set @s se.tp_lock 0");
            cmd("function space_editor:teleport/tick");
            check(runtime().getListOrEmpty("playerSnapshots").size()==2,"all players captured before any TP");
            check(runtime().getListOrEmpty("spaceLinkContacts").size()==2,"both SpaceLink contacts use pre-TP positions");
            check(runtime().getListOrEmpty("transfers").size()==2,"both players TP independently in one tick");
            near(runtime().getListOrEmpty("playerSnapshots").getCompoundOrEmpty(0).getListOrEmpty("point").getDoubleOr(0,999),.5,"snapshot unchanged by transfer");
            near(other.getX(),22,"second player mapping independent");
            cmd("function space_editor:teleport/tick");
            check(runtime().getListOrEmpty("transfers").isEmpty(),"next tick suppresses both loops");
        }finally{if(addFirst)list.remove(player);helper.getLevel().getServer().getPlayerList().remove(other);}
        // Cross-dimension mapping uses identical math, with loaded/safe target.
        player.setPos(.5,80.5,1.5);pcmd("scoreboard players set @s se.tp_cd 0");pcmd("scoreboard players set @s se.tp_lock 0");
        cmd("data modify storage space_editor:document regions[{id:"+dest+"}].dimension set value \"minecraft:the_nether\"");
        cmd("execute in minecraft:the_nether run fill 18 78 -2 26 88 8 air");
        snapshot();pcmd("function space_editor:teleport/player");
        check(player.level().dimension().identifier().toString().equals("minecraft:the_nether"),"dimension transfer succeeds");
        near(player.getX(),22.5,"dimension transfer mapping");
        pcmd("execute in minecraft:overworld run tp @s 0.5 80.5 1.5");
        select(tp,"delete",0);pcmd("function space_editor:region/apply_hit");
        check(document().getListOrEmpty("linkGroups").size()==1,"shared group retained for SpaceLink");
        select(sl,"delete",0);pcmd("function space_editor:region/apply_hit");
        check(document().getListOrEmpty("linkGroups").isEmpty(),"unreferenced group collected");
    }
    static void test(GameTestHelper h){
        helper=h;source=h.getLevel().getServer().createCommandSourceStack();
        cmd("function space_editor:load");cmd("forceload add -16 -16 48 16");cmd("execute in minecraft:the_nether run forceload add 16 -16 32 16");
        player=h.makeMockServerPlayerInLevel();player.setNoGravity(true);player.setPos(.5,82,-2.5);
        final boolean[] done={false};final int[] ticks={0};
        h.onEachTick(()->{
            if(done[0])return;
            try{
                cmd("execute store success storage space_editor:runtime testLoaded byte 1 if loaded 0 80 0");
                if(!runtime().getBooleanOr("testLoaded",false)){if(++ticks[0]>100)throw new AssertionError("test chunks not loaded");return;}
                cmd("execute in minecraft:the_nether store success storage space_editor:runtime netherLoaded byte 1 if loaded 22 80 1");
                if(!runtime().getBooleanOr("netherLoaded",false)){if(++ticks[0]>2000){for(var level:h.getLevel().getServer().getAllLevels())System.out.println("TEST_LEVEL "+level.dimension());throw new AssertionError("Nether test chunks not loaded");}return;}
                mappingTests();pairTests();uiTests();teleportTests();
                System.out.println("SPACE_EDITOR_STAGE5_RUNTIME_PASS: 64 mappings, no drift, 384 face edits, rollback, pose, placement, reload, group warnings, TP/re-entry, safe/unloaded exits, two players, pre-TP contacts, dimension transfer");
                done[0]=true;h.succeed();
            }catch(Throwable ex){done[0]=true;ex.printStackTrace();h.fail(ex.getMessage());}
        });
    }
    public static void main(String[] args)throws Exception{
        SharedConstants.tryDetectVersion();
        TestFunctionLoader.registerLoader(new TestFunctionLoader(){
            public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register){
                register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorStage5GameTest::test);
            }
        });
        Path universe=Path.of(args[0]).toAbsolutePath().normalize();
        Path allowed=Path.of("build/test-server").toAbsolutePath().normalize();
        if(!universe.startsWith(allowed)||Files.exists(universe))throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/stage5-runtime-report.xml").toAbsolutePath().toString()},ignored->{});
    }
}
