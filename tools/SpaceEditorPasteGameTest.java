// Dedicated paste regressions on the actual 26.1 server, in a disposable world.
// Reuses only the existing Stage 03 harness's command/storage helpers.
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.function.*;
import net.minecraft.SharedConstants;
import net.minecraft.core.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.*;
import net.minecraft.nbt.*;
import net.minecraft.resources.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.*;

public class SpaceEditorPasteGameTest extends SpaceEditorStage3GameTest {
    static int phase, index, ticks, specialId;
    static boolean ended, loadedDuringPlace;
    static UUID sentinel;
    static CompletableFuture<Void> reload;
    static CompoundTag savedJob;
    static BlockState[] states = new BlockState[64];
    static int maxCommands;
    static final int DX=64, DZ=0;
    static CompoundTag job(){return document().getCompoundOrEmpty("job");}
    static void tickJob(){
        if(!jobState().equals("running"))return;
        var measured=new java.util.concurrent.atomic.AtomicReference<net.minecraft.commands.execution.ExecutionContext<net.minecraft.commands.CommandSourceStack>>();
        net.minecraft.commands.Commands.executeCommandInContext(source,context->{measured.set(context);cmd("function space_editor:job/tick");});
        try{
            var type=net.minecraft.commands.execution.ExecutionContext.class;
            var limit=type.getDeclaredField("commandLimit");limit.setAccessible(true);
            var quota=type.getDeclaredField("commandQuota");quota.setAccessible(true);
            check(limit.getInt(measured.get())==65536,"default command limit retained");
            int used=65536-quota.getInt(measured.get());
            check(used<65536,"paste tick stays within command limit");maxCommands=Math.max(maxCommands,used);
        }catch(ReflectiveOperationException ex){throw new AssertionError(ex);}
    }
    static BlockPos src(int i){return new BlockPos(i%8,TY+i/32,(i/8)%4);}
    static BlockPos dest(int i,int rot,int flip){
        int x=i%8,y=i/32,z=(i/8)%4,tx=x,tz=z;
        if(rot==90){tx=3-z;tz=x;}
        if(rot==180){tx=7-x;tz=3-z;}
        if(rot==270){tx=z;tz=7-x;}
        return new BlockPos(DX+tx,TY+(flip==1?1-y:y),DZ+tz);
    }
    static String xyz(BlockPos p){return p.getX()+" "+p.getY()+" "+p.getZ();}
    static void block(BlockPos p,String b){cmd("setblock "+xyz(p)+" "+b+" strict");}
    static void wand(boolean masked){pcmd("item replace entity @s weapon.mainhand with minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\""+(masked?"paste_masked":"paste")+"\"}}]");}
    static void fixture(){
        cmd("data modify storage space_editor:document templates set value []");
        cmd("data modify storage space_editor:document nextTemplateId set value 1");
        cmd("data modify storage space_editor:document actions set value []");
        for(int i=0;i<64;i++){
            String b="minecraft:stone";
            if(i<3)b=new String[]{"minecraft:air","minecraft:cave_air","minecraft:void_air"}[i];
            if(i==4)b="minecraft:oak_stairs[facing=north,half=bottom,shape=inner_left,waterlogged=true]";
            if(i==5)b="minecraft:oak_slab[type=bottom,waterlogged=true]";
            if(i==6)b="minecraft:iron_chain[axis=x,waterlogged=true]";
            if(i>=8&&i<24)b="minecraft:water[level="+(i-8)+"]";
            if(i>=24&&i<40)b="minecraft:lava[level="+(i-24)+"]";
            block(src(i),b); states[i]=helper.getLevel().getBlockState(src(i));
        }
        cmd("data modify storage space_editor:runtime hit set value {dimension:\"minecraft:overworld\",x1m:0,x2m:8000,y1m:80000,y2m:82000,z1m:0,z2m:4000}");
        pcmd("function space_editor:copy/start");
        check(jobState().equals("running"),"fluid copy started");
    }
    static void extraTemplates(){
        for(int i=0;i<64;i++)block(new BlockPos(AX+64+i%8,AY+i/32,AZ+(i/8)%4),new String[]{"minecraft:air","minecraft:cave_air","minecraft:void_air"}[i%3]);
        cmd("fill "+(AX+96)+" "+AY+" "+AZ+" "+(AX+127)+" "+(AY+1)+" "+(AZ+15)+" minecraft:air strict");
        block(new BlockPos(AX+128,AY,AZ),"minecraft:water[level=0]");
        block(new BlockPos(AX+129,AY,AZ),"minecraft:lava[level=0]");
        for(int[] v:new int[][]{{2,64,8,2,4},{3,96,32,2,16},{5,128,1,1,1},{6,129,1,1,1}})
            cmd("data modify storage space_editor:document templates append value {id:"+v[0]+",version:1,archive:{dimension:\"minecraft:overworld\",x:"+(AX+v[1])+",y:"+AY+",z:"+AZ+"},size:[I;"+v[2]+","+v[3]+","+v[4]+"]}");
    }
    static void startCase(){
        int transform=index%8,rot=(transform%4)*90,flip=transform/4;
        boolean masked=(index/8)%2==1;
        int id=index<16?1:2;
        cmd("gamerule minecraft:max_block_modifications 32768");
        cmd("fill 64 80 0 71 81 7 minecraft:gold_block strict");
        cmd("kill @e[tag=paste_sentinel]");
        block(dest(0,rot,flip),"minecraft:chest[facing=north]{Items:[{Slot:0b,id:\"minecraft:diamond\",count:3}]}");
        // Use the configured collision carrier so the normal orphan cleanup is relevant.
        cmd("function space_editor:paste/cancel");
        // Existing special collision carriers are included in this tag; pick the first.
        var collision=helper.getLevel().registryAccess().lookupOrThrow(Registries.BLOCK)
            .getOrThrow(net.minecraft.tags.TagKey.create(Registries.BLOCK,Identifier.parse("space_editor:special_collision"))).iterator().next().value();
        helper.getLevel().setBlock(dest(1,rot,flip),collision.defaultBlockState(),Block.UPDATE_CLIENTS|Block.UPDATE_KNOWN_SHAPE);
        cmd("execute positioned "+xyz(dest(1,rot,flip))+" run summon minecraft:block_display ~ ~ ~ {Tags:[\"space_editor.special\",\"paste_sentinel\"],block_state:{Name:\"minecraft:stone\"}}");
        var entity=java.util.stream.StreamSupport.stream(helper.getLevel().getAllEntities().spliterator(),false).filter(e->e.entityTags().contains("paste_sentinel")).findFirst().orElseThrow();
        sentinel=entity.getUUID(); specialId=9000+index;
        cmd("scoreboard players set @e[tag=paste_sentinel] se.sid "+specialId);
        cmd("data modify storage space_editor:document specials append value {id:"+specialId+",test:1b}");
        block(dest(2,rot,flip),"minecraft:barrel{Items:[{Slot:0b,id:\"minecraft:emerald\",count:2}]}");
        wand(masked); pcmd("function space_editor:paste_mode/begin");
        pcmd("scoreboard players set @s se.rot "+rot); pcmd("scoreboard players set @s se.flip "+flip);
        pcmd("item replace entity @s weapon.offhand with minecraft:paper[minecraft:custom_data={space_editor:{kind:\"template\",templateId:"+id+"}}]");
        cmd("data modify storage space_editor:runtime hover set value {dimension:\"minecraft:overworld\",pos:[I;64,80,0]}");
        pcmd("function space_editor:input/paste");
        check(runtime().getCompoundOrEmpty("pastePending").getBooleanOr("masked",false)==masked,"preview captures wand mode "+index);
        wand(!masked); pcmd("function space_editor:paste_mode/held_tick");
        check(score("se.rot")==rot && score("se.flip")==flip,"switch between paste tools retains session");
        pcmd("scoreboard players set @s se.ph 0"); pcmd("function space_editor:paste_mode/held_tick");
        check(score("se.rot")==rot && score("se.flip")==flip,"re-equip restores pending transform");
        pcmd("function space_editor:input/paste");
        check(job().getBooleanOr("masked",false)==masked && jobState().equals("running"),"confirm retains preview mode after switching wand");
        ticks=0;
    }
    static void verifyCase(){
        int transform=index%8,rot=transform%4*90,flip=transform/4;
        boolean masked=(index/8)%2==1,empty=index>=16;
        check(jobState().equals("complete")||jobState().equals("done"),"paste completes case="+index);
        for(int i=0;i<64;i++){
            BlockState actual=helper.getLevel().getBlockState(dest(i,rot,flip));
            if((empty||i<3)&&masked){
                if(i==0)check(actual.is(Blocks.CHEST)&&helper.getLevel().getBlockEntity(dest(i,rot,flip)) instanceof net.minecraft.world.level.block.entity.ChestBlockEntity chest&&chest.getItem(0).getCount()==3,"Air preserves chest inventory");
                else if(i==1)check(helper.getLevel().getEntity(sentinel)!=null,"Air preserves special display UUID");
                else if(i==2)check(actual.is(Blocks.BARREL)&&helper.getLevel().getBlockEntity(dest(i,rot,flip)) instanceof net.minecraft.world.level.block.entity.BarrelBlockEntity barrel&&barrel.getItem(0).getCount()==2,"Air preserves barrel inventory");
                else check(actual.is(Blocks.GOLD_BLOCK),"empty template leaves destination intact");
            }else if(empty||i<3)check(actual.isAir()&&helper.getLevel().getBlockEntity(dest(i,rot,flip))==null,"normal paste overwrites Air "+i);
            else {
                BlockState expected=states[i].rotate(new Rotation[]{Rotation.NONE,Rotation.CLOCKWISE_90,Rotation.CLOCKWISE_180,Rotation.COUNTERCLOCKWISE_90}[rot/90]);
                if(flip==1 && expected.hasProperty(BlockStateProperties.HALF))expected=expected.setValue(BlockStateProperties.HALF,Half.TOP);
                if(flip==1 && expected.hasProperty(BlockStateProperties.SLAB_TYPE))expected=expected.setValue(BlockStateProperties.SLAB_TYPE,SlabType.TOP);
                check(actual.equals(expected),"exact state including fluid level/waterlogged case="+index+" cell="+i+" expected="+expected+" actual="+actual);
            }
        }
        check(job().getIntOr("unsupportedBlocks",0)==0&&job().getIntOr("skippedBlocks",0)==0,"Air and fluids are not unsupported");
        if(masked)check(document().getListOrEmpty("specials").stream().anyMatch(t->t instanceof CompoundTag c&&c.getIntOr("id",0)==specialId),"Air preserves special record");
        cmd("data remove storage space_editor:document specials[{test:1b}]");
    }
    static void startLarge(boolean transformed){
        block(new BlockPos(AX+127,AY+1,AZ+15),transformed?"minecraft:air":"minecraft:water[level=7]");
        cmd("gamerule minecraft:max_block_modifications 32768");
        cmd("fill 64 80 32 95 81 63 minecraft:gold_block strict");
        cmd("gamerule minecraft:max_block_modifications 512");
        cmd("data modify storage space_editor:runtime pasteTransform set value {rotation:"+(transformed?90:0)+",flipY:1b,masked:1b}");
        if(!transformed)cmd("data modify storage space_editor:runtime pasteTransform.flipY set value 0b");
        cmd("data modify storage space_editor:runtime targetDimension set value \"minecraft:overworld\"");
        cmd("data modify storage space_editor:runtime targetPos set value [I;64,80,32]");
        pcmd("function space_editor:paste/start {id:3}"); tickJob();
        check(jobState().equals("running"),"large job spans ticks");
        if(!transformed)check(job().getBooleanOr("emptyCheck",false)&&job().getIntOr("emptyCursor",0)==256,"empty chunk scan bounded at 256");
        savedJob=job().copy();
        reload=helper.getLevel().getServer().reloadResources(helper.getLevel().getServer().getPackRepository().getSelectedIds());
        ticks=0; loadedDuringPlace=false;
    }
    static void checkFailures(){
        for(boolean badSource:new boolean[]{true,false}){
            cmd("data modify storage space_editor:runtime pasteTransform set value {rotation:0,flipY:0b,masked:1b}");
            cmd("data modify storage space_editor:runtime targetPos set value [I;64,80,32]");
            pcmd("function space_editor:paste/start {id:2}");
            cmd("data modify storage space_editor:document job."+(badSource?"sourceX set value 25000000":"targetY set value 400"));
            tickJob();check(jobState().equals("error"),"empty clone still rejects "+(badSource?"unloaded source":"out of bounds destination"));
        }
        // A failed nonempty clone must also remain an error.
        cmd("data modify storage space_editor:runtime targetPos set value [I;64,400,32]");
        pcmd("function space_editor:paste/start {id:1}");tickJob();check(jobState().equals("error"),"nonempty invalid clone detected");
        cmd("data modify storage space_editor:runtime targetPos set value [I;64,80,32]");
        cmd("gamerule minecraft:max_block_modifications 1");
        pcmd("function space_editor:paste/start {id:2}");tickJob();check(jobState().equals("error"),"empty fallback does not hide block modification limit failure");
    }
    static void test(GameTestHelper h){
        helper=h; source=h.getLevel().getServer().createCommandSourceStack(); phase=0; index=0; ticks=0; ended=false;
        cmd("function space_editor:load");cmd("forceload add 0 0 176 96");cmd("forceload add "+AX+" "+AZ+" "+(AX+144)+" "+(AZ+16));
        player=h.makeMockServerPlayerInLevel(); player.setNoGravity(true);player.setPos(10.5,TY+4,10.5);
        h.onEachTick(()->{if(ended)return;try{
            if(phase==0){
                if(!h.getLevel().hasChunkAt(new BlockPos(AX+144,AY,AZ+16))||!h.getLevel().hasChunkAt(new BlockPos(176,80,96))){check(++ticks<300,"fixture chunks load");return;}
                pcmd("function space_editor:start");
                pcmd("execute store success storage space_editor:runtime issued byte 1 if items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"paste_masked\"}}]");
                check(runtime().getBooleanOr("issued",false),"start issues masked wand");
                pcmd("tag @s remove space_editor.editing");fixture();phase=1;ticks=0;
            }else if(phase==1){
                tickJob();check(++ticks<100,"copy completes");
                if(!jobState().equals("running")){
                    for(int i=0;i<64;i++)check(h.getLevel().getBlockState(new BlockPos(AX+i%8,AY+i/32,AZ+(i/8)%4)).equals(states[i]),"copy archives exact state "+i);
                    extraTemplates();startCase();phase=2;
                }
            }else if(phase==2){
                tickJob();check(++ticks<100,"matrix paste completes "+index);
                if(!jobState().equals("running")){verifyCase();if(++index<32)startCase();else{startLarge(false);phase=3;}}
            }else if(phase==3||phase==4){
                if(!reload.isDone()){check(++ticks<600,"resource reload completes");return;}
                reload.join();
                if(ticks!=-1){
                    for(String field:new String[]{"id","masked","rotation","flipY","mode","type","sourceX","sourceY","sourceZ","targetX","targetY","targetZ"})
                        check(Objects.equals(job().get(field),savedJob.get(field)),"real resource reload preserves Job field "+field);
                    if(phase==3)check(job().getIntOr("cursorX",0)>=savedJob.getIntOr("cursorX",0),"reload retains fast progress");
                    else check(!job().getStringOr("phase","").equals("preflight")||job().getIntOr("cursor",0)>=savedJob.getIntOr("cursor",0),"reload retains preflight progress");
                    ticks=-1;
                }
                tickJob();
                if(phase==4&&!loadedDuringPlace&&job().getStringOr("phase","").equals("place")&&job().getIntOr("cursor",0)>=64){
                    cmd("function space_editor:load");loadedDuringPlace=true;check(job().getBooleanOr("masked",false),"load during transformed placement keeps mode");
                }
                if(!jobState().equals("running")){
                    check(jobState().equals("complete")||jobState().equals("done"),"large empty job completes");
                    check(h.getLevel().getBlockState(new BlockPos(64,TY,32)).is(Blocks.GOLD_BLOCK),"large Air preserves destination");
                    if(phase==3){
                        check(job().getIntOr("completedChunks",0)==2,"fast chunk splitting retained");
                        check(h.getLevel().getBlockState(new BlockPos(95,TY+1,47)).is(Blocks.WATER)&&h.getLevel().getBlockState(new BlockPos(95,TY+1,47)).getValue(BlockStateProperties.LEVEL)==7,"nonempty fluid strip executes after empty strip");
                        startLarge(true);phase=4;
                    }
                    else{check(loadedDuringPlace,"transformed placement crossed tick boundary");checkFailures();
                        // Native strict clone retains fluid state without scheduling fluid updates.
                        cmd("gamerule minecraft:max_block_modifications 32768");
                        cmd("clone "+(AX+128)+" "+AY+" "+AZ+" "+(AX+128)+" "+AY+" "+AZ+" 144 90 80 strict replace force");
                        cmd("clone "+(AX+129)+" "+AY+" "+AZ+" "+(AX+129)+" "+AY+" "+AZ+" 160 90 80 strict replace force");
                        ticks=0;phase=5;
                    }
                }
            }else if(phase==5&&++ticks>=40){
                check(h.getLevel().getBlockState(new BlockPos(144,89,80)).isAir()&&h.getLevel().getBlockState(new BlockPos(160,89,80)).isAir(),"strict liquid clone does not initiate flow");
                cmd("setblock 145 90 80 minecraft:stone");cmd("setblock 161 90 80 minecraft:stone");ticks=0;phase=6;
            }else if(phase==6&&++ticks>=100){
                check(h.getLevel().getBlockState(new BlockPos(144,89,80)).is(Blocks.WATER)&&h.getLevel().getBlockState(new BlockPos(160,89,80)).is(Blocks.LAVA),"external block update starts vanilla liquid flow");
                System.out.println("SPACE_EDITOR_PASTE_RUNTIME_PASS: exact fluid copy; 32 normal/masked rotation/FlipY and all-Air cases; all 16 levels of water/lava; waterlogged stairs/slabs/chains; Air preserves inventories/display UUID/record; preview tool switching; split/bounded empty jobs; real resource reload and placement load; invalid/unloaded failures; strict flow resumes on neighbor update");
                System.out.println("SPACE_EDITOR_PASTE_COMMAND_BUDGET: max_commands="+maxCommands+" limit=65536");
                ended=true;h.succeed();
            }
        }catch(Throwable ex){ended=true;ex.printStackTrace();h.fail(ex.getMessage());}});
    }
    public static void main(String[] args)throws Exception{
        SharedConstants.tryDetectVersion();
        TestFunctionLoader.registerLoader(new TestFunctionLoader(){public void load(BiConsumer<ResourceKey<Consumer<GameTestHelper>>,Consumer<GameTestHelper>> register){register.accept(ResourceKey.create(Registries.TEST_FUNCTION,Identifier.parse("editor_test:integration")),SpaceEditorPasteGameTest::test);}});
        Path universe=Path.of(args[0]).toAbsolutePath().normalize();
        if(!universe.startsWith(Path.of("build/test-server").toAbsolutePath().normalize())||Files.exists(universe))throw new IllegalArgumentException("Fresh build/test-server subdirectory required");
        GameTestMainUtil.runGameTestServer(new String[]{"--universe",universe.toString(),"--packs",Path.of(args[1]).toAbsolutePath().toString(),"--tests","editor_test:integration","--report",Path.of("build/test-server/paste-runtime-report.xml").toAbsolutePath().toString()},ignored->{});
    }
}
