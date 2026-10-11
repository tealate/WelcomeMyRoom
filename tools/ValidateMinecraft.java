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
                    line = macro.matcher(line.substring(1)).replaceAll(m -> Matcher.quoteReplacement(values.getOrDefault(m.group(1), "1")));
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
