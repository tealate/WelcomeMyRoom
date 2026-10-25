// Isolated runtime checks for Space Editor phase 2 on Minecraft Java 26.1.
import java.nio.file.*;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.nbt.*;
import net.minecraft.world.level.block.Blocks;

public class SpaceEditorStage2GameTest {
    static GameTestHelper helper;
    static CommandSourceStack source;
    static net.minecraft.server.level.ServerPlayer player;
    static int step, waitTicks;
    static int x, y, z;
    static boolean finished;
    static final Identifier DOCUMENT = Identifier.parse("space_editor:document");
    static final Identifier RUNTIME = Identifier.parse("space_editor:runtime");

    static CompoundTag document() { return helper.getLevel().getServer().getCommandStorage().get(DOCUMENT); }
    static CompoundTag runtime() { return helper.getLevel().getServer().getCommandStorage().get(RUNTIME); }
    static ListTag regions() { return document().getListOrEmpty("regions"); }
    static void cmd(String command) { helper.getLevel().getServer().getCommands().performPrefixedCommand(source, command); }
    static void pcmd(String command) { helper.getLevel().getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS), command); }
    static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message + " DOCUMENT=" + document() + " RUNTIME=" + runtime()); }
    static String jobState() { return document().getCompoundOrEmpty("job").getStringOr("state", ""); }

    static void tickJob() {
        if (jobState().equals("running")) cmd("function space_editor:job/tick");
    }

    static void test(GameTestHelper h) {
        helper=h; source=h.getLevel().getServer().createCommandSourceStack(); step=0; waitTicks=0; finished=false;
        h.onEachTick(() -> {
            if (finished) return;
            try {
                if (step==0) {
                    cmd("function space_editor:load");
                    cmd("data modify storage space_editor:document regions set value []");
                    cmd("data modify storage space_editor:document templates set value []");
                    cmd("data modify storage space_editor:document actions set value []");
                    cmd("data modify storage space_editor:document nextId set value 1");
                    cmd("data modify storage space_editor:document nextTemplateId set value 1");
                    cmd("gamerule minecraft:max_block_modifications 2");
                    x=0; y=80; z=0;
                    cmd("forceload add 0 0");
                    cmd("setblock "+x+" "+y+" "+z+" minecraft:stone");
                    cmd("setblock "+(x+1)+" "+y+" "+z+" minecraft:dirt");
                    cmd("setblock "+x+" "+y+" "+(z+1)+" minecraft:oak_planks");
                    cmd("setblock "+(x+1)+" "+y+" "+(z+1)+" minecraft:bricks");
                    cmd("data modify storage space_editor:runtime selection set value {a:[I;"+x+","+y+","+z+"],b:[I;"+(x+1)+","+y+","+(z+1)+"],dimension:\"minecraft:overworld\"}");
                    cmd("function space_editor:region/create");
                    check(regions().size()==1,"copy source region created");
                    player=h.makeMockServerPlayerInLevel(); player.setNoGravity(true); player.setPos(x+0.5,y+2,z+0.5);
                    cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[0]");
                    pcmd("function space_editor:copy/start");
                    check(jobState().equals("running"),"copy job persisted before clone");
                    step=1;
                } else if (step==1) {
                    tickJob(); waitTicks++;
                    if (!jobState().equals("running")) {
                        check(document().getCompoundOrEmpty("job").getIntOr("completedChunks",0)==2,"copy split into two X chunks at live block limit");
                        check(document().getListOrEmpty("templates").size()==1,"template registry appended after all chunks");
                        var template=document().getListOrEmpty("templates").getCompoundOrEmpty(0);
                        check(template.getIntOr("id",0)==1 && template.getIntArray("size").orElseThrow()[0]==2,"template id and size stored");
                        var archive=template.getCompoundOrEmpty("archive");
                        BlockPos ap=new BlockPos(archive.getIntOr("x",0),archive.getIntOr("y",0),archive.getIntOr("z",0));
                        check(h.getLevel().getBlockState(ap).is(Blocks.STONE),"archive copied first block");
                        check(h.getLevel().getBlockState(ap.offset(1,0,1)).is(Blocks.BRICKS),"archive copied last block");
                        cmd("setblock "+(x+8)+" "+y+" "+z+" minecraft:cobblestone");
                        player.setPos(x+8.5,y+3,z+0.5);
                        player.setXRot(90.0f);
                        pcmd("item replace entity @s weapon.offhand with minecraft:paper[minecraft:custom_data={space_editor:{kind:\"template\",templateId:1,version:1}}]");
                        pcmd("function space_editor:input/paste");
                        check(runtime().contains("pastePending"),"first paste click stores preview state");
                        check(!jobState().equals("running"),"first paste click does not modify blocks");
                        pcmd("function space_editor:input/paste");
                        check(jobState().equals("running"),"paste job persisted");
                        step=2; waitTicks=0;
                    } else if (waitTicks>20) throw new AssertionError("copy job timeout");
                } else if (step==2) {
                    tickJob(); waitTicks++;
                    if (!jobState().equals("running")) {
                        BlockPos target=new BlockPos(x+8,y,z);
                        check(h.getLevel().getBlockState(target).is(Blocks.STONE),"paste copied first block at feet anchor");
                        check(h.getLevel().getBlockState(target.offset(1,0,1)).is(Blocks.BRICKS),"paste copied last block");
                        check(document().getListOrEmpty("actions").size()==1,"paste action persisted");
                        int fx=x+12;
                        cmd("data modify storage space_editor:runtime selection set value {a:[I;"+fx+","+y+","+z+"],b:[I;"+fx+","+y+","+z+"],dimension:\"minecraft:overworld\"}");
                        cmd("function space_editor:region/create");
                        cmd("data modify storage space_editor:runtime hit set from storage space_editor:document regions[1]");
                        cmd("data modify storage space_editor:runtime activeTool set value \"fill\"");
                        pcmd("item replace entity @s weapon.offhand with minecraft:gold_block");
                        pcmd("function space_editor:region/apply_hit");
                        check(h.getLevel().getBlockState(new BlockPos(fx,y,z)).is(Blocks.GOLD_BLOCK),"main-hand block filled");
                        check(regions().size()==1,"successful fill removed only its Region");
                        step=3;
                    } else if (waitTicks>20) throw new AssertionError("paste job timeout");
                } else if (step==3) {
                    cmd("function space_editor:load");
                    check(document().getListOrEmpty("templates").size()==1,"reload preserves template registry");
                    check(document().getListOrEmpty("actions").size()==1,"reload preserves paste action");
                    System.out.println("SPACE_EDITOR_STAGE2_RUNTIME_PASS: fill wand cleanup, clicked-block paste anchor, template archive, split clone copy/paste, action persistence, reload persistence");
                    finished=true; h.succeed();
                }
            } catch (Throwable ex) { finished=true; ex.printStackTrace(); h.fail(ex.getMessage()); }
        });
    }

    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion();
        TestFunctionLoader.registerLoader(new TestFunctionLoader() {
            public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register) {
                register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorStage2GameTest::test);
            }
        });
        Path universe=Path.of(args[0]).toAbsolutePath().normalize();
        Path allowed=Path.of("build/test-server").toAbsolutePath().normalize();
        if(!universe.startsWith(allowed)||Files.exists(universe)) throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/stage2-runtime-report.xml").toAbsolutePath().toString()}, ignored -> {});
    }
}
