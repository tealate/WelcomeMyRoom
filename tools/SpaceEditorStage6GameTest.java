// Formal Stage06 acceptance tests on the official 26.1 server, isolated world only.
import java.nio.file.*;
import java.util.*;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.nbt.*;
import net.minecraft.world.entity.*;

public class SpaceEditorStage6GameTest {
    static GameTestHelper helper;
    static CommandSourceStack source;
    static net.minecraft.server.level.ServerPlayer player, second;
    static java.util.concurrent.CompletableFuture<Void> reload;
    static Set<Integer> reloadIds;
    static final Identifier DOCUMENT=Identifier.parse("space_editor:document"), RUNTIME=Identifier.parse("space_editor:runtime"), PROJECTION=Identifier.parse("space_editor:projection");
    static CompoundTag state(){return helper.getLevel().getServer().getCommandStorage().get(PROJECTION);}
    static CompoundTag runtime(){return helper.getLevel().getServer().getCommandStorage().get(RUNTIME);}
    static void cmd(String s){helper.getLevel().getServer().getCommands().performPrefixedCommand(source,s);}
    static void pcmd(String s){helper.getLevel().getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS),s);}
    static boolean matches(String s){cmd("execute store success storage space_editor:projection test byte 1 run "+s);return state().getBooleanOr("test",false);}
    static void check(boolean ok,String message){if(!ok)throw new AssertionError(message+" active="+state().getListOrEmpty("active"));}
    static void near(double a,double b,String message){check(Math.abs(a-b)<0.0011,message+" actual="+a+" expected="+b);}
    static net.minecraft.server.level.ServerPlayer namedPlayer(String name){
        var server=helper.getLevel().getServer();
        var cookie=net.minecraft.server.network.CommonListenerCookie.createInitial(new com.mojang.authlib.GameProfile(UUID.randomUUID(),name),false);
        var p=new net.minecraft.server.level.ServerPlayer(server,helper.getLevel(),cookie.gameProfile(),cookie.clientInformation());
        var connection=new net.minecraft.network.Connection(net.minecraft.network.protocol.PacketFlow.SERVERBOUND);
        new io.netty.channel.embedded.EmbeddedChannel(connection);server.getPlayerList().placeNewPlayer(connection,p,cookie);
        p.setNoGravity(true);p.setPos(-2,81,1);return p;
    }
    static List<CompoundTag> routes(){var out=new ArrayList<CompoundTag>();for(var t:state().getListOrEmpty("active"))out.add((CompoundTag)t);return out;}
    static int owner(){pcmd("execute store result storage space_editor:projection testOwner int 1 run scoreboard players get @s pr.owner");return state().getIntOr("testOwner",0);}
    static CompoundTag route(int target){int own=owner();return routes().stream().filter(r->r.getIntOr("owner",0)==own&&r.getIntOr("targetId",0)==target).findFirst().orElseThrow(()->new AssertionError("missing target "+target+" "+routes()));}
    static net.minecraft.world.entity.decoration.Mannequin body(int id,boolean debug){
        cmd("tag @e[type=minecraft:mannequin,tag=space_editor.proxy] remove test.selected");
        cmd("tag @e[type=minecraft:mannequin,tag=space_editor.proxy,tag=pr."+(debug?"debug":"production")+",scores={pr.id="+id+"},limit=1] add test.selected");
        return helper.getLevel().getEntities(EntityType.MANNEQUIN,e->e.isAlive()&&e.entityTags().contains("test.selected")).stream().findFirst().orElseThrow(()->new AssertionError("missing body "+id+" debug="+debug+" state="+state()));
    }
    static List<? extends net.minecraft.world.entity.decoration.Mannequin> bodies(boolean debug){return helper.getLevel().getEntities(EntityType.MANNEQUIN,e->e.isAlive()&&e.entityTags().contains("space_editor.proxy")&&e.entityTags().contains(debug?"pr.debug":"pr.production"));}
    static List<? extends net.minecraft.world.entity.decoration.Mannequin> removing(){return helper.getLevel().getEntities(EntityType.MANNEQUIN,e->e.isAlive()&&e.entityTags().contains("pr.removing"));}
    static List<? extends net.minecraft.world.entity.Display.TextDisplay> labels(boolean debug){return helper.getLevel().getEntities(EntityType.TEXT_DISPLAY,e->e.entityTags().contains("space_editor.proxy")&&e.entityTags().contains(debug?"pr.debug":"pr.production"));}
    static String text(net.minecraft.world.entity.Display.TextDisplay e){try{var m=e.getClass().getDeclaredMethod("getText");m.setAccessible(true);return ((net.minecraft.network.chat.Component)m.invoke(e)).getString();}catch(Exception ex){throw new AssertionError(ex);}}
    static void tick(){cmd("function space_editor:projection/maintenance");cmd("function space_editor:teleport/tick");}
    static void finishDeletes(){for(int i=0;i<6;i++)cmd("function space_editor:projection/maintenance");}
    static boolean loaded(int x,int z){cmd("execute store success storage space_editor:projection testLoaded byte 1 run execute if loaded "+x+" 81 "+z);return state().getBooleanOr("testLoaded",false);}
    static void at(double x,double y,double z,float yaw,float pitch){player.setPos(x,y,z);player.setYRot(yaw);player.setXRot(pitch);}
    static void frame(int id,int x,int z,String kind,int rotation,int flip,String room){
        cmd("data modify storage space_editor:runtime frame set value {id:"+id+",kind:\""+kind+"\",roomId:\""+room+"\",dimension:\"minecraft:overworld\",rotationY:"+rotation+",flipY:"+flip+"b,x1m:"+(x*1000)+",x2m:"+((x+4)*1000)+",y1m:80000,y2m:84000,z1m:"+(z*1000)+",z2m:"+((z+4)*1000)+"}");
        cmd("function space_editor:pair/frame");cmd("data modify storage space_editor:document regions append from storage space_editor:runtime frame");
    }
    static void existence(int id,int x1,int x2,int z1,int z2,String room){
        cmd("data modify storage space_editor:document regions append value {id:"+id+",kind:\"proxy_existence\",roomId:\""+room+"\",dimension:\"minecraft:overworld\",x1m:"+x1+",x2m:"+x2+",y1m:76000,y2m:90000,z1m:"+z1+",z2m:"+z2+"}");
    }
    static void fixture(int n){
        cmd("function space_editor:projection/clear");
        cmd("data modify storage space_editor:document regions set value []");cmd("data modify storage space_editor:document regionPairs set value []");
        cmd("data modify storage space_editor:document spaceLinkGroups set value []");cmd("data modify storage space_editor:document editMode set value 0b");
        cmd("data modify storage space_editor:document projection.debugMaps set value []");
        cmd("scoreboard players set @a pr.debug 0");cmd("scoreboard players set @a se.tp_lock 0");cmd("scoreboard players set @a se.tp_cd 0");
        for(int i=0;i<n;i++){
            frame(i+1,i*12,0,"space_link",i==1?90:i==2?180:0,i>0?1:0,"room_"+(i+1));
            cmd("data modify storage space_editor:document regions[{id:"+(i+1)+"}].spaceLinkGroupId set value 1");
            existence(101+i,i*12000-4000,i*12000+8000,-4000,8000,"room_"+(i+1));
        }
        var members=new StringJoiner(",");for(int i=1;i<=n;i++)members.add(""+i);
        cmd("data modify storage space_editor:document spaceLinkGroups append value {id:1,localSize:[I;4000,4000,4000],members:["+members+"]}");
        cmd("function space_editor:projection/enable");at(-2,81,1,15,25);tick();
    }
    static void phase1(){
        fixture(2);check(routes().isEmpty(),"outside link has no path");
        pcmd("item replace entity @s armor.head with minecraft:diamond_helmet");pcmd("item replace entity @s weapon.mainhand with minecraft:diamond_sword");pcmd("item replace entity @s weapon.offhand with minecraft:shield");
        at(1,81,1,15,25);tick();check(routes().size()==1,"one route A to B");
        int id=route(2).getIntOr("id",0);var b=body(id,false);var uuid=b.getUUID();
        near(b.getX(),15,"90 degree x");near(b.getZ(),1,"90 degree z");near(b.getY(),81.1,"inverted pivot compensation");
        near(b.getYRot(),105,"yaw mapped");near(b.getXRot(),-25,"pitch flip");
        check(b.getCustomName().getString().equals("Dinnerbone"),"relative inversion trigger");check(b.getTeam().getName().equals("pr_hidden"),"hide Dinnerbone");
        check(b.getItemBySlot(EquipmentSlot.HEAD).is(net.minecraft.world.item.Items.DIAMOND_HELMET),"armor copied");check(b.getOffhandItem().is(net.minecraft.world.item.Items.SHIELD),"offhand copied");
        check(labels(false).size()==1&&text(labels(false).getFirst()).equals("ProjectorOne"),"original player name");var labelId=labels(false).getFirst().getUUID();
        check(matches("execute if data entity @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production,limit=1] {teleport_duration:3}"),"production label uses three-tick teleport interpolation");
        check(matches("execute if data entity @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production,limit=1] {transformation:{left_rotation:[0f,0f,1f,0f]}}"),"inverted production label rotates 180 degrees");
        near(labels(false).getFirst().getY(),80.9,"inverted name includes the rotated-text baseline correction");
        for(int i=0;i<8;i++)tick();check(routes().size()==1&&body(id,false).getUUID().equals(uuid),"inside contact never respawns");
        player.setShiftKeyDown(true);player.setPose(Pose.CROUCHING);tick();check(body(id,false).getPose()==Pose.CROUCHING,"pose reuse");near(body(id,false).getY(),81.4,"crouch pivot");near(labels(false).getFirst().getY(),81.2,"inverted crouching label keeps pose-specific head position and baseline correction");
        player.setShiftKeyDown(false);player.setPose(Pose.STANDING);
        cmd("data modify storage space_editor:document regions[{id:2}].flipY set value 0b");tick();
        check(body(id,false).getCustomName()==null,"flip off clears Dinnerbone trigger");check(labels(false).getFirst().getUUID().equals(labelId),"flip transition reuses label UUID");
        check(matches("execute if data entity @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production,limit=1] {transformation:{left_rotation:[0f,0f,0f,1f]}}"),"flip off restores normal label rotation");
        near(labels(false).getFirst().getY(),83.1,"normal name returns above the head");
        System.out.println("SPACE_EDITOR_STAGE6_PHASE1_PASS: mapping, label interpolation/flip/height, body/name/gear, UUID reuse");
    }
    static void phase2(){
        fixture(3);at(1,81,1,0,0);tick();check(routes().size()==2&&bodies(false).size()==2,"A projects B and C concurrently");
        var ids=new HashSet<UUID>();for(var b:bodies(false))ids.add(b.getUUID());for(int i=0;i<8;i++)tick();check(bodies(false).stream().allMatch(b->ids.contains(b.getUUID())),"stable multi-route UUIDs");
        // Different group/path to the same named room must not collapse.
        frame(11,0,0,"space_link",0,0,"room_1");frame(12,26,0,"space_link",0,0,"room_3");
        cmd("data modify storage space_editor:document regions[{id:11}].spaceLinkGroupId set value 2");cmd("data modify storage space_editor:document regions[{id:12}].spaceLinkGroupId set value 2");
        cmd("data modify storage space_editor:document spaceLinkGroups append value {id:2,localSize:[I;4000,4000,4000],members:[11,12]}");tick();
        check(routes().size()==3,"distinct route to same Room retained");for(int i=0;i<20;i++)tick();check(routes().size()==3&&bodies(false).size()==3,"mannequins never become sources or recursively multiply");
        System.out.println("SPACE_EDITOR_STAGE6_PHASE2_PASS: three-region fanout, distinct same-room paths, no growth/cycles");
    }
    static void phase3(){
        fixture(3);cmd("data modify storage space_editor:document regions[{id:103}].x1m set value 22000");cmd("data modify storage space_editor:document regions[{id:103}].x2m set value 28000");
        at(1,81,1,0,0);tick();int bid=route(2).getIntOr("id",0),cid=route(3).getIntOr("id",0);var buuid=body(bid,false).getUUID();var cuuid=body(cid,false).getUUID();
        at(5,81,1,0,0);tick();check(routes().size()==2,"outside link but inside existence stays active");
        cmd("data modify storage space_editor:document regions[{id:103}].x1m set value 22001");
        at(5.999,81,1,0,0);tick();check(routes().size()==2,"fractional existence minimum is inclusive");
        at(5.9995,81,1,0,0);tick();check(routes().size()==1&&route(2).getIntOr("id",0)==bid,"half-milliblock outside C removes only C");
        var deletingC=(net.minecraft.world.entity.decoration.Mannequin)helper.getLevel().getEntity(cuuid);check(deletingC!=null,"removed C still exists during deletion wait");check(deletingC.entityTags().contains("pr.removing"),"removed C is detached into deletion queue tags="+deletingC.entityTags());check(deletingC.hasEffect(net.minecraft.world.effect.MobEffects.INVISIBILITY),"removed C has invisibility effect during deletion wait");
        check(deletingC.getItemBySlot(EquipmentSlot.HEAD).isEmpty()&&deletingC.getMainHandItem().isEmpty(),"deleting C has no equipment");
        cmd("function space_editor:projection/maintenance");check(deletingC.getY()>0,"deleting C waits one full tick before teleport");cmd("function space_editor:projection/maintenance");near(deletingC.getY(),-63,"deleting C teleports after two ticks");
        for(int i=0;i<4;i++)cmd("function space_editor:projection/maintenance");check(!deletingC.isAlive(),"C deletion finishes four ticks after teleport");check(body(bid,false).getUUID().equals(buuid),"single-route deletion preserves B");
        at(5,81,1,0,0);tick();check(routes().size()==1,"return to existence does not reactivate");
        at(1,81,1,0,0);tick();check(routes().size()==2&&route(3).getIntOr("id",0)!=cid,"new link entry reactivates C");check(body(bid,false).getUUID().equals(buuid),"B unaffected by C recreation");
        frame(901,36,0,"region",270,0,"debug_b");frame(902,48,0,"region",0,1,"debug_c");
        pcmd("function space_editor:projection/debug/map {target:2,region:901}");pcmd("function space_editor:projection/debug/map {target:3,region:902}");pcmd("function space_editor:projection/debug/on");tick();
        check(bodies(true).size()==2,"two debug routes");near(body(bid,true).getX(),37,"debug relative room transform x");near(body(bid,true).getZ(),3,"debug relative room transform z");
        check(labels(true).stream().allMatch(l->matches("execute if data entity @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.debug,limit=1] {teleport_duration:3}")),"debug labels use three-tick teleport interpolation");
        check(body(bid,true).getCustomName()==null,"debug frame owns its own relative flip");check(labels(true).stream().allMatch(l->text(l).contains("ProjectorOne")&&text(l).contains("→")),"debug identifies owner and route");
        var debugBodies=new ArrayList<>(bodies(true));pcmd("function space_editor:projection/debug/off");check(bodies(true).isEmpty()&&labels(true).isEmpty(),"debug off immediately detaches debug bodies and names");check(body(bid,false).getUUID().equals(buuid)&&routes().size()==2,"debug off preserves production");finishDeletes();check(debugBodies.stream().noneMatch(Entity::isAlive),"debug deletion wait fully drains");
        int restoredC=route(3).getIntOr("id",0);
        cmd("data modify storage space_editor:document regions[{id:3}].x1m set value 10000000");cmd("data modify storage space_editor:document regions[{id:3}].x2m set value 10004000");
        cmd("data modify storage space_editor:document regions[{id:103}].x1m set value 9998000");cmd("data modify storage space_editor:document regions[{id:103}].x2m set value 10004000");
        check(!loaded(10000,1),"destination genuinely unloaded");tick();check(routes().size()==2&&bodies(false).size()==1,"unloaded destination retains route without stale render");
        cmd("data modify storage space_editor:document regions[{id:3}].x1m set value 24000");cmd("data modify storage space_editor:document regions[{id:3}].x2m set value 28000");
        cmd("data modify storage space_editor:document regions[{id:103}].x1m set value 22000");cmd("data modify storage space_editor:document regions[{id:103}].x2m set value 28000");tick();
        check(route(3).getIntOr("id",0)==restoredC&&bodies(false).size()==2,"loaded destination resumes existing logical route");
        cmd("data remove storage space_editor:document regions[{id:103}]");tick();check(routes().size()==1,"deleted existence removes related route");
        cmd("data modify storage space_editor:document regions[{id:2}].x1m set value 14000");cmd("data modify storage space_editor:document regions[{id:2}].x2m set value 18000");tick();near(body(bid,false).getX(),17,"live edited target bounds are used");
        var finalBodies=new ArrayList<>(bodies(false));cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:2}]");pcmd("function space_editor:region/delete_selected");tick();check(routes().isEmpty()&&bodies(false).isEmpty()&&labels(false).isEmpty(),"Region deletion detaches body and name");finishDeletes();check(finalBodies.stream().noneMatch(Entity::isAlive),"Region deletion leaves no live mannequin after wait");
        System.out.println("SPACE_EDITOR_STAGE6_PHASE3_PASS: existence exit/reentry, independent paths, debug transform/lifecycle, live editing/deletion");
    }
    static void teleportPair(){
        frame(201,0,0,"teleport",0,0,"room_1");frame(202,12,0,"teleport",90,1,"room_2");
        for(int id:new int[]{201,202}){cmd("data modify storage space_editor:document regions[{id:"+id+"}].pairId set value 1");cmd("data modify storage space_editor:document regions[{id:"+id+"}].partnerId set value "+(id==201?202:201));cmd("data modify storage space_editor:document regions[{id:"+id+"}].side set value \""+(id==201?"A":"B")+"\"");}
        cmd("data modify storage space_editor:document regionPairs append value {id:1,kind:\"teleport\",a:201,b:202,localSize:[I;4000,4000,4000],direction:\"both\",cooldownTicks:20,groupId:0,roomA:\"room_1\",roomB:\"room_2\"}");
    }
    static void phase4(){
        fixture(3);teleportPair();second=namedPlayer("ProjectorTwo");
        at(1.123456,81.234567,1.345678,15,25);second.setPos(2.123456,81.456789,2.234567);second.setYRot(35);second.setXRot(10);
        tick();check(runtime().getListOrEmpty("transfers").size()==2,"two real same-tick TP transfers");check(routes().size()==4,"pre-TP entry creates all four paths");
        var oldPoint=new HashMap<Integer,Tag>();var oldUUID=new HashMap<Integer,UUID>();
        for(var r:routes()){check(r.getIntOr("sourceId",0)==2,"rebase source to B independent of owner");if(r.getIntOr("targetId",0)==3){int id=r.getIntOr("id",0);oldPoint.put(id,r.get("point").copy());oldUUID.put(id,body(id,false).getUUID());}}
        tick();check(routes().size()==4,"TP arrival does not duplicate routes");
        for(var r:routes())if(r.getIntOr("targetId",0)==3){int id=r.getIntOr("id",0);check(body(id,false).getUUID().equals(oldUUID.get(id)),"C body UUID survives TP");var a=(ListTag)oldPoint.get(id);var b=r.getListOrEmpty("point");for(int i=0;i<3;i++)near(a.getDoubleOr(i,0),b.getDoubleOr(i,0),"C logical point continuous");check(body(id,false).getCustomName()==null,"B/C relative flip XOR becomes normal");}
        check(labels(false).stream().map(SpaceEditorStage6GameTest::text).collect(java.util.stream.Collectors.toSet()).containsAll(Set.of("ProjectorOne","ProjectorTwo")),"names stay separated after simultaneous TP");
        helper.getLevel().getServer().getPlayerList().remove(second);second=null;tick();check(routes().size()==2&&labels(false).stream().allMatch(l->text(l).equals("ProjectorOne")),"logout only clears departed owner's paths");
        var previous=routes().stream().map(r->r.getIntOr("id",0)).collect(java.util.stream.Collectors.toSet());cmd("function space_editor:load");tick();check(routes().stream().map(r->r.getIntOr("id",0)).collect(java.util.stream.Collectors.toSet()).equals(previous),"load preserves active path IDs and restores render");
        pcmd("scoreboard players add @s pr.leave 1");tick();check(routes().stream().noneMatch(r->previous.contains(r.getIntOr("id",0))),"rejoin invalidates old player session");
        System.out.println("SPACE_EDITOR_STAGE6_PHASE4_PASS: pre-TP activation, two simultaneous transfers, fractional mapping continuity, stable C UUID, logout/load/rejoin");
    }
    static int measured(){
        var actor=player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS);
        var holder=new java.util.concurrent.atomic.AtomicReference<net.minecraft.commands.execution.ExecutionContext<CommandSourceStack>>();
        net.minecraft.commands.Commands.executeCommandInContext(actor,c->{holder.set(c);helper.getLevel().getServer().getCommands().performPrefixedCommand(actor,"function space_editor:tick");});
        try{var type=net.minecraft.commands.execution.ExecutionContext.class;var limit=type.getDeclaredField("commandLimit");limit.setAccessible(true);var quota=type.getDeclaredField("commandQuota");quota.setAccessible(true);check(limit.getInt(holder.get())==65536,"command limit stays 65536");int used=65536-quota.getInt(holder.get());check(used<65536,"full tick completes within budget");return used;}catch(ReflectiveOperationException e){throw new AssertionError(e);}
    }
    static void stress(int n,boolean two){stress(n,two,false);}
    static void stress(int n,boolean two,boolean debug){
        fixture(2);cmd("function space_editor:projection/clear");cmd("data modify storage space_editor:document regions set value []");
        var members=new StringJoiner(",");
        for(int i=0;i<n;i++){int x=(i%8)*12,z=(i/8)*12;frame(i+1,x,z,"space_link",i==1?90:0,i==1?1:0,"stress_"+i);cmd("data modify storage space_editor:document regions[{id:"+(i+1)+"}].spaceLinkGroupId set value 1");existence(1000+i,x*1000-4000,x*1000+8000,z*1000-4000,z*1000+8000,"stress_"+i);members.add(""+(i+1));}
        cmd("data modify storage space_editor:document spaceLinkGroups set value [{id:1,localSize:[I;4000,4000,4000],members:["+members+"]}]");
        if(two){second=namedPlayer("LoadTwo");second.setPos(1.25,81,1.25);cmd("scoreboard players set @a se.tp_lock 0");cmd("scoreboard players set @a se.tp_cd 0");teleportPair();}
        if(debug){for(int i=2;i<=n;i++)cmd("execute as @a run function space_editor:projection/debug/map {target:"+i+",region:"+i+"}");cmd("scoreboard players set @a pr.debug 1");}
        at(1,81,1,0,0);int peak=measured();
        check(routes().size()==(n-1)*(two?2:1),"all logical routes accepted before render budget");
        if(two)check(runtime().getListOrEmpty("transfers").size()==2,"stress simultaneous TP");
        for(int i=0;i<(debug?40:18);i++)peak=Math.max(peak,measured());
        long[] times=new long[10];for(int i=0;i<times.length;i++){long t=System.nanoTime();peak=Math.max(peak,measured());times[i]=System.nanoTime()-t;}
        Arrays.sort(times);System.out.printf("SPACE_EDITOR_STAGE6_PERF link_regions=%d existence_regions=%d players=%d logical_paths=%d rendered=%d debug_rendered=%d full_tick_max_commands=%d median_ms=%.3f p90_ms=%.3f samples=10%n",n,n,two?2:1,routes().size(),bodies(false).size(),bodies(true).size(),peak,times[5]/1e6,times[9]/1e6);
        if(two){helper.getLevel().getServer().getPlayerList().remove(second);second=null;tick();}
        cmd("function space_editor:projection/clear");
    }
    static void demoTest(){
        fixture(2);var original=helper.getLevel().getServer().getCommandStorage().get(DOCUMENT).getListOrEmpty("regions").copy();
        cmd("data modify storage space_editor:document nextId set value 2000");cmd("data modify storage space_editor:document nextSpaceLinkGroupId set value 10");cmd("data modify storage space_editor:document nextPairId set value 10");
        at(32,80,32,0,0);pcmd("function space_editor:projection/demo/setup");
        var doc=helper.getLevel().getServer().getCommandStorage().get(DOCUMENT);var demo=doc.getCompoundOrEmpty("projection").getCompoundOrEmpty("demo");
        check(demo.getListOrEmpty("ids").size()==8,"demo creates three links, three existence Regions and two debug anchors");
        pcmd("function space_editor:projection/demo/setup");check(helper.getLevel().getServer().getCommandStorage().get(DOCUMENT).getListOrEmpty("regions").size()==original.size()+8,"demo repeated setup is idempotent");
        pcmd("function space_editor:play");at(33,81,37,0,0);tick();check(routes().size()==2,"demo links work");
        pcmd("function space_editor:projection/debug/on");tick();check(bodies(true).size()==2,"demo debug mappings work");
        pcmd("function space_editor:projection/demo/teleport");at(31,81,37,0,0);tick();at(33,81,37,0,0);tick();check(runtime().getListOrEmpty("transfers").size()==1,"demo adds working TP pair");
        pcmd("function space_editor:projection/demo/cleanup");var remaining=helper.getLevel().getServer().getCommandStorage().get(DOCUMENT).getListOrEmpty("regions");check(remaining.equals(original),"demo cleanup preserves every unrelated Region byte-for-byte");check(bodies(false).isEmpty()&&bodies(true).isEmpty(),"demo cleanup detaches renders");finishDeletes();check(removing().isEmpty(),"demo cleanup deletion queue drains");
        System.out.println("SPACE_EDITOR_STAGE6_DEMO_PASS: additive setup, working links/debug/TP, idempotence, narrow cleanup");
    }
    static void test(GameTestHelper h){
        helper=h;source=h.getLevel().getServer().createCommandSourceStack();cmd("function space_editor:load");cmd("forceload add -16 -16 112 112");player=namedPlayer("ProjectorOne");
        final int[] phase={0},wait={0};final boolean[] done={false};
        h.onEachTick(()->{if(done[0])return;try{
            if(!loaded(0,0)||!loaded(15,1)||!loaded(27,1)||!loaded(51,1)||!loaded(100,100)){check(++wait[0]<200,"test chunks loaded");return;}
            switch(phase[0]){
                case 0->{phase1();phase[0]++;}case 1->{phase2();phase[0]++;}case 2->{phase3();phase[0]++;}case 3->{phase4();phase[0]++;}
                case 4->{reloadIds=routes().stream().map(r->r.getIntOr("id",0)).collect(java.util.stream.Collectors.toSet());reload=helper.getLevel().getServer().reloadResources(helper.getLevel().getServer().getPackRepository().getSelectedIds());phase[0]++;}
                case 5->{if(reload.isDone()){reload.join();phase[0]++;}}
                case 6->{tick();check(routes().stream().map(r->r.getIntOr("id",0)).collect(java.util.stream.Collectors.toSet()).equals(reloadIds),"actual reload preserves path IDs");System.out.println("SPACE_EDITOR_STAGE6_RELOAD_PASS");phase[0]++;}
                case 7->{stress(4,false);phase[0]++;}case 8->{stress(16,false);phase[0]++;}case 9->{stress(64,false);phase[0]++;}case 10->{stress(64,true);phase[0]++;}
                case 11->{stress(64,true,true);phase[0]++;}case 12->{demoTest();phase[0]++;}
                default->{cmd("function space_editor:projection/disable");finishDeletes();check(removing().isEmpty(),"disable/reload deletion queues fully drain");System.out.println("SPACE_EDITOR_STAGE6_RUNTIME_PASS: four phases, reload, bounded full-tick load, additive demo");done[0]=true;h.succeed();}
            }
        }catch(Throwable ex){done[0]=true;ex.printStackTrace();h.fail(ex.getMessage());}});
    }
    public static void main(String[] args)throws Exception{
        SharedConstants.tryDetectVersion();TestFunctionLoader.registerLoader(new TestFunctionLoader(){public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register){register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorStage6GameTest::test);}});
        Path universe=Path.of(args[0]).toAbsolutePath().normalize(),allowed=Path.of("build/test-server").toAbsolutePath().normalize();if(!universe.startsWith(allowed)||Files.exists(universe))throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/stage6-runtime-report.xml").toAbsolutePath().toString()},ignored->{});
    }
}
