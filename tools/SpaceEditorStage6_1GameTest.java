import java.nio.file.*;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;

public class SpaceEditorStage6_1GameTest {
    static GameTestHelper helper;
    static CommandSourceStack source;
    static net.minecraft.server.level.ServerPlayer player;
    static java.util.concurrent.CompletableFuture<Void> reload;
    static void cmd(String value) { helper.getLevel().getServer().getCommands().performPrefixedCommand(source,value); }
    static void pcmd(String value) { helper.getLevel().getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS),value); }
    static boolean matches(String value) {
        cmd("execute store success storage space_editor:proxy_spike test byte 1 run "+value);
        return helper.getLevel().getServer().getCommandStorage().get(Identifier.parse("space_editor:proxy_spike")).getBooleanOr("test",false);
    }
    static boolean playerMatches(String value) {
        pcmd("execute store success storage space_editor:proxy_spike test byte 1 run "+value);
        return helper.getLevel().getServer().getCommandStorage().get(Identifier.parse("space_editor:proxy_spike")).getBooleanOr("test",false);
    }
    static void check(boolean ok,String message) { if(!ok) throw new AssertionError(message); }
    static net.minecraft.server.level.ServerPlayer namedPlayer(String name) {
        var server=helper.getLevel().getServer();
        var cookie=net.minecraft.server.network.CommonListenerCookie.createInitial(new com.mojang.authlib.GameProfile(java.util.UUID.randomUUID(),name),false);
        var p=new net.minecraft.server.level.ServerPlayer(server,helper.getLevel(),cookie.gameProfile(),cookie.clientInformation());
        var connection=new net.minecraft.network.Connection(net.minecraft.network.protocol.PacketFlow.SERVERBOUND);
        new io.netty.channel.embedded.EmbeddedChannel(connection);
        server.getPlayerList().placeNewPlayer(connection,p,cookie);
        p.setNoGravity(true);p.setPos(0,82,0);
        return p;
    }
    static net.minecraft.world.entity.decoration.Mannequin body(String role) {
        pcmd("function space_editor:proxy_spike/select");
        return helper.getLevel().getEntities(net.minecraft.world.entity.EntityType.MANNEQUIN,
            e->e.isAlive() && e.entityTags().contains("sp.selected") && e.entityTags().contains("sp."+role)).getFirst();
    }
    static net.minecraft.world.entity.Display.TextDisplay label(String role) {
        pcmd("function space_editor:proxy_spike/select");
        return helper.getLevel().getEntities(net.minecraft.world.entity.EntityType.TEXT_DISPLAY,
            e->e.entityTags().contains("sp.selected") && e.entityTags().contains("sp.label_"+role)).getFirst();
    }
    static void near(double actual,double expected,String message) { check(Math.abs(actual-expected)<0.002,message+" actual="+actual+" expected="+expected); }
    static String textOf(Object entity,String name) {
        try { var method=entity.getClass().getDeclaredMethod(name);method.setAccessible(true);return ((net.minecraft.network.chat.Component)method.invoke(entity)).getString(); }
        catch(ReflectiveOperationException ex) { throw new AssertionError(ex); }
    }
    static int measuredTick() {
        var actor=player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS);
        var holder=new java.util.concurrent.atomic.AtomicReference<net.minecraft.commands.execution.ExecutionContext<CommandSourceStack>>();
        net.minecraft.commands.Commands.executeCommandInContext(actor,context->{
            holder.set(context);cmd("function space_editor:proxy_spike/tick");
        });
        try {
            var type=net.minecraft.commands.execution.ExecutionContext.class;
            var limit=type.getDeclaredField("commandLimit");limit.setAccessible(true);
            var quota=type.getDeclaredField("commandQuota");quota.setAccessible(true);
            check(limit.getInt(holder.get())==65536,"command ceiling unchanged");
            return 65536-quota.getInt(holder.get());
        } catch(ReflectiveOperationException ex) { throw new AssertionError(ex); }
    }
    static void performance(String mode) {
        for(int i=0;i<20;i++) measuredTick();
        long[] nanos=new long[100];int commands=0;
        for(int i=0;i<nanos.length;i++) { long start=System.nanoTime();commands=Math.max(commands,measuredTick());nanos[i]=System.nanoTime()-start; }
        java.util.Arrays.sort(nanos);
        check(commands<1000,"bounded spike tick cost");
        System.out.printf("SPACE_EDITOR_STAGE6_1_PERF %s commands=%d median_us=%.1f p95_us=%.1f samples=100%n",mode,commands,nanos[50]/1000.0,nanos[95]/1000.0);
    }
    static void test(GameTestHelper h) {
        helper=h; source=h.getLevel().getServer().createCommandSourceStack();
        cmd("function space_editor:load");
        cmd("forceload add -16 -16 16 16");
        player=namedPlayer("ProxyOne");
        final boolean[] done={false}; final int[] ticks={0};final int[] phase={0};
        final java.util.UUID[] paused={null};
        h.onEachTick(()->{
            if(done[0]) return;
            try {
                if(!matches("execute if loaded 0 82 0")) { if(++ticks[0]>100) throw new AssertionError("test chunk not loaded"); return; }
                if(phase[0]==1) {
                    if(++ticks[0]<6) return;
                    var frozen=helper.getLevel().getEntity(paused[0]);
                    check(frozen!=null,"pause keeps existing UUID through real server ticks");near(frozen.getY(),84,"no gravity over six server ticks");
                    pcmd("function space_editor:proxy_spike/stop");
                    check(matches("execute unless entity @e[tag=space_editor.proxy_spike]"),"stop cleans all owned entities");
                    check(matches("execute unless entity @e[type=minecraft:item]"),"no duplicated equipment drops on cleanup");
                    phase[0]=2;ticks[0]=0;return;
                }
                if(phase[0]==2) {
                    if(++ticks[0]<22) return;
                    check(matches("execute unless entity @e[type=minecraft:item]"),"no delayed equipment drops");
                    pcmd("function space_editor:proxy_spike/pair");
                    reload=helper.getLevel().getServer().reloadResources(helper.getLevel().getServer().getPackRepository().getSelectedIds());
                    phase[0]=3;ticks[0]=0;return;
                }
                if(phase[0]==3) {
                    if(!reload.isDone()) { check(++ticks[0]<400,"resource reload finishes");return; }
                    reload.join();
                    // load-tag functions execute on the following game tick.
                    phase[0]=4;return;
                }
                if(phase[0]==4) {
                    check(matches("execute unless entity @e[tag=space_editor.proxy_spike]"),"actual resource reload removes test entities");
                    check(playerMatches("execute if score @s sp.follow matches 0"),"actual resource reload stops follow");
                    pcmd("function space_editor:proxy_spike/pair");
                    check(textOf(label("main"),"getText").equals("ProxyOne"),"restart after actual resource reload");
                    pcmd("function space_editor:proxy_spike/stop");
                    System.out.println("SPACE_EDITOR_STAGE6_1_RUNTIME_PASS: exact owner names/UUID profile, two-player isolation, fixed offset and rotation, label reuse/pose heights, equipment, native modes, swing state, logout, stale epochs/generations, reload, command budget, physical pause, no item drops");
                    done[0]=true;h.succeed();return;
                }
                var document=helper.getLevel().getServer().getCommandStorage().get(Identifier.parse("space_editor:document")).copy();
                pcmd("tp @s 0.0 82 0.0 0 0");
                pcmd("function space_editor:proxy_spike/spawn");
                check(matches("execute if entity @e[tag=sp.main,tag=space_editor.proxy_spike]"),"spawn main");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] profile.id"),"dynamic profile UUID");
                pcmd("data modify storage space_editor:proxy_spike expectedUUID set from entity @s UUID");
                pcmd("data modify storage space_editor:proxy_spike actualUUID set from entity @e[tag=sp.selected,tag=sp.main,limit=1] profile.id");
                var scratch=helper.getLevel().getServer().getCommandStorage().get(Identifier.parse("space_editor:proxy_spike"));
                check(scratch.get("actualUUID").equals(scratch.get("expectedUUID")),"profile UUID equals exact source player");
                performance("one_player_one_body");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {immovable:1b,NoGravity:1b,Invulnerable:1b}"),"display-only flags");
                pcmd("function space_editor:proxy_spike/pair");
                check(matches("execute if entity @e[tag=sp.reference,tag=space_editor.proxy_spike]"),"comparison mannequin");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {CustomName:\"Dinnerbone\"}"),"Dinnerbone component");
                check(matches("execute if entity @e[tag=sp.main,team=sp_hidden]"),"pair hides Dinnerbone nametag");
                check(body("main").isModelPartShown(net.minecraft.world.entity.player.PlayerModelPart.CAPE),"cape layer enabled for inversion predicate");
                check(matches("execute if data entity @e[tag=sp.label_main,limit=1] text.text"),"inverted mannequin shows source player name");
                check(matches("execute if data entity @e[tag=sp.label_reference,limit=1] text.text"),"normal mannequin shows source player name");
                near(label("main").getY(),84.1,"inverted name stays above model volume");
                near(label("reference").getX(),2,"reference separation");
                near(label("reference").getY(),84.1,"normal name height");
                check(textOf(label("main"),"getText").equals("ProxyOne"),"exact resolved username main");
                check(textOf(label("reference"),"getText").equals("ProxyOne"),"exact resolved username reference");
                var mainId=body("main").getUUID();var labelId=label("main").getUUID();
                pcmd("function space_editor:proxy_spike/name_team_hidden");
                check(matches("execute if entity @e[tag=sp.main,team=sp_hidden]"),"team nametag mode");
                pcmd("function space_editor:proxy_spike/name_description");
                check(matches("execute unless data entity @e[tag=sp.main,limit=1] {hide_description:1b}"),"description comparison mode");
                check(textOf(body("main"),"getDescription").equals("ProxyOne"),"description contains resolved name, not unresolved selector");
                pcmd("function space_editor:proxy_spike/name_native_visible");
                check(body("main").isCustomNameVisible(),"native visible comparison");
                pcmd("function space_editor:proxy_spike/name_custom_hidden");
                check(!body("main").isCustomNameVisible(),"custom hidden comparison");
                pcmd("function space_editor:proxy_spike/name_text_display");
                check(matches("execute if entity @e[tag=sp.label,tag=space_editor.proxy_spike]"),"text display mode");
                check(matches("execute if data entity @e[tag=sp.label,limit=1] text.text"),"label owner name resolved");
                check(body("main").getUUID().equals(mainId)&&label("main").getUUID().equals(labelId),"mode changes reuse body and label UUIDs");
                pcmd("function space_editor:proxy_spike/flip_grumm");check(body("main").getCustomName().getString().equals("Grumm"),"Grumm trigger");
                pcmd("function space_editor:proxy_spike/flip_off");check(body("main").getCustomName()==null,"flip off clears trigger");
                pcmd("function space_editor:proxy_spike/flip_on");
                pcmd("function space_editor:proxy_spike/swing_main");
                check(body("main").swinging,"swing actually starts server animation");
                body("main").swinging=false;body("reference").swinging=false;
                pcmd("function space_editor:proxy_spike/swing_off");
                check(body("main").swingingArm==net.minecraft.world.InteractionHand.OFF_HAND,"offhand swing");
                body("main").swinging=false;body("reference").swinging=false;
                var victim=net.minecraft.world.entity.EntityType.PIG.create(helper.getLevel(),net.minecraft.world.entity.EntitySpawnReason.COMMAND);
                victim.getAttribute(net.minecraft.world.entity.ai.attributes.Attributes.MAX_HEALTH).setBaseValue(1000);
                victim.setHealth(1000);victim.setPos(player.position());helper.getLevel().addFreshEntity(victim);
                player.attack(victim);
                check(victim.getHealth()<1000,"actual melee hit damages test victim");
                check(body("main").swinging && body("main").swingingArm==net.minecraft.world.InteractionHand.MAIN_HAND,"melee advancement forwards swing");
                victim.discard();
                pcmd("function space_editor:proxy_spike/label_style {scale:1.25,background:536870912}");
                check(matches("execute if data entity @e[tag=sp.label_main,limit=1] {background:536870912,transformation:{scale:[1.25f,1.25f,1.25f]}}"),"label style macro");
                pcmd("item replace entity @s weapon.mainhand with minecraft:diamond_sword");
                pcmd("item replace entity @s weapon.offhand with minecraft:shield");
                pcmd("item replace entity @s armor.head with minecraft:iron_helmet");
                for(String part:java.util.List.of("chest","legs","feet")) pcmd("item replace entity @s armor."+part+" with minecraft:"+switch(part){case "chest"->"iron_chestplate";case "legs"->"iron_leggings";default->"iron_boots";});
                pcmd("tp @s 8.0 84 8.0 90 30");
                pcmd("function space_editor:proxy_spike/player_tick");
                near(body("main").getX(),8,"fixed world X");near(body("main").getY(),84,"jump height");near(body("main").getZ(),11,"fixed world Z");
                near(body("main").getYRot(),90,"yaw copied");near(body("main").getXRot(),30,"pitch copied");near(body("main").getYHeadRot(),90,"head yaw copied");
                pcmd("tp @s 8.0 84 8.0 -170 -40");pcmd("function space_editor:proxy_spike/player_tick");
                near(body("main").getX(),8,"stationary look does not orbit");near(body("main").getZ(),11,"stationary look does not orbit Z");
                near(net.minecraft.util.Mth.wrapDegrees(body("main").getYHeadRot()),-170,"head turn across yaw wrap");near(body("main").getXRot(),-40,"pitch turn");
                check(matches("execute if items entity @e[tag=sp.main,limit=1] weapon.mainhand minecraft:diamond_sword"),"mainhand equipment");
                check(matches("execute if items entity @e[tag=sp.main,limit=1] weapon.offhand minecraft:shield"),"offhand equipment");
                check(matches("execute if items entity @e[tag=sp.main,limit=1] armor.head minecraft:iron_helmet"),"armor equipment");
                check(body("main").getItemBySlot(net.minecraft.world.entity.EquipmentSlot.CHEST).is(net.minecraft.world.item.Items.IRON_CHESTPLATE),"chest armor");
                check(body("main").getItemBySlot(net.minecraft.world.entity.EquipmentSlot.LEGS).is(net.minecraft.world.item.Items.IRON_LEGGINGS),"leg armor");
                check(body("main").getItemBySlot(net.minecraft.world.entity.EquipmentSlot.FEET).is(net.minecraft.world.item.Items.IRON_BOOTS),"feet armor");
                pcmd("item replace entity @s weapon.offhand with minecraft:air");pcmd("function space_editor:proxy_spike/player_tick");
                check(body("main").getOffhandItem().isEmpty(),"empty slot clears prior equipment");
                check(matches("execute if data entity @e[tag=sp.label,limit=1] text"),"name display text assigned");
                player.setShiftKeyDown(true);
                player.setPose(net.minecraft.world.entity.Pose.CROUCHING);
                pcmd("function space_editor:proxy_spike/player_tick");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {pose:\"crouching\"}"),"crouching pose");
                near(label("main").getY(),85.8,"crouching label follows pose");
                player.setShiftKeyDown(false);
                player.setSwimming(true);
                player.setPose(net.minecraft.world.entity.Pose.SWIMMING);
                pcmd("function space_editor:proxy_spike/player_tick");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {pose:\"swimming\"}"),"swimming pose");
                near(label("main").getY(),84.9,"swimming label height");
                player.setSwimming(false);
                player.startFallFlying();
                player.setPose(net.minecraft.world.entity.Pose.FALL_FLYING);
                pcmd("function space_editor:proxy_spike/player_tick");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {pose:\"fall_flying\"}"),"fall flying pose");
                player.stopFallFlying();player.setSleepingPos(new net.minecraft.core.BlockPos(8,84,8));player.setPose(net.minecraft.world.entity.Pose.SLEEPING);
                pcmd("function space_editor:proxy_spike/player_tick");check(body("main").getPose()==net.minecraft.world.entity.Pose.SLEEPING,"sleeping_pos maps to sleeping pose");
                player.clearSleepingPos();player.setPose(net.minecraft.world.entity.Pose.STANDING);
                pcmd("function space_editor:proxy_spike/offset {x:-3,y:0.25,z:0}");
                pcmd("function space_editor:proxy_spike/flip_height {fy:0.5}");
                pcmd("function space_editor:proxy_spike/label_height {normal:2.2,inverted:2.4}");
                pcmd("function space_editor:proxy_spike/player_tick");
                near(body("main").getX(),5,"configurable offset");near(body("main").getY(),84.75,"visual Y correction independent of coordinate flip");
                near(body("reference").getY(),84.25,"inverted correction affects main only");near(label("main").getY(),87.15,"configured inverted label height");
                performance("one_player_two_bodies");
                pcmd("function space_editor:proxy_spike/follow_off");
                check(playerMatches("execute if score @s sp.follow matches 0"),"follow off");
                pcmd("function space_editor:proxy_spike/tick");
                check(matches("execute if entity @e[tag=sp.main]"),"follow off keeps mannequin");
                pcmd("function space_editor:proxy_spike/follow_on");
                check(playerMatches("execute if score @s sp.follow matches 1"),"follow on");
                var first=player;var other=namedPlayer("ProxyTwo");player=other;
                pcmd("function space_editor:proxy_spike/pair");var otherBody=body("main").getUUID();
                check(textOf(label("main"),"getText").equals("ProxyTwo"),"second username resolves independently");
                player=first;check(body("main").getUUID().equals(mainId),"second player does not replace first");
                pcmd("function space_editor:proxy_spike/stop");player=other;check(body("main").getUUID().equals(otherBody),"first stop preserves second body");
                helper.getLevel().getServer().getPlayerList().remove(other);player=first;cmd("function space_editor:proxy_spike/tick");
                check(matches("execute unless entity @e[tag=space_editor.proxy_spike]"),"offline owner cleanup");
                pcmd("function space_editor:proxy_spike/pair");
                // Reproduce a stale entity returning from an unloaded chunk after /reload.
                var stale=body("main");cmd("scoreboard players remove @e[tag=sp.selected,tag=sp.main,limit=1] sp.epoch 1");
                cmd("function space_editor:proxy_spike/tick");check(!stale.isAlive(),"stale reload epoch is collected even if owner online");
                check(matches("execute unless entity @e[tag=sp.label_main]"),"stale body's name removed with it");
                pcmd("function space_editor:proxy_spike/spawn");
                cmd("kill @e[tag=sp.selected,tag=sp.label_main]");cmd("function space_editor:proxy_spike/tick");
                check(textOf(label("main"),"getText").equals("ProxyOne"),"missing label repaired and survives cleanup in same tick");
                // Simulate an old session entity becoming loaded after a new spawn.
                cmd("summon minecraft:mannequin 1.0 84 1.0 {Tags:[\"space_editor.proxy_spike\",\"sp.main\",\"sp.stale_test\"],NoGravity:1b,immovable:1b}");
                cmd("scoreboard players operation @e[tag=sp.stale_test] sp.epoch = #epoch sp.epoch");
                cmd("scoreboard players set @e[tag=sp.stale_test] sp.owner 999999");
                cmd("function space_editor:proxy_spike/tick");
                check(matches("execute unless entity @e[tag=sp.stale_test]"),"old generation collected without touching current body");
                check(body("main").isAlive(),"current generation survives stale cleanup");
                pcmd("scoreboard players add @s sp.leave 1");cmd("function space_editor:proxy_spike/tick");
                check(matches("execute unless entity @e[tag=space_editor.proxy_spike]"),"logout/rejoin statistic invalidates unloaded old session");
                pcmd("function space_editor:proxy_spike/delete");
                check(matches("execute unless entity @e[tag=space_editor.proxy_spike]"),"delete all owned spike entities");
                pcmd("function space_editor:proxy_spike/spawn");
                pcmd("function space_editor:proxy_spike/name_text_display");
                cmd("kill @e[tag=sp.main]");
                pcmd("function space_editor:proxy_spike/mark_online");
                check(matches("execute unless entity @e[tag=sp.label]"),"orphan name cleanup");
                pcmd("function space_editor:proxy_spike/spawn");
                cmd("function space_editor:proxy_spike/load");
                check(matches("execute unless entity @e[tag=space_editor.proxy_spike]"),"reload cleanup");
                check(document.equals(helper.getLevel().getServer().getCommandStorage().get(Identifier.parse("space_editor:document"))),"persistent Stage01-05 document untouched");
                pcmd("tp @s 0.0 84 0.0 0 0");pcmd("function space_editor:proxy_spike/pair");
                pcmd("function space_editor:proxy_spike/follow_off");paused[0]=body("main").getUUID();
                check(!matches("damage @e[tag=sp.selected,tag=sp.main,limit=1] 5 minecraft:generic"),"ordinary damage rejected");
                pcmd("tp @s 5 90 5 0 0");phase[0]=1;ticks[0]=0;
            } catch(Throwable ex) { done[0]=true;ex.printStackTrace();h.fail(ex.getMessage()); }
        });
    }
    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion();
        TestFunctionLoader.registerLoader(new TestFunctionLoader(){
            public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register){
                register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorStage6_1GameTest::test);
            }
        });
        Path universe=Path.of(args[0]).toAbsolutePath().normalize();
        Path allowed=Path.of("build/test-server").toAbsolutePath().normalize();
        if(!universe.startsWith(allowed)||Files.exists(universe)) throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/stage6_1-runtime-report.xml").toAbsolutePath().toString()},ignored->{});
    }
}
