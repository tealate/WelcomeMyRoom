import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;
import net.minecraft.SharedConstants;
import net.minecraft.server.Bootstrap;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.EmptyBlockGetter;
import net.minecraft.world.level.block.Block;

public class DumpBlockProperties {
    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion();
        Bootstrap.bootStrap();
        List<String> lines = BuiltInRegistries.BLOCK.entrySet().stream()
            .sorted(java.util.Comparator.comparing(e -> e.getKey().identifier().toString()))
            .map(e -> e.getKey().identifier() + "\t" +
                e.getValue().getStateDefinition().getProperties().stream()
                    .map(p -> p.getName() + "=" + p.getPossibleValues().stream().map(String::valueOf).collect(Collectors.joining("|")))
                    .collect(Collectors.joining(",")) + "\t" +
                e.getValue().getStateDefinition().getPossibleStates().stream().allMatch(s ->
                    Block.isShapeFullBlock(s.getCollisionShape(EmptyBlockGetter.INSTANCE, BlockPos.ZERO))))
            .toList();
        Files.write(Path.of(args[0]), lines);
    }
}
