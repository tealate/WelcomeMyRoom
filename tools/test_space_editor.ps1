param([string]$JavaHome = "", [string]$Python = "")
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
if (-not $JavaHome) {
    $JavaHome = (Get-ChildItem build/test-server/java25 -Directory | Select-Object -First 1).FullName
}
if (-not (Test-Path -LiteralPath "$JavaHome/bin/java.exe")) { throw 'Java 25 JDK is required.' }
$libraryPaths = (Get-ChildItem build/test-server/libraries -Recurse -Filter '*.jar').FullName
$serverJar = (Resolve-Path 'build/test-server/versions/26.1/server-26.1.jar').Path
$classPath = ($libraryPaths + $serverJar) -join ';'
New-Item -ItemType Directory -Force build/test-server/packs/integration/data/editor_test/test_instance | Out-Null
Copy-Item space_editor_datapack/pack.mcmeta build/test-server/packs/integration/pack.mcmeta -Force
Copy-Item space_editor_datapack -Destination build/test-server/packs -Recurse -Force
if (-not $Python) { $Python = "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe" }
& $Python tools/editor_data.py pack tests/fixtures/roundtrip.json --out build/test-server/roundtrip.zip
if ($LASTEXITCODE -ne 0) { throw 'Roundtrip fixture compilation failed' }
Expand-Archive -LiteralPath build/test-server/roundtrip.zip -DestinationPath build/test-server/packs/roundtrip -Force
'{"type":"minecraft:function","environment":"minecraft:default","function":"editor_test:integration","max_ticks":6000,"required":true,"setup_ticks":1,"structure":"minecraft:empty"}' | Set-Content build/test-server/packs/integration/data/editor_test/test_instance/integration.json -Encoding utf8
& "$JavaHome/bin/javac.exe" -encoding UTF-8 -cp $classPath -d build/test-server tools/ValidateMinecraft.java tools/SpaceEditorGameTest.java
if ($LASTEXITCODE -ne 0) { throw 'Harness compilation failed' }
& "$JavaHome/bin/java.exe" -Xmx1G -cp "$classPath;build/test-server" ValidateMinecraft space_editor_datapack > build/test-server/command-validation.log 2>&1
if ($LASTEXITCODE -ne 0) { Get-Content build/test-server/command-validation.log; throw 'Minecraft command validation failed' }
$runPath = Join-Path $projectRoot ('build/test-server/run-' + [guid]::NewGuid().ToString('N'))
# The Java harness also checks that this is a fresh directory inside build/.
& "$JavaHome/bin/java.exe" -Xmx2G -cp "$classPath;build/test-server" SpaceEditorGameTest $runPath build/test-server/packs > build/test-server/runtime-validation.log 2>&1
$testExit = $LASTEXITCODE
Write-Output "Test world: $runPath/gametestworld"
Get-Content build/test-server/command-validation.log | Select-String 'VALIDATION|ERROR'
Get-Content build/test-server/runtime-validation.log | Select-String 'SPACE_EDITOR_STEP|SPACE_EDITOR_RUNTIME_PASS|ERROR|required tests passed' | ForEach-Object { if ($_.Line.Length -gt 500) { $_.Line.Substring(0,500) } else { $_.Line } }
if ($testExit -ne 0) { throw 'Minecraft GameTest failed; inspect build/test-server/runtime-validation.log' }
