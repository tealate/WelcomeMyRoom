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
        cmd("function space_editor:pair/create {source:"+a+",kind:\"teleport\"}");
        check(region(a).contains("pairId"),"pair committed");
        check(document().getListOrEmpty("regionPairs").size()==pairsBefore+1,"exactly one pair record per creation");
        if(kind.equals("space_link")){
            // Actual pre-migration fixture: no new SpaceLink pair creation API.
            int pairId=region(a).getIntOr("pairId",0),b=region(a).getIntOr("partnerId",0);
            cmd("data modify storage space_editor:document regions[{id:"+a+"}].kind set value \"space_link\"");
            cmd("data modify storage space_editor:document regions[{id:"+b+"}].kind set value \"space_link\"");
            cmd("data modify storage space_editor:document regionPairs[{id:"+pairId+"}].kind set value \"space_link\"");
        }
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
        int a=pair("teleport"),b=region(a).getIntOr("partnerId",0);
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
        cmd("function space_editor:pair/create {source:"+mixed+",kind:\"teleport\"}");
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
        cmd("function space_editor:pair/configure {id:"+region(regionId).getIntOr("pairId",region(regionId).getIntOr("legacyPairId",0))+",groupId:"+group+",roomA:\"room_a\",roomB:\"room_b\",direction:\"both\",cooldownTicks:20}");
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
        int slDest=region(sl).getIntOr("partnerId",0);
        config(tp,1);config(sl,1);
        check(runtime().getListOrEmpty("linkWarnings").isEmpty(),"matching independent pairs validate");
        pose(dest,90,1);
        check(runtime().getListOrEmpty("linkWarnings").size()==1,"independent pair pose mismatch warns");
        pose(slDest,90,1);
        check(runtime().getListOrEmpty("linkWarnings").isEmpty(),"matching new poses clear warning");
        int slThird=groupAdd(sl,40000);
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
            check(runtime().getListOrEmpty("spaceLinkContacts").size()==4,"both players contact both targets before TP");
            check(runtime().getListOrEmpty("transfers").size()==2,"both players TP independently in one tick");
            check(runtime().getCompoundOrEmpty("testBefore").getListOrEmpty("contacts").size()==4 && runtime().getCompoundOrEmpty("testBefore").getListOrEmpty("transfers").isEmpty(),"before hook sees all contacts and no transfers");
            check(runtime().getCompoundOrEmpty("testAfter").getListOrEmpty("transfers").size()==2,"after hook sees both successful transfers");
            var thirdPoints=new java.util.HashMap<String,Tag>();
            for(var v:runtime().getListOrEmpty("spaceLinkContacts")){var c=(CompoundTag)v;if(c.getIntOr("targetRegionId",0)==slThird)thirdPoints.put(c.get("uuid").toString(),c.getCompoundOrEmpty("destination").get("point").copy());}
            near(runtime().getListOrEmpty("playerSnapshots").getCompoundOrEmpty(0).getListOrEmpty("point").getDoubleOr(0,999),.5,"snapshot unchanged by transfer");
            near(other.getX(),22,"second player mapping independent");
            cmd("function space_editor:teleport/tick");
            check(runtime().getListOrEmpty("transfers").isEmpty(),"next tick suppresses both loops");
            check(runtime().getListOrEmpty("spaceLinkContacts").size()==4,"B retains routes to A and C after TP");
            for(var v:runtime().getListOrEmpty("spaceLinkContacts")){var c=(CompoundTag)v;if(c.getIntOr("targetRegionId",0)==slThird)check(c.getCompoundOrEmpty("destination").get("point").equals(thirdPoints.get(c.get("uuid").toString())),"C mapped position continuous across A to B TP");}
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
        check(document().getListOrEmpty("linkGroups").isEmpty(),"unreferenced Room association collected");
        check(region(slDest).contains("spaceLinkGroupId") && region(slThird).contains("spaceLinkGroupId"),"TP regression cleanup leaves two SpaceLink survivors");
    }
    static CompoundTag group(int id){for(var v:document().getListOrEmpty("spaceLinkGroups"))if(v instanceof CompoundTag g && g.getIntOr("id",0)==id)return g;throw new AssertionError("Missing group "+id);}
    static int groupAdd(int sourceId,int x){
        int id=document().getIntOr("nextId",0);
        cmd("data modify storage space_editor:runtime pairCandidate set from storage space_editor:document regions[{id:"+sourceId+"}]");
        for(String key:new String[]{"pairId","partnerId","spaceLinkGroupId","legacyPairId"})cmd("data remove storage space_editor:runtime pairCandidate."+key);
        int width=region(sourceId).getIntOr("x2m",0)-region(sourceId).getIntOr("x1m",0);
        cmd("data modify storage space_editor:runtime pairCandidate.x1m set value "+x);
        cmd("data modify storage space_editor:runtime pairCandidate.x2m set value "+(x+width));
        measured("function space_editor:space_group/add {source:"+sourceId+"}");
        check(region(id).contains("spaceLinkGroupId"),"new member committed");return id;
    }
    static void crouch(boolean value){player.setShiftKeyDown(value);player.setPose(value?net.minecraft.world.entity.Pose.CROUCHING:net.minecraft.world.entity.Pose.STANDING);}
    static void groupTests(){
        cmd("data modify storage space_editor:document regions set value []");
        cmd("data modify storage space_editor:document regionPairs set value []");
        cmd("data modify storage space_editor:document spaceLinkGroups set value []");
        cmd("data modify storage space_editor:document masks set value []");
        cmd("data modify storage space_editor:document actions set value []");
        int legacy=pair("space_link"),legacyB=region(legacy).getIntOr("partnerId",0);
        // Preserve fractional poses and all unrelated metadata through migration.
        cmd("data modify storage space_editor:document regions[{id:"+legacy+"}].roomId set value \"same_room\"");
        cmd("data modify storage space_editor:document regions[{id:"+legacyB+"}].roomId set value \"same_room\"");
        cmd("data modify storage space_editor:runtime frame set from storage space_editor:document regions[{id:"+legacy+"}]");
        cmd("data modify storage space_editor:runtime frame.rotationY set value 90");cmd("data modify storage space_editor:runtime frame.flipY set value 1b");
        cmd("function space_editor:pair/pose_bounds");
        cmd("data modify storage space_editor:document regions[{id:"+legacy+"}] set from storage space_editor:runtime frame");
        cmd("data modify storage space_editor:document regions[{id:"+legacyB+"}].dimension set value \"minecraft:the_nether\"");
        var oldA=region(legacy).copy();var oldB=region(legacyB).copy();var oldActions=document().getListOrEmpty("actions").copy();
        cmd("function space_editor:load");
        int gid=region(legacy).getIntOr("spaceLinkGroupId",0);
        check(gid>0 && group(gid).getListOrEmpty("members").size()==2,"old pair migrated to two member group");
        for(var old:new CompoundTag[]{oldA,oldB}){
            var actual=region(old.getIntOr("id",0));
            for(String key:new String[]{"id","dimension","roomId","x1m","x2m","y1m","y2m","z1m","z2m","rotationY","flipY"})check(actual.get(key).equals(old.get(key)),"migration preserves "+key);
            check(!actual.contains("pairId") && !actual.contains("partnerId"),"pair membership removed");
        }
        for(int i=0;i<oldActions.size();i++)check(document().getListOrEmpty("actions").get(i).equals(oldActions.get(i)),"old Action unchanged");
        var migrated=document().copy();cmd("function space_editor:load");check(document().equals(migrated),"migration is idempotent");
        // Broken legacy reference is warned, never destructively repaired.
        cmd("data modify storage space_editor:document regionPairs append value {id:990001,kind:\"space_link\",a:990002,b:990003}");
        var broken=document().copy();cmd("function space_editor:load");check(document().equals(broken),"invalid migration preserves entire Document");
        check(!runtime().getListOrEmpty("spaceLinkWarnings").isEmpty(),"invalid migration warning");
        cmd("data remove storage space_editor:document regionPairs[{id:990001}]");
        // A stale unmarked pair that points at new membership cannot override it.
        cmd("data remove storage space_editor:document regionPairs[0].spaceLinkGroupId");
        var mixed=document().copy();cmd("function space_editor:space_group/migrate");check(document().equals(mixed),"new format wins over conflicting old record");
        cmd("data modify storage space_editor:document regionPairs[0].spaceLinkGroupId set value "+gid);
        int third=groupAdd(legacy,40000),fourth=groupAdd(legacy,60000);
        check(group(gid).getListOrEmpty("members").size()==4,"three and four member append");
        for(int id:new int[]{legacy,legacyB,third}){select(id,"mask",0);pcmd("function space_editor:mask/create_selected");}
        check(document().getListOrEmpty("masks").size()==3,"group members have independent Masks");
        var savedMasks=document().getListOrEmpty("masks").copy();
        int independent=plain(),independentB=groupAdd(independent,-20000);
        check(region(independent).getIntOr("spaceLinkGroupId",0)!=gid,"independent new two member group");
        cmd("data modify storage space_editor:runtime pairCandidate set from storage space_editor:document regions[{id:"+independentB+"}]");
        var before=document().copy();cmd("function space_editor:space_group/add {source:"+legacy+"}");check(document().equals(before),"foreign membership cannot be silently merged");
        cmd("data modify storage space_editor:runtime pairCandidate set from storage space_editor:document regions[{id:"+legacy+"}]");
        for(String key:new String[]{"pairId","partnerId","spaceLinkGroupId","legacyPairId"})cmd("data remove storage space_editor:runtime pairCandidate."+key);
        var validCandidate=runtime().getCompoundOrEmpty("pairCandidate").copy();
        for(String invalid:new String[]{"dimension set value \"test:unknown\"","x2m set value 500000001","x2m set value -1000","rotationY set value 45","flipY set value 2b"}){
            cmd("data modify storage space_editor:runtime pairCandidate set value "+validCandidate);
            cmd("data modify storage space_editor:runtime pairCandidate."+invalid);
            before=document().copy();cmd("function space_editor:space_group/add {source:"+legacy+"}");
            check(document().equals(before),"invalid candidate does not partially create group or IDs: "+invalid);
        }
        // All 8x8 source/target poses, with a third differently posed member.
        // Independent normal-vector oracle checks the moved AND fixed faces.
        pcmd("function space_editor:play");
        for(int ar=0;ar<4;ar++)for(int af=0;af<2;af++)for(int br=0;br<4;br++)for(int bf=0;bf<2;bf++){
            pose(legacy,ar*90,af);pose(legacyB,br*90,bf);pose(third,((br+1)%4)*90,1-bf);
            for(int face=0;face<6;face++){
                var originals=new CompoundTag[]{region(legacy).copy(),region(legacyB).copy(),region(third).copy(),region(fourth).copy()};
                select(legacy,"resize_face",face);measured("function space_editor:region/resize_face");
                int[] normal={0,0,0};normal[face/2]=face%2==0?-1:1;
                for(var old:originals){
                    int[] mapped=turn(turn(normal,-ar,af==1),old.getIntOr("rotationY",0)/90,old.getBooleanOr("flipY",false));
                    var now=region(old.getIntOr("id",0));
                    for(int axis=0;axis<3;axis++)for(int edge=1;edge<=2;edge++){
                        String key="xyz".charAt(axis)+""+edge+"m";
                        int delta=mapped[axis]<0 && edge==1?-100:mapped[axis]>0 && edge==2?100:0;
                        check(now.getIntOr(key,0)==old.getIntOr(key,0)+delta,"group local face and fixed opposite face");
                    }
                    check(java.util.Arrays.equals(now.getIntArray("localSize").orElseThrow(),group(gid).getIntArray("localSize").orElseThrow()),"shared localSize");
                }
                crouch(true);select(legacy,"resize_face",face);pcmd("function space_editor:region/resize_face");crouch(false);
                for(var old:originals)check(region(old.getIntOr("id",0)).equals(old),"group grow shrink exact inverse");
            }
        }
        var all=regions().copy();select(third,"move",1);pcmd("function space_editor:region/move");
        for(var v:all){var old=(CompoundTag)v;if(old.getIntOr("id",0)!=third)check(region(old.getIntOr("id",0)).equals(old),"move only selected group member");}
        all=regions().copy();pose(third,270,1);
        for(var v:all){var old=(CompoundTag)v;if(old.getIntOr("id",0)!=third)check(region(old.getIntOr("id",0)).equals(old),"pose only selected member");}
        check(document().getListOrEmpty("masks").equals(savedMasks),"group move/pose/resize retain Mask definitions and settings");
        select(third,"mask",0);cmd("data modify storage space_editor:runtime currentMask set from storage space_editor:document masks[{regionId:"+third+"}]");cmd("function space_editor:mask/prepare");
        near(runtime().getCompoundOrEmpty("maskRender").getDoubleOr("x1",999),region(third).getDoubleOr("x1",999),"Mask render follows moved member bounds");
        all=regions().copy();select(legacy,"resize_all",0);pcmd("function space_editor:region/resize_all");
        crouch(true);select(legacy,"resize_all",0);pcmd("function space_editor:region/resize_all");crouch(false);check(regions().equals(all),"whole group size round trip");
        // Failure at final member: all preceding staged edits must be discarded.
        pose(fourth,0,0);
        cmd("data modify storage space_editor:document regions[{id:"+fourth+"}].y1m set value 316000");
        cmd("data modify storage space_editor:document regions[{id:"+fourth+"}].y2m set value 320000");
        pose(legacy,0,0);before=document().copy();select(legacy,"resize_face",3);pcmd("function space_editor:region/resize_face");
        check(document().equals(before),"late member height failure rolls back all data and Actions");
        cmd("data modify storage space_editor:document regions[{id:"+fourth+"}].y1m set value 80000");
        cmd("data modify storage space_editor:document regions[{id:"+fourth+"}].y2m set value 84000");
        // Composition and inverses across ALL three endpoint poses, fractional negative point.
        for(int a=0;a<8;a++)for(int b=0;b<8;b++)for(int c=0;c<8;c++){
            String fa=frame((a/2)*90,a%2,0),fb=frame((b/2)*90,b%2,20000),fc=frame((c/2)*90,c%2,40000);
            cmd("data modify storage space_editor:runtime map set value {source:"+fa+",target:"+fc+",point:[-0.5005d,80.1235d,0.1005d],vector:[0.1d,-0.2d,0.3d],yaw:-0.1f,pitch:30.123f}");cmd("function space_editor:mapping/position");
            var direct=runtime().getCompoundOrEmpty("map").getCompoundOrEmpty("result").copy();
            cmd("data modify storage space_editor:runtime map.target set value "+fb);cmd("function space_editor:mapping/position");
            for(String key:new String[]{"point","vector","yaw","pitch"})cmd("data modify storage space_editor:runtime map."+key+" set from storage space_editor:runtime map.result."+key);
            cmd("data modify storage space_editor:runtime map.source set value "+fb);cmd("data modify storage space_editor:runtime map.target set value "+fc);cmd("function space_editor:mapping/position");
            check(runtime().getCompoundOrEmpty("map").getCompoundOrEmpty("result").equals(direct),"A-B-C equals A-C, position/vector/look");
        }
        // Runtime uses only containing sources, then their group's destinations.
        player.setPos(.5,80.5,1.5);pose(legacy,0,0);pose(legacyB,90,1);
        cmd("data modify storage space_editor:document regions[{id:"+third+"}].dimension set value \"minecraft:the_nether\"");
        snapshot();cmd("data modify storage space_editor:runtime spaceLinkContacts set value []");
        int cost=measured("function space_editor:link/player");
        var contacts=runtime().getListOrEmpty("spaceLinkContacts");
        // Independent group's source overlaps A: each real source has its own routes.
        int count=0;var paths=new java.util.HashSet<String>();
        for(var v:contacts){var contact=(CompoundTag)v;if(contact.getIntOr("spaceLinkGroupId",0)==gid){count++;check(contact.getIntOr("sourceRegionId",0)!=contact.getIntOr("targetRegionId",0),"no self route");paths.add(contact.getCompoundOrEmpty("projectionPathId").toString());check(contact.contains("uuid") && contact.contains("instanceId"),"identity contract");}}
        check(count==3 && paths.size()==3,"three targets including same RoomID remain distinct");
        var originalB=region(legacyB).copy();var overlap=region(legacy).copy();
        overlap.putInt("id",legacyB);overlap.putString("idText",originalB.getStringOr("idText",""));
        cmd("data modify storage space_editor:document regions[{id:"+legacyB+"}] set value "+overlap);
        snapshot();cmd("data modify storage space_editor:runtime spaceLinkContacts set value []");pcmd("function space_editor:link/player");
        int overlappingRoutes=0;paths.clear();for(var v:runtime().getListOrEmpty("spaceLinkContacts")){var c=(CompoundTag)v;if(c.getIntOr("spaceLinkGroupId",0)==gid){overlappingRoutes++;paths.add(c.getCompoundOrEmpty("projectionPathId").toString());}}
        check(overlappingRoutes==6 && paths.size()==6,"coincident Regions preserve source and target path identity");
        pcmd("function space_editor:start");pcmd("function space_editor:space_group/select_id {id:"+legacyB+"}");
        check(runtime().getCompoundOrEmpty("pairSession").getIntOr("selected",0)==legacyB,"overlapping Region selected explicitly by stable ID");
        pcmd("function space_editor:play");
        cmd("data modify storage space_editor:document regions[{id:"+legacyB+"}] set value "+originalB);
        cmd("data modify storage space_editor:runtime map set value {point:[0.5d,80.5d,1.5d],yaw:15f,pitch:25f}");
        cmd("function space_editor:space_group/map {groupId:"+gid+",source:"+legacy+",target:"+third+"}");
        check(runtime().getCompoundOrEmpty("map").getCompoundOrEmpty("result").getStringOr("dimension","").equals("minecraft:the_nether"),"group API resolves cross-dimension target");
        cmd("data modify storage space_editor:document spaceLinkGroups[{id:"+gid+"}].members append value 999999");
        cmd("data modify storage space_editor:runtime spaceLinkContacts set value []");pcmd("function space_editor:link/player");
        check(!runtime().getListOrEmpty("spaceLinkRuntimeWarnings").isEmpty(),"invalid runtime member reported and skipped");
        cmd("data remove storage space_editor:document spaceLinkGroups[{id:"+gid+"}].members[-1]");
        // Delete preserves unrelated masks; final survivor becomes reusable plain Region.
        var survivor=region(legacy).copy();var unrelated=region(independent).copy();
        for(int id:new int[]{legacyB,fourth}){select(id,"delete",0);pcmd("function space_editor:region/apply_hit");}
        check(group(gid).getListOrEmpty("members").size()==2 && region(legacy).equals(survivor),"individual deletion keeps other members");
        check(document().getListOrEmpty("masks").size()==2,"only deleted member Mask removed");
        select(third,"delete",0);pcmd("function space_editor:region/apply_hit");
        check(!region(legacy).contains("spaceLinkGroupId") && !region(legacy).contains("kind"),"one survivor is plain unconnected Region");
        check(document().getListOrEmpty("masks").size()==1 && document().getListOrEmpty("masks").getCompoundOrEmpty(0).equals(savedMasks.getCompoundOrEmpty(0)),"survivor Mask retained unchanged");
        check(region(independent).equals(unrelated),"other group untouched");
        groupAdd(legacy,40000);check(region(legacy).contains("spaceLinkGroupId"),"survivor reusable as group source");
        var saved=document().copy();cmd("function space_editor:load");check(document().equals(saved),"new groups survive reload unchanged");
        groupUiTests(legacy);
        groupLoadTests();
        System.out.println("SPACE_LINK_GROUP_PASS: migration/idempotence/conflict, 2/3/4 members, 384 local faces across four members, 512 composition triples, atomic rollback, individual deletion/dissolution, reload, same-room routes, dimension; contact_commands="+cost);
    }
    static void groupLoadTests(){
        cmd("data modify storage space_editor:document regions set value []");cmd("data modify storage space_editor:document regionPairs set value []");
        cmd("data modify storage space_editor:document spaceLinkGroups set value []");cmd("data modify storage space_editor:document masks set value []");
        int a=plain();player.setPos(.5,80.5,1.5);pcmd("function space_editor:play");
        int maxAdd=0,maxContact=0;
        for(int n=2;n<=64;n++){
            groupAdd(a,100000+n*10000);
            if(n==4 || n==8 || n==16 || n==32 || n==64){
                snapshot();cmd("data modify storage space_editor:runtime spaceLinkContacts set value []");
                int used=measured("function space_editor:link/player");maxContact=Math.max(maxContact,used);
                check(runtime().getListOrEmpty("spaceLinkContacts").size()==n-1,"load test all targets present");
                System.out.println("SPACE_LINK_GROUP_LOAD: members="+n+" contact_commands="+used);
            }
        }
        select(a,"resize_face",1);int editCost=measured("function space_editor:region/resize_face");
        int gid=region(a).getIntOr("spaceLinkGroupId",0);
        for(var v:regions())check(java.util.Arrays.equals(((CompoundTag)v).getIntArray("localSize").orElseThrow(),group(gid).getIntArray("localSize").orElseThrow()),"64 member transaction complete");
        var other=namedPlayer("group-load-two");other.setNoGravity(true);other.setPos(1,81,2);
        var list=helper.getLevel().getServer().getPlayerList().getPlayers();boolean add=!list.contains(player);if(add)list.add(player);
        try{int used=measured("function space_editor:teleport/tick");check(runtime().getListOrEmpty("spaceLinkContacts").size()==126,"two players at group capacity");System.out.println("SPACE_LINK_GROUP_LOAD: members=64 players=2 tick_commands="+used+" edit_commands="+editCost);}
        finally{if(add)list.remove(player);helper.getLevel().getServer().getPlayerList().remove(other);}
        groupAdd(a,800000);check(group(gid).getListOrEmpty("members").size()==65,"group is not limited to 64 members");
    }
    static void groupUiTests(int a){
        pcmd("function space_editor:start");
        pcmd("item replace entity @s weapon.mainhand with minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"space_link\"}}]");
        pcmd("function space_editor:pair/held_space_link");select(a,"pair_select",0);pcmd("function space_editor:pair/select");
        int gid=region(a).getIntOr("spaceLinkGroupId",0),count=group(gid).getListOrEmpty("members").size();
        check(runtime().contains("pairPending"),"existing group starts add session");
        for(int i=0;i<2;i++){
            pcmd("function space_editor:pair/confirm");
            check(group(gid).getListOrEmpty("members").size()==++count && runtime().contains("pairPending"),"consecutive UI placement keeps pending session");
        }
        var saved=document().copy();pcmd("item replace entity @s weapon.mainhand with minecraft:air");cmd("function space_editor:tick");
        check(!runtime().contains("pairPending") && document().equals(saved),"switching tools discards only pending preview");
        pcmd("function space_editor:pair/held_space_link");crouch(true);select(a,"pair_select",0);pcmd("function space_editor:pair/select");
        check(!runtime().contains("pairPending") && runtime().getCompoundOrEmpty("pairSession").getStringOr("mode","").equals("pose"),"first Shift selection explicitly targets existing Region pose");
        crouch(false);
        var other=namedPlayer("group-editor-other");var originalPlayer=player;var session=runtime().getCompoundOrEmpty("pairSession").copy();
        try{player=other;pcmd("function space_editor:start");pcmd("function space_editor:pair/held_space_link");check(runtime().getCompoundOrEmpty("pairSession").equals(session),"second editor cannot overwrite owner session");}
        finally{player=originalPlayer;helper.getLevel().getServer().getPlayerList().remove(other);}
        cmd("function space_editor:load");check(!runtime().contains("pairPending") && !runtime().contains("pairSession"),"reload clears transient editor state");
        pcmd("function space_editor:pair/held_space_link");select(a,"pair_select",0);pcmd("function space_editor:pair/select");
        pcmd("tag @s remove space_editor.editing");cmd("function space_editor:space_group/session_tick");
        check(!runtime().contains("pairPending") && !runtime().contains("pairSession"),"missing editor owner releases transient session");
        pcmd("function space_editor:play");
    }
    static int editMaxCommands;
    static int measured(String command){
        var actor=player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS);
        var holder=new java.util.concurrent.atomic.AtomicReference<net.minecraft.commands.execution.ExecutionContext<CommandSourceStack>>();
        net.minecraft.commands.Commands.executeCommandInContext(actor,context->{
            holder.set(context);
            helper.getLevel().getServer().getCommands().performPrefixedCommand(actor,command);
        });
        try{
            var type=net.minecraft.commands.execution.ExecutionContext.class;
            var limit=type.getDeclaredField("commandLimit");limit.setAccessible(true);
            var quota=type.getDeclaredField("commandQuota");quota.setAccessible(true);
            check(limit.getInt(holder.get())==65536,"default command limit unchanged");
            int used=65536-quota.getInt(holder.get());
            check(used<65536,"edit completes within command budget");
            editMaxCommands=Math.max(editMaxCommands,used);return used;
        }catch(ReflectiveOperationException ex){throw new AssertionError(ex);}
    }
    static void box(int id,int x1,int y1,int z1,int x2,int y2,int z2){
        var r=new CompoundTag();r.putInt("id",id);r.putString("idText","region_"+id);r.putString("dimension","minecraft:overworld");
        var min=new ListTag();var max=new ListTag();int[] a={x1,y1,z1},b={x2,y2,z2};
        for(int i=0;i<3;i++){
            String axis="xyz".substring(i,i+1);r.putInt(axis+"1m",a[i]);r.putInt(axis+"2m",b[i]);r.putInt("s"+axis+"m",b[i]-a[i]);
            r.putDouble(axis+"1",a[i]*.001);r.putDouble(axis+"2",b[i]*.001);r.putDouble("s"+axis,(b[i]-a[i])*.001);
            min.add(DoubleTag.valueOf(a[i]*.001));max.add(DoubleTag.valueOf(b[i]*.001));
        }
        r.put("min",min);r.put("maxExclusive",max);
        cmd("data modify storage space_editor:document regions append value "+r);
    }
    static java.util.Map<java.util.UUID,net.minecraft.world.phys.Vec3> displays(String tag){
        var result=new java.util.HashMap<java.util.UUID,net.minecraft.world.phys.Vec3>();
        for(var e:helper.getLevel().getAllEntities())if(!e.isRemoved() && e.entityTags().contains(tag))result.put(e.getUUID(),e.position());
        return result;
    }
    static void rayMove(double x,double y,double z,float yaw,float pitch){
        // Independent oracle: the original exhaustive, first-sample/list-order
        // algorithm, using Minecraft's own local-coordinate implementation.
        var actor=player.createCommandSourceStack().withPosition(new net.minecraft.world.phys.Vec3(x,y,z)).withRotation(new net.minecraft.world.phys.Vec2(pitch,yaw)).withAnchor(net.minecraft.commands.arguments.EntityAnchorArgument.Anchor.EYES);
        CompoundTag expected=null;int face=-1;
        for(int step=0;step<=512 && expected==null;step++){
            var p=new net.minecraft.commands.arguments.coordinates.LocalCoordinates(0,0,step*.025).getPosition(actor);
            int[] pos={(int)Math.floor(p.x*1000),(int)Math.floor(p.y*1000),(int)Math.floor(p.z*1000)};
            for(var value:regions()){
                var r=(CompoundTag)value;if(!r.getStringOr("dimension","").equals("minecraft:overworld"))continue;
                boolean inside=true;int best=Integer.MAX_VALUE,f=0;
                for(int i=0;i<3;i++){
                    String a="xyz".substring(i,i+1);int lo=r.getIntOr(a+"1m",0),hi=r.getIntOr(a+"2m",0);
                    if(pos[i]<lo || pos[i]>=hi)inside=false;
                    if(pos[i]-lo<best){best=pos[i]-lo;f=i*2;}
                    if(hi-pos[i]<best){best=hi-pos[i];f=i*2+1;}
                }
                if(inside){expected=r.copy();face=f;break;}
            }
        }
        var before=regions().copy();
        measured(String.format(java.util.Locale.ROOT,"execute positioned %.9f %.9f %.9f rotated %.5f %.5f run function space_editor:input/move",x,y,z,yaw,pitch));
        if(expected==null){check(!runtime().contains("hit") && regions().equals(before),"miss preserves all records");return;}
        int id=expected.getIntOr("id",0);check(runtime().getCompoundOrEmpty("hit").getIntOr("id",0)==id,"legacy sampled overlap priority");
        check(runtime().getIntOr("hitFace",-1)==face,"legacy nearest face, including inside");
        int delta=(face%2==0?-1000:1000)*(player.isCrouching()?-1:1);
        for(int i=0;i<3;i++)for(int edge=1;edge<=2;edge++){
            String key="xyz".substring(i,i+1)+edge+"m";
            check(region(id).getIntOr(key,0)==expected.getIntOr(key,0)+(i==face/2?delta:0),"exact milliblock move");
        }
        check(regions().size()==before.size(),"move keeps every saved Region");
        for(var value:before){var r=(CompoundTag)value;if(r.getIntOr("id",0)!=id)check(region(r.getIntOr("id",0)).equals(r),"unselected data unchanged");}
        for(var e:helper.getLevel().getAllEntities())check(!e.entityTags().contains("space_editor.ray_probe") && !e.entityTags().contains("space_editor.ray_sample"),"ray markers cleaned");
    }
    static void regionEditTests() throws Exception{
        cmd("function space_editor:preview/hide");
        cmd("data modify storage space_editor:document regions set value []");cmd("data modify storage space_editor:document regionPairs set value []");
        cmd("data modify storage space_editor:document masks set value []");cmd("data modify storage space_editor:document actions set value []");
        cmd("data remove storage space_editor:runtime pastePending");cmd("data remove storage space_editor:runtime hit");
        cmd("data modify storage space_editor:document editMode set value 1b");
        cmd("data modify storage space_editor:document settings.regionsVisible set value 1b");
        // 32 early misses plus a distant hit exceeded 65536 in the old ray.
        for(int i=1;i<=32;i++)box(i,2000,80000,-1000,3000,84000,1000);
        box(100,123,80001,234,1124,84002,1235);
        cmd("function space_editor:preview/resync");
        check(displays("space_editor.region").size()==33,"33 Region displays initially present");
        var untouched=displays("space_editor.region");var labels=displays("space_editor.label");
        // Exclude only the selected Region's box/label from UUID invariants.
        cmd("execute as @e[scores={se.id=100}] run tag @s add editor_test.target");
        for(var e:helper.getLevel().getAllEntities())if(e.entityTags().contains("editor_test.target")){untouched.remove(e.getUUID());labels.remove(e.getUUID());}
        for(int n=0;n<24;n++){
            var r=region(100);rayMove(.5,81.5,r.getDoubleOr("z1",0)-11.5,0,0);
            check(displays("space_editor.region").size()==33 && displays("space_editor.label").size()==33,"24 far moves keep all frames/labels");
            check(displays("space_editor.region").entrySet().containsAll(untouched.entrySet()),"other Region UUIDs and positions preserved");
            check(displays("space_editor.label").entrySet().containsAll(labels.entrySet()),"other labels preserved");
        }
        var r=region(100);player.setShiftKeyDown(true);player.setPose(net.minecraft.world.entity.Pose.CROUCHING);
        rayMove(.5,81.5,r.getDoubleOr("z1",0)-.125,0,0);
        player.setShiftKeyDown(false);player.setPose(net.minecraft.world.entity.Pose.STANDING);
        r=region(100);rayMove(.5,81.5,r.getDoubleOr("z1",0)+.5,0,0); // inside
        int beforeX1=region(100).getIntOr("x1m",0),beforeX2=region(100).getIntOr("x2m",0);
        select(100,"resize_face",1);measured("function space_editor:region/resize_face");
        check(region(100).getIntOr("x2m",0)==beforeX2+100,"fractional face resize");
        select(100,"resize_all",0);measured("function space_editor:region/resize_all");
        check(region(100).getIntOr("x1m",0)==beforeX1-100 && region(100).getIntOr("x2m",0)==beforeX2+200,"fractional whole resize");
        select(100,"mask_create",0);pcmd("function space_editor:mask/create_selected");
        var maskRecord=document().getListOrEmpty("masks").copy();
        double maskZ=0;for(var e:helper.getLevel().getAllEntities())if(e.entityTags().contains("space_editor.mask_body"))maskZ=e.getZ();
        r=region(100);rayMove((r.getDoubleOr("x1",0)+r.getDoubleOr("x2",0))/2,81.5,r.getDoubleOr("z1",0)-1,0,0);
        for(var e:helper.getLevel().getAllEntities())if(!e.isRemoved() && e.entityTags().contains("space_editor.mask_body"))near(e.getZ(),maskZ-1,"Mask follows move");
        check(document().getListOrEmpty("masks").equals(maskRecord),"Mask saved metadata unchanged");
        check(displays("space_editor.mask_body").size()==1 && displays("space_editor.mask_guide").size()==1,"no duplicate Mask entities");
        measured("function space_editor:preview/resync");check(displays("space_editor.region").size()==33,"manual full resync still works");
        // Paired edits refresh only the affected member(s), including all
        // direction labels/arrows and attached Masks; IDs can overlap Mask IDs.
        cmd("data modify storage space_editor:document nextId set value 300");
        int paired=pair("teleport"),partner=region(paired).getIntOr("partnerId",0);
        select(partner,"mask_create",0);pcmd("function space_editor:mask/create_selected");
        pcmd("function space_editor:preview/resync");
        var partnerDisplays=new java.util.HashSet<java.util.UUID>();
        cmd("execute as @e[scores={se.id="+partner+"}] run tag @s add editor_test.partner");
        for(var e:helper.getLevel().getAllEntities())if(e.entityTags().contains("editor_test.partner"))partnerDisplays.add(e.getUUID());
        select(paired,"move",1);measured("function space_editor:region/move");
        var all=new java.util.HashSet<java.util.UUID>();for(var e:helper.getLevel().getAllEntities())if(!e.isRemoved())all.add(e.getUUID());
        check(all.containsAll(partnerDisplays),"pair move preserves partner frames/directions");
        int pairX=region(paired).getIntOr("x1m",0),partnerX=region(partner).getIntOr("x1m",0);
        select(paired,"resize_face",0);measured("function space_editor:region/resize_face");
        check(region(paired).getIntOr("x1m",0)==pairX-100 && region(partner).getIntOr("x1m",0)==partnerX-100,"paired face resize remains synchronized");
        check(displays("space_editor.region").size()==35,"paired resize keeps unrelated frames");
        check(displays("space_editor.direction_front").size()==2 && displays("space_editor.direction_up").size()==2,"paired arrows do not accumulate");
        check(displays("space_editor.label").size()==43,"paired labels do not accumulate");
        measured("function space_editor:pair/set_pose {id:"+paired+",rotationY:90,flipY:1}");
        select(paired,"resize_all",0);measured("function space_editor:region/resize_all");
        check(java.util.Arrays.equals(region(paired).getIntArray("localSize").orElseThrow(),region(partner).getIntArray("localSize").orElseThrow()),"rotated paired whole resize stays synchronized");
        for(var e:helper.getLevel().getAllEntities())if(e.entityTags().contains("space_editor.mask_body")){
            // Mask #2 follows partner #301, not Region #2 with the same score.
            if(e.getX()>10)near(e.getX(),region(partner).getDoubleOr("x1",0),"paired Mask position synchronized");
        }
        pcmd("function space_editor:region/display/hide");select(paired,"move",1);measured("function space_editor:region/move");
        check(displays("space_editor.region").isEmpty() && displays("space_editor.label").isEmpty() && displays("space_editor.mask_guide").isEmpty(),"hidden Region edits do not reveal frames/labels/guides");
        check(displays("space_editor.mask_body").size()==2,"hidden edits retain Mask bodies");
        pcmd("function space_editor:region/display/show");select(paired,"delete",0);measured("function space_editor:region/apply_hit");
        check(displays("space_editor.region").size()==33 && displays("space_editor.direction_front").isEmpty(),"pair deletion removes only pair displays");
        check(document().getListOrEmpty("masks").size()==1,"pair deletion removes only attached Mask");
        pcmd("function space_editor:play");select(100,"move",1);measured("function space_editor:region/move");
        check(displays("space_editor.preview").isEmpty() && displays("space_editor.mask_body").size()==1,"play edit keeps only persistent Mask");
        cmd("data modify storage space_editor:document editMode set value 1b");
        // Thin, negative, diagonal, descending, overlapping and miss rays.
        cmd("data modify storage space_editor:document masks set value []");
        cmd("data modify storage space_editor:document regions set value []");
        box(201,-1234,80001,-1234,1235,84002,1235);box(202,-1234,80001,-1234,1235,84002,1235);
        rayMove(.25,81.5,-10,0,0); // equal-distance list order
        rayMove(10,81.5,0,90,0);rayMove(-10,81.5,-10,-45,0);rayMove(0,90,0,0,90);rayMove(0,70,0,0,-90);
        rayMove(10,81.5,10,0,0);
        cmd("data modify storage space_editor:document regions set value []");box(203,-1,80000,-1,0,84000,1000);
        rayMove(-.0005,81.5,-2,0,0); // one-milliblock width
        // Paste preview wins a same-sample tie against an ordinary Region.
        box(204,0,80000,0,1000,84000,1000);
        cmd("data modify storage space_editor:runtime pastePending set value {targetDimension:\"minecraft:overworld\",x:0,y:80,z:0,sx:1,sy:4,sz:1}");
        var saved=regions().copy();measured("execute positioned 0.5 81.5 -1 rotated 0 0 run function space_editor:input/delete");
        check(!runtime().contains("pastePending") && regions().equals(saved),"Paste cancel priority preserved");
        cmd("data modify storage space_editor:runtime pastePending set value {targetDimension:\"minecraft:overworld\",x:0,y:80,z:0,sx:1,sy:4,sz:1}");
        measured("execute positioned 0.5 81.5 -1 rotated 0 0 run function space_editor:input/move");
        near(runtime().getCompoundOrEmpty("pastePending").getDoubleOr("z",999),-1,"Paste move priority preserved");
        check(regions().equals(saved),"Paste movement does not edit Region");cmd("data remove storage space_editor:runtime pastePending");
        var config=com.google.gson.JsonParser.parseString(Files.readString(Path.of("space_editor_blocks.json"))).getAsJsonObject();
        String fence=config.getAsJsonObject("collisionCarriers").get("fence").getAsString();
        cmd("setblock 0 83 0 "+fence);
        measured("execute positioned 0.5 81.5 -1 rotated 0 0 run function space_editor:input/delete");
        check(helper.getLevel().getBlockState(new net.minecraft.core.BlockPos(0,83,0)).isAir() && regions().equals(saved),"special collision deletion precedes Region selection");
        System.out.println("SPACE_EDITOR_REGION_EDIT_PASS: 33 Regions, 24 far moves, near/inside/Shift, fractional/thin/diagonal/vertical/overlap/miss, resize, Mask, UUID preservation, resync; max_commands="+editMaxCommands+" limit=65536");
    }
    static void fillOffhandTests(){
        String[] items={"minecraft:gold_block","minecraft:air","minecraft:water_bucket","minecraft:lava_bucket","minecraft:bucket"};
        String[] blocks={"minecraft:gold_block","minecraft:air","minecraft:water","minecraft:lava","minecraft:stone"};
        for(int i=0;i<items.length;i++){
            int id=9000+i;box(id,8000,80000,8000,9000,81000,9000);
            cmd("setblock 8 80 8 minecraft:stone");
            cmd("data modify storage space_editor:runtime hover set value {dimension:\"minecraft:overworld\",pos:[I;8,80,8],x:8,y:80,z:8}");
            pcmd("item replace entity @s weapon.offhand with "+items[i]);
            int before=regions().size();var saved=region(id).copy();
            pcmd("function space_editor:input/fill");
            var expected=net.minecraft.core.registries.BuiltInRegistries.BLOCK.getValue(Identifier.parse(blocks[i]));
            var actual=helper.getLevel().getBlockState(new net.minecraft.core.BlockPos(8,80,8));
            check(actual.is(expected),"offhand fill result for "+items[i]);
            boolean supported=i<4;
            check(regions().size()==before-(supported?1:0),"only successful fills remove their Region");
            if(!supported)check(region(id).equals(saved),"unsupported bucket preserves saved Region");
            if(i==2 || i==3)check(actual.getFluidState().isSource(),"bucket fills place fluid sources");
            if(i==1)check(runtime().getStringOr("fillBlock","").equals("minecraft:air"),"empty offhand clears preceding material");
        }
        pcmd("item replace entity @s weapon.offhand with minecraft:air");
        cmd("setblock 8 80 8 minecraft:air");
        System.out.println("SPACE_EDITOR_FILL_OFFHAND_PASS: empty=air, water/lava buckets=source fluids, ordinary block unchanged, unsupported bucket preserves Region");
    }
    static void test(GameTestHelper h){
        helper=h;source=h.getLevel().getServer().createCommandSourceStack();
        cmd("function space_editor:load");cmd("forceload add -48 -48 80 48");cmd("execute in minecraft:the_nether run forceload add 16 -16 32 16");
        player=h.makeMockServerPlayerInLevel();player.setNoGravity(true);player.setPos(.5,82,-2.5);
        final boolean[] done={false};final int[] ticks={0};
        h.onEachTick(()->{
            if(done[0])return;
            try{
                cmd("execute store success storage space_editor:runtime testLoaded byte 1 if loaded 0 80 0");
                if(!runtime().getBooleanOr("testLoaded",false)){if(++ticks[0]>100)throw new AssertionError("test chunks not loaded");return;}
                cmd("execute in minecraft:the_nether store success storage space_editor:runtime netherLoaded byte 1 if loaded 22 80 1");
                if(!runtime().getBooleanOr("netherLoaded",false)){if(++ticks[0]>2000){for(var level:h.getLevel().getServer().getAllLevels())System.out.println("TEST_LEVEL "+level.dimension());throw new AssertionError("Nether test chunks not loaded");}return;}
                regionEditTests();fillOffhandTests();mappingTests();pairTests();uiTests();teleportTests();groupTests();
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
