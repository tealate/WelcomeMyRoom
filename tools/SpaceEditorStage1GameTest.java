// Isolated runtime checks for the stage-1 Space Editor implementation.
import java.nio.file.*;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.nbt.*;

public class SpaceEditorStage1GameTest {
    static GameTestHelper helper;
    static CommandSourceStack source;
    static net.minecraft.server.level.ServerPlayer player;
    static int step;
    static int loadedX, loadedY, loadedZ;
    static boolean finished;
    static final Identifier DOCUMENT = Identifier.parse("space_editor:document");
    static final Identifier RUNTIME = Identifier.parse("space_editor:runtime");

    static CompoundTag document() { return helper.getLevel().getServer().getCommandStorage().get(DOCUMENT); }
    static CompoundTag runtime() { return helper.getLevel().getServer().getCommandStorage().get(RUNTIME); }
    static ListTag regions() { return document().getListOrEmpty("regions"); }
    static void cmd(String command) { helper.getLevel().getServer().getCommands().performPrefixedCommand(source, command); }
    static void pcmd(String command) { helper.getLevel().getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS), command); }
    static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message + " DOCUMENT=" + document() + " RUNTIME=" + runtime()); }
    static long count(String tag) { long n=0; for (var e: helper.getLevel().getAllEntities()) if (e.entityTags().contains(tag)) n++; return n; }

    static void test(GameTestHelper h) {
        helper=h; source=h.getLevel().getServer().createCommandSourceStack(); step=0; finished=false;
        h.onEachTick(() -> {
            if (finished) return;
            try {
                if (step==0) {
                    cmd("function space_editor:load");
                    check(document().getIntOr("schemaVersion",0)==1,"schema initialized");
                    cmd("data modify storage space_editor:runtime selection set value {a:[I;-1,80,-1],b:[I;-2,80,-2],dimension:\"minecraft:overworld\"}");
                    cmd("function space_editor:region/create");
                    check(regions().size()==1,"first region created");
                    var r=regions().getCompoundOrEmpty(0);
                    check(r.getStringOr("idText","").equals("region_1"),"stable id");
                    check(r.getIntArray("min").orElseThrow()[0]==-2 && r.getIntArray("maxExclusive").orElseThrow()[0]==0,"reversed negative normalization");
                    check(r.getIntOr("sx",0)==2 && r.getIntOr("sy",0)==1,"inclusive endpoint size");
                    cmd("data modify storage space_editor:document regions[0].x1 set value -2.00001d");
                    cmd("data modify storage space_editor:document regions[0].x1m set value -2001");
                    cmd("function space_editor:internal/migrate_bounds");
                    r=regions().getCompoundOrEmpty(0);
                    check(r.getIntOr("x1m",99)==-2000 && Math.abs(r.getDoubleOr("x1",99)+2.0)<0.000001,"legacy floating error snaps to exact 0.1 boundary");
                    cmd("function space_editor:set_step {amount:0.1}");
                    check(document().getCompoundOrEmpty("settings").getIntOr("stepMilli",0)==100,"decimal step converts to exact integer units");
                    step++;
                } else if (step==1) {
                    cmd("data modify storage space_editor:runtime selection set value {a:[I;2,80,2],b:[I;2,80,2],dimension:\"minecraft:overworld\"}");
                    cmd("function space_editor:region/create");
                    check(regions().size()==2,"one-block region created");
                    check(regions().getCompoundOrEmpty(1).getIntOr("sx",0)==1,"one-block size");
                    BlockPos loaded=h.absolutePos(new BlockPos(0,5,0));
                    loadedX=loaded.getX(); loadedY=loaded.getY(); loadedZ=loaded.getZ();
                    cmd("data modify storage space_editor:runtime selection set value {a:[I;"+loadedX+","+loadedY+","+loadedZ+"],b:[I;"+loadedX+","+loadedY+","+loadedZ+"],dimension:\"minecraft:overworld\"}");
                    cmd("function space_editor:region/create");
                    check(regions().size()==3,"loaded-chunk region created");
                    player=h.makeMockServerPlayerInLevel(); player.setNoGravity(true); player.setPos(0.5,80,0.5);
                    pcmd("function space_editor:start");
                    check(player.entityTags().contains("space_editor.editing"),"editing mode");
                    step++;
                } else if (step==2) {
                    check(count("space_editor.region")==1,"loaded region preview rendered");
                    check(count("space_editor.label")==1,"position and size label rendered");
                    pcmd("function space_editor:play");
                    check(count("space_editor.preview")==0,"play hides previews");
                    check(regions().size()==3,"play preserves regions");
                    pcmd("function space_editor:start");
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
                    pcmd("function space_editor:region/resize_all");
                    var r=regions().getCompoundOrEmpty(0);
                    check(Math.abs(r.getDoubleOr("x1",99)+2.1)<0.0001 && Math.abs(r.getDoubleOr("x2",99)-0.1)<0.0001,"whole resize expands by 0.1");
                    check(r.getIntOr("x1m",99)==-2100 && r.getIntOr("x2m",99)==100,"whole resize keeps exact fixed-point bounds");
                    step++;
                } else if (step==3) {
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
                    cmd("data modify storage space_editor:runtime hitFace set value 1");
                    pcmd("function space_editor:region/resize_face");
                    check(Math.abs(regions().getCompoundOrEmpty(0).getDoubleOr("x2",99)-0.2)<0.0001,"face resize moves one face by 0.1");
                    for (int i=0;i<8;i++) {
                        cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
                        cmd("data modify storage space_editor:runtime hitFace set value 1");
                        pcmd("function space_editor:region/resize_face");
                    }
                    check(regions().getCompoundOrEmpty(0).getIntOr("x2m",99)==1000,"repeated 0.1 edits have no floating-point drift");
                    player.setShiftKeyDown(true); player.setPose(net.minecraft.world.entity.Pose.CROUCHING);
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[1]");
                    pcmd("function space_editor:region/resize_all");
                    check(Math.abs(regions().getCompoundOrEmpty(1).getDoubleOr("sx",0)-0.8)<0.0001,"whole shrink uses 0.1 per face");
                    player.setShiftKeyDown(false); player.setPose(net.minecraft.world.entity.Pose.STANDING);
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[1]");
                    pcmd("function space_editor:region/delete_selected");
                    check(regions().size()==2,"delete tool path removes selected region");
                    step++;
                } else if (step==4) {
                    cmd("function space_editor:load");
                    check(regions().size()==2,"reload preserves regions and deletion");
                    check(regions().getCompoundOrEmpty(0).getStringOr("idText","").equals("region_1"),"reload preserves id");
                    check(count("space_editor.region")==1,"reload resynchronizes loaded previews");
                    System.out.println("SPACE_EDITOR_STAGE1_RUNTIME_PASS: normalization, negative coordinates, one-block region, persistence, labels, preview hide/restore, 0.1 whole resize, 0.1 face resize, delete, reload resync");
                    finished=true; h.succeed();
                }
            } catch (Throwable ex) { finished=true; ex.printStackTrace(); h.fail(ex.getMessage()); }
        });
    }

    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion();
        TestFunctionLoader.registerLoader(new TestFunctionLoader() {
            public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register) {
                register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorStage1GameTest::test);
            }
        });
        Path universe=Path.of(args[0]).toAbsolutePath().normalize();
        Path allowed=Path.of("build/test-server").toAbsolutePath().normalize();
        if(!universe.startsWith(allowed)||Files.exists(universe)) throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/stage1-runtime-report.xml").toAbsolutePath().toString()}, ignored -> {});
    }
}
