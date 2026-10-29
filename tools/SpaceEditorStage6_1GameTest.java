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
    static void test(GameTestHelper h) {
        helper=h; source=h.getLevel().getServer().createCommandSourceStack();
        cmd("function space_editor:load");
        cmd("forceload add -16 -16 16 16");
        player=h.makeMockServerPlayerInLevel(); player.setNoGravity(true); player.setPos(.5,82,.5);
        final boolean[] done={false}; final int[] ticks={0};
        h.onEachTick(()->{
            if(done[0]) return;
            try {
                if(!matches("execute if loaded 0 82 0")) { if(++ticks[0]>100) throw new AssertionError("test chunk not loaded"); return; }
                pcmd("tp @s 0 82 0 0 0");
                pcmd("function space_editor:proxy_spike/spawn");
                check(matches("execute if entity @e[tag=sp.main,tag=space_editor.proxy_spike]"),"spawn main");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] profile.id"),"dynamic profile UUID");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {immovable:1b,NoGravity:1b,Invulnerable:1b}"),"display-only flags");
                pcmd("function space_editor:proxy_spike/pair");
                check(matches("execute if entity @e[tag=sp.reference,tag=space_editor.proxy_spike]"),"comparison mannequin");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {CustomName:\"Dinnerbone\"}"),"Dinnerbone component");
                check(matches("execute if entity @e[tag=sp.main,team=sp_hidden]"),"pair hides Dinnerbone nametag");
                check(matches("execute if data entity @e[tag=sp.label_main,limit=1] text.text"),"inverted mannequin shows source player name");
                check(matches("execute if data entity @e[tag=sp.label_reference,limit=1] text.text"),"normal mannequin shows source player name");
                check(matches("execute if entity @e[tag=sp.label_main,x=0,y=82.7,z=3,distance=..1]"),"inverted name near low head");
                check(matches("execute if entity @e[tag=sp.label_reference,x=-1,y=84.3,z=3,distance=..1]"),"normal name above head");
                pcmd("function space_editor:proxy_spike/name_team_hidden");
                check(matches("execute if entity @e[tag=sp.main,team=sp_hidden]"),"team nametag mode");
                pcmd("function space_editor:proxy_spike/name_description");
                check(matches("execute unless data entity @e[tag=sp.main,limit=1] {hide_description:1b}"),"description comparison mode");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] description.selector"),"description owner selector");
                pcmd("function space_editor:proxy_spike/name_text_display");
                check(matches("execute if entity @e[tag=sp.label,tag=space_editor.proxy_spike]"),"text display mode");
                check(matches("execute if data entity @e[tag=sp.label,limit=1] text.text"),"label owner name resolved");
                pcmd("function space_editor:proxy_spike/swing_main");
                pcmd("item replace entity @s weapon.mainhand with minecraft:diamond_sword");
                pcmd("item replace entity @s weapon.offhand with minecraft:shield");
                pcmd("item replace entity @s armor.head with minecraft:iron_helmet");
                pcmd("tp @s 8 84 8 90 30");
                pcmd("function space_editor:proxy_spike/player_tick");
                check(matches("execute if entity @e[tag=sp.main,x=5,y=84,z=8,distance=..1]"),"position follows player local forward");
                check(matches("execute if items entity @e[tag=sp.main,limit=1] weapon.mainhand minecraft:diamond_sword"),"mainhand equipment");
                check(matches("execute if items entity @e[tag=sp.main,limit=1] weapon.offhand minecraft:shield"),"offhand equipment");
                check(matches("execute if items entity @e[tag=sp.main,limit=1] armor.head minecraft:iron_helmet"),"armor equipment");
                check(matches("execute if data entity @e[tag=sp.label,limit=1] text"),"name display text assigned");
                player.setShiftKeyDown(true);
                player.setPose(net.minecraft.world.entity.Pose.CROUCHING);
                pcmd("function space_editor:proxy_spike/player_tick");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {pose:\"crouching\"}"),"crouching pose");
                player.setShiftKeyDown(false);
                player.setSwimming(true);
                player.setPose(net.minecraft.world.entity.Pose.SWIMMING);
                pcmd("function space_editor:proxy_spike/player_tick");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {pose:\"swimming\"}"),"swimming pose");
                player.setSwimming(false);
                player.startFallFlying();
                player.setPose(net.minecraft.world.entity.Pose.FALL_FLYING);
                pcmd("function space_editor:proxy_spike/player_tick");
                check(matches("execute if data entity @e[tag=sp.main,limit=1] {pose:\"fall_flying\"}"),"fall flying pose");
                player.setPose(net.minecraft.world.entity.Pose.STANDING);
                pcmd("function space_editor:proxy_spike/follow_off");
                check(playerMatches("execute if score @s sp.follow matches 0"),"follow off");
                pcmd("function space_editor:proxy_spike/tick");
                check(matches("execute if entity @e[tag=sp.main]"),"follow off keeps mannequin");
                pcmd("function space_editor:proxy_spike/follow_on");
                check(playerMatches("execute if score @s sp.follow matches 1"),"follow on");
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
                System.out.println("SPACE_EDITOR_STAGE6_1_RUNTIME_PASS: spawn, profile UUID, flags, comparison, Dinnerbone data, name modes, follow, equipment, pose, swing command, stop, delete, reload cleanup");
                done[0]=true;h.succeed();
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
