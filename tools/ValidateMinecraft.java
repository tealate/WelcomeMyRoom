// Uses the actual 26.1 command dispatcher; never opens a player world.
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import net.minecraft.SharedConstants;
import net.minecraft.server.Bootstrap;
import net.minecraft.commands.*;
import net.minecraft.data.registries.VanillaRegistries;
import net.minecraft.server.permissions.PermissionSet;

public class ValidateMinecraft {
    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion();
        Bootstrap.bootStrap();
        var registries = VanillaRegistries.createLookup();
        var commands = new Commands(Commands.CommandSelection.ALL, Commands.createValidationContext(registries));
        var dispatcher = commands.getDispatcher();
        var source = Commands.createCompilationContext(PermissionSet.ALL_PERMISSIONS);
        Map<String,String> values = new HashMap<>();
        values.put("dim", "minecraft:overworld"); values.put("dimension", "minecraft:overworld");
        values.put("palette", "stone"); values.put("variant", "normal"); values.put("block", "minecraft:stone");
        values.put("point", "a"); values.put("label", "test"); values.put("type", "mask");
        Pattern macro = Pattern.compile("\\$\\(([^)]+)\\)");
        int count = 0, errors = 0;
        for (Path path : Files.walk(Path.of(args[0])).filter(p -> p.toString().endsWith(".mcfunction")).sorted().toList()) {
            var lines = Files.readAllLines(path);
            for (int i=0; i<lines.size(); i++) {
                String line = lines.get(i).strip();
                if (line.isEmpty() || line.startsWith("#")) continue;
                if (line.startsWith("$")) {
                    Map<String,String> lineValues = new HashMap<>(values);
                    String file = path.getFileName().toString();
                    if (path.toString().contains("transform\\apply_axis_waterlogged")) {
                        lineValues.put("block", "minecraft:iron_chain"); lineValues.put("axis", "x"); lineValues.put("waterlogged", "false");
                    } else if (path.toString().contains("transform\\apply_axis")) {
                        lineValues.put("block", "minecraft:oak_log"); lineValues.put("axis", "x"); lineValues.put("waterlogged", "false");
                    } else if (path.toString().contains("transform\\apply_special_wall")) {
                        lineValues.put("block", "minecraft:cobblestone_wall"); lineValues.put("north", "none"); lineValues.put("east", "none"); lineValues.put("south", "none"); lineValues.put("west", "none"); lineValues.put("up", "true"); lineValues.put("waterlogged", "false");
                    } else if (path.toString().contains("transform\\apply_special_fence") || path.toString().contains("transform\\apply_fence")) {
                        lineValues.put("block", "minecraft:oak_fence"); lineValues.put("north", "false"); lineValues.put("east", "false"); lineValues.put("south", "false"); lineValues.put("west", "false"); lineValues.put("waterlogged", "false");
                    } else if (path.toString().contains("transform\\apply_connections")) {
                        lineValues.put("block", "minecraft:oak_fence"); lineValues.put("north", "false"); lineValues.put("east", "false"); lineValues.put("south", "false"); lineValues.put("west", "false"); lineValues.put("waterlogged", "false");
                    } else if (path.toString().contains("transform\\apply_slab")) {
                        lineValues.put("block", "minecraft:stone_slab"); lineValues.put("type", "bottom"); lineValues.put("waterlogged", "false");
                    } else if (path.toString().contains("transform\\apply_stairs")) {
                        lineValues.put("block", "minecraft:oak_stairs"); lineValues.put("facing", "north"); lineValues.put("half", "bottom"); lineValues.put("shape", "straight"); lineValues.put("waterlogged", "false");
                    } else if (path.toString().contains("transform\\apply_wall")) {
                        lineValues.put("block", "minecraft:cobblestone_wall"); lineValues.put("north", "none"); lineValues.put("east", "none"); lineValues.put("south", "none"); lineValues.put("west", "none"); lineValues.put("up", "true"); lineValues.put("waterlogged", "false");
                    }
                    line = macro.matcher(line.substring(1)).replaceAll(m -> Matcher.quoteReplacement(lineValues.getOrDefault(m.group(1), "1")));
                }
                count++;
                try { Commands.validateParseResults(dispatcher.parse(line, source)); }
                catch (Exception ex) {
                    errors++;
                    System.out.println("ERROR " + path + ":" + (i+1) + " " + ex.getMessage());
                    System.out.println("  " + line);
                }
            }
        }
        System.out.println("VALIDATION commands=" + count + " errors=" + errors);
        System.exit(errors == 0 ? 0 : 1);
    }
}
