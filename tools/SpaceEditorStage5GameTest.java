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
    static final Identifier DOCUMENT=Identifier.parse("space_editor:document");
    static final Identifier RUNTIME=Identifier.parse("space_editor:runtime");
    static CompoundTag document(){return helper.getLevel().getServer().getCommandStorage().get(DOCUMENT);}
    static CompoundTag runtime(){return helper.getLevel().getServer().getCommandStorage().get(RUNTIME);}
    static void cmd(String value){helper.getLevel().getServer().getCommands().performPrefixedCommand(source,value);}
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
    }
    static void test(GameTestHelper h){
        helper=h;source=h.getLevel().getServer().createCommandSourceStack();
        try{
            cmd("function space_editor:load");
            mappingTests();
            System.out.println("SPACE_EDITOR_STAGE5_RUNTIME_PASS: 64 pose combinations, forward/inverse point/vector/look, exact fractional centers");
            h.succeed();
        }catch(Throwable ex){ex.printStackTrace();h.fail(ex.getMessage());}
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
