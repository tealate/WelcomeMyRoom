// Integration tests run through Mojang's GameTestServer, with no client,
// account, network listener, or access to the user's Minecraft saves.
import java.nio.file.*;
import java.util.*;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.resources.*;
import net.minecraft.nbt.*;
import net.minecraft.world.level.block.Blocks;

public class SpaceEditorGameTest {
    static GameTestHelper helper;
    static CommandSourceStack source;
    static int step;
    static long started;
    static long waitUntil;
    static net.minecraft.server.level.ServerPlayer player;
    static int remoteId;
    static boolean finished;
    static List<Runnable> steps = new ArrayList<>();
    static final Identifier DATA = Identifier.parse("editor:data");
    static final Identifier RUNTIME = Identifier.parse("editor:runtime");
    static CompoundTag data() { return helper.getLevel().getServer().getCommandStorage().get(DATA); }
    static CompoundTag runtime() { return helper.getLevel().getServer().getCommandStorage().get(RUNTIME); }
    static ListTag objects() { return data().getCompoundOrEmpty("document").getListOrEmpty("objects"); }
    static void cmd(String s) { helper.getLevel().getServer().getCommands().performPrefixedCommand(source, s); }
    static void pcmd(String s) { helper.getLevel().getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withPermission(net.minecraft.server.permissions.PermissionSet.ALL_PERMISSIONS),s); }
    static long count(String tag) { long result=0; for(var e:helper.getLevel().getAllEntities()) if(e.entityTags().contains(tag))result++; return result; }
    static void check(boolean value, String message) { if (!value) throw new AssertionError(message + " DATA=" + data() + " RUNTIME=" + runtime()); }
    static void select(int x1,int y1,int z1,int x2,int y2,int z2) {
        cmd("function editor:selection/set {ax:"+x1+",ay:"+y1+",az:"+z1+",bx:"+x2+",by:"+y2+",bz:"+z2+",dimension:\"minecraft:overworld\"}");
        check(data().getCompoundOrEmpty("selection").contains("valid"), "selection valid");
    }
    static void block(int x,int y,int z,net.minecraft.world.level.block.Block block) {
        check(helper.getLevel().getBlockState(new BlockPos(x,y,z)).is(block), "block at "+x+","+y+","+z+" expected "+block);
    }
    static void test(GameTestHelper h) {
        helper=h; source=h.getLevel().getServer().createCommandSourceStack();
        step=0; started=h.getTick(); waitUntil=0; finished=false; steps.clear();
        steps.add(() -> {
            cmd("function editor:load");
            check(data().getCompoundOrEmpty("document").getIntOr("schema",0)==1,"initialized");
            // Keep the test region loaded; worker must preserve our ticket.
            cmd("forceload add -32 -32 32 32");
            select(-1,80,-1,-2,80,-2);
            check(data().getCompoundOrEmpty("selection").getIntOr("x1",0)==-2,"negative/reversed normalization");
            cmd("function editor:block/place");
        });
        steps.add(() -> { check(objects().size()==1,"first fill recorded"); block(-2,80,-2,Blocks.STONE); select(-1,80,-1,-1,80,-1);cmd("function editor:palette/dirt");cmd("function editor:block/place"); });
        steps.add(() -> { block(-1,80,-1,Blocks.DIRT);cmd("function editor:history/undo"); });
        steps.add(() -> { check(objects().size()==1,"undo document");block(-1,80,-1,Blocks.STONE);cmd("function editor:history/redo"); });
        steps.add(() -> { block(-1,80,-1,Blocks.DIRT);cmd("function editor:objects/delete {id:1}"); });
        steps.add(() -> { block(-2,80,-2,Blocks.AIR);block(-1,80,-1,Blocks.DIRT);cmd("function editor:history/undo"); });
        steps.add(() -> { block(-2,80,-2,Blocks.STONE);cmd("function editor:block/erase"); });
        steps.add(() -> { block(-1,80,-1,Blocks.AIR);cmd("function editor:history/undo"); });
        steps.add(() -> { block(-1,80,-1,Blocks.DIRT); select(0,80,0,0,82,2);cmd("function editor:settings/offset {x:-0.01,y:0,z:0}");cmd("function editor:mask/create"); });
        steps.add(() -> {
            check(objects().size()==3,"mask recorded"); var mask=objects().getCompoundOrEmpty(2);
            check(Math.abs(mask.getDoubleOr("px",99)+0.01)<0.00001,"fractional offset preserved");
            check(mask.getDoubleOr("sy",0)==3,"inclusive bounds size");
            cmd("function editor:teleport/create");
        });
        steps.add(() -> { check(objects().size()==4,"teleport recorded");cmd("function editor:objects/list");cmd("function editor:export");cmd("function editor:build"); });
        steps.add(() -> { block(-1,80,-1,Blocks.DIRT); check(objects().size()==4,"rebuild retains document");cmd("function editor:build"); });
        steps.add(() -> {
            check(data().getStringOr("build_state","").equals("clean"),"rebuild is clean");
            check(count("editor.mask")==1,"one mask after repeated rebuild");
            check(count("editor.guide")==2,"one guide per mask/TP");
            for(var entity:h.getLevel().getAllEntities()) if(entity.entityTags().contains("editor.mask")) {
                check(Math.abs(entity.getX()+0.01)<0.000001 && entity.getZ()==0,"display origin is exact, without implicit block centering");
            }
            // Explicit invalid selections must invalidate earlier valid bounds.
            cmd("function editor:selection/set {ax:0,ay:80,az:0,bx:32,by:80,bz:0,dimension:\"minecraft:overworld\"}");
            check(!data().getCompoundOrEmpty("selection").contains("valid"),"oversize rejected");
            cmd("function editor:block/place"); check(objects().size()==4,"invalid selection cannot place");
            cmd("function editor:load");check(objects().size()==4,"reload preserves authored data");
            select(16,80,16,20,84,20);cmd("function editor:block/hollow");
        });
        steps.add(() -> { block(16,80,16,Blocks.DIRT);block(18,82,18,Blocks.AIR);cmd("function editor:selection/east");check(data().getCompoundOrEmpty("selection").getIntOr("x1",0)==17,"selection move");
            player=h.makeMockServerPlayerInLevel();player.setNoGravity(true);player.setGameMode(net.minecraft.world.level.GameType.CREATIVE);
            player.setPos(8.5,80,8.5);player.setYRot(0);player.setXRot(0);
            pcmd("function editor:start");pcmd("function editor:menu");
            check(player.entityTags().contains("editor.editing"),"editor mode");
            check(player.getMainHandItem().is(net.minecraft.world.item.Items.CARROT_ON_A_STICK),"wand was given");
            cmd("setblock 8 81 11 minecraft:stone");pcmd("scoreboard players set @s se.use 1");
        });
        steps.add(() -> {check(data().getCompoundOrEmpty("selection").getIntOr("ax",-999)==8,"wand raycast A x");check(data().getCompoundOrEmpty("selection").getIntOr("az",-999)==11,"wand raycast A z");
            player.setPos(9.5,80,8.5);player.setShiftKeyDown(true);player.setPose(net.minecraft.world.entity.Pose.CROUCHING);cmd("setblock 9 81 11 minecraft:stone");pcmd("function editor:internal/wand");
        });
        steps.add(() -> {check(data().getCompoundOrEmpty("selection").getIntOr("bx",-999)==9,"sneak wand B");player.setShiftKeyDown(false);player.setPose(net.minecraft.world.entity.Pose.STANDING);
            player.setPos(12,80,12);player.setYRot(45);player.setXRot(0);
            int tp=objects().getCompoundOrEmpty(3).getIntOr("id",0);pcmd("function editor:teleport/link {id:"+tp+"}");
            check(objects().getCompoundOrEmpty(3).contains("target"),"teleport link stored");
            player.setPos(.5,80,1.5);pcmd("function editor:internal/teleport/tick");check(Math.abs(player.getX()-.5)<0.01,"editing excludes teleport");
            pcmd("function editor:play");pcmd("scoreboard players set @s se.cd 0");pcmd("function editor:internal/teleport/tick");
            check(Math.abs(player.getX()-12)<0.01 && Math.abs(player.getZ()-12)<0.01,"linked teleport moves player without coordinate centering");
            check(Math.abs(player.getYRot()-45)<0.01,"linked teleport preserves target rotation");
            pcmd("function editor:objects/list");pcmd("function editor:export");
            select(2048,80,2048,2048,82,2050);cmd("function editor:mask/create");
            remoteId=data().getIntOr("next_id",0)-1;
            // A reload while the durable queue is pending must keep the job.
            cmd("function editor:load");check(runtime().contains("job"),"pending job survives reload");
        });
        steps.add(() -> {
            cmd("execute store success storage editor:test kept byte 1 run forceload query 0 0");
            cmd("execute store success storage editor:test remote byte 1 run forceload query 2032 2048");
            var tickets=h.getLevel().getServer().getCommandStorage().get(Identifier.parse("editor:test"));
            check(tickets.getBooleanOr("kept",false),"preexisting force-load preserved");
            check(!tickets.getBooleanOr("remote",true),"worker force-load released");
            cmd("forceload add 2032 2048");waitUntil=h.getTick()+20;
        });
        steps.add(() -> {check(count("editor.mask")==2,"remote mask rendered across offset chunk boundary");
            cmd("forceload remove 2032 2048");
            waitUntil=h.getTick()+400;
        });
        steps.add(() -> {cmd("function editor:objects/delete {id:"+remoteId+"}");});
        steps.add(() -> {check(count("editor.mask")==1,"deleted remote mask swept");
            cmd("function editor:history/undo");
        });
        steps.add(() -> {cmd("forceload add 2032 2048");waitUntil=h.getTick()+20;});
        steps.add(() -> {check(count("editor.mask")==2,"undo restores remote mask");
            cmd("function editor:objects/select {id:4}");cmd("function editor:settings/offset {x:0,y:0,z:-0.125}");cmd("function editor:objects/update {id:4}");
        });
        steps.add(() -> {check(objects().size()==6,"update preserves object count");
            boolean found=false;
            for(var entity:h.getLevel().getAllEntities()) if(entity.entityTags().contains("editor.mask") && entity.getX()<100) {
                check(entity.getX()==0 && entity.getZ()==-.125,"update applies exact transform");found=true;
            }
            check(found,"updated mask exists");
            cmd("function editor:objects/select {id:4}");cmd("function editor:block/place");
        });
        steps.add(() -> {block(0,82,2,Blocks.DIRT);check(!objects().getCompoundOrEmpty(6).contains("px"),"block created from mask selection cannot inherit display transform");cmd("function editor:history/undo");});
        steps.add(() -> {
            // GameTest advances ticks without real-time pacing. Warm this
            // dimension synchronously so disk/worldgen latency is not mistaken
            // for a 60-second production timeout in a sub-second test run.
            h.getLevel().getServer().getLevel(net.minecraft.world.level.Level.NETHER).getChunk(2,2);
            cmd("function editor:selection/set {ax:32,ay:80,az:32,bx:33,by:80,bz:33,dimension:\"minecraft:the_nether\"}");cmd("function editor:palette/stone");cmd("function editor:block/place");
        });
        steps.add(() -> {
            var nether=h.getLevel().getServer().getLevel(net.minecraft.world.level.Level.NETHER);
            check(nether.getBlockState(new BlockPos(32,80,32)).is(Blocks.STONE),"nether placement");
            cmd("function editor:selection/set {ax:0,ay:-1,az:0,bx:0,by:0,bz:0,dimension:\"minecraft:the_nether\"}");
            check(!data().getCompoundOrEmpty("selection").contains("valid"),"nether height bounds");
            cmd("function editor_import:load");
        });
        steps.add(() -> {check(objects().size()==4,"external JSON import replaces document");block(16,80,16,Blocks.AIR);cmd("function editor:history/undo");});
        steps.add(() -> {check(objects().size()==7,"undo restores pre-import document");block(16,80,16,Blocks.DIRT);
            helper.getLevel().getServer().saveEverything(true,false,true);
            System.out.println("SPACE_EDITOR_RUNTIME_PASS: normalization, overlap, undo, redo, delete, erase, fractional mask, no duplicate displays, teleport registration/link/activation, rebuild twice, invalid selection, reload, hollow room, selection move, player menu, wand A/B, force-load ownership, remote deletion, object update, mask-to-block selection, nether, JSON import/undo");
            finished=true;h.succeed();
        });
        h.onEachTick(() -> {
            if(finished) return;
            try {
                if (runtime().contains("job")) {
                    check(!runtime().getCompoundOrEmpty("job").getStringOr("phase","").equals("error"),"worker failed");
                    return;
                }
                if(h.getTick()<waitUntil) return;
                if (step<steps.size()) {System.out.println("SPACE_EDITOR_STEP "+step); steps.get(step++).run();}
            } catch (Throwable ex) { finished=true;ex.printStackTrace(); h.fail(ex.getMessage()); }
        });
    }
    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion();
        TestFunctionLoader.registerLoader(new TestFunctionLoader() {
            public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register) {
                register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorGameTest::test);
            }
        });
        // GameTestMainUtil clears its universe directory. Refuse existing paths
        // and require an explicit path inside this workspace's build folder.
        Path universe=Path.of(args[0]).toAbsolutePath().normalize();
        Path allowed=Path.of("build/test-server").toAbsolutePath().normalize();
        if(!universe.startsWith(allowed)||Files.exists(universe)) throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/runtime-report.xml").toAbsolutePath().toString()}, ignored -> {});
    }
}
