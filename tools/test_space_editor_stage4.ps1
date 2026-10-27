param([string]$JavaHome = "")
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
if (-not $JavaHome) { $JavaHome = (Get-ChildItem build/test-server/java25 -Directory | Select-Object -First 1).FullName }
if (-not (Test-Path -LiteralPath "$JavaHome/bin/java.exe")) { throw 'Java 25 JDK is required.' }
$libraryPaths = (Get-ChildItem build/test-server/libraries -Recurse -Filter '*.jar').FullName
$serverJar = (Resolve-Path 'build/test-server/versions/26.1/server-26.1.jar').Path
$classPath = ($libraryPaths + $serverJar) -join ';'
$packRoot = 'build/test-server/packs-stage4'
New-Item -ItemType Directory -Force "$packRoot/integration/data/editor_test/test_instance" | Out-Null
Copy-Item space_editor_datapack/pack.mcmeta "$packRoot/integration/pack.mcmeta" -Force
Copy-Item space_editor_datapack -Destination $packRoot -Recurse -Force
'{"type":"minecraft:function","environment":"minecraft:default","function":"editor_test:integration","max_ticks":6000,"required":true,"setup_ticks":1,"structure":"minecraft:empty"}' | Set-Content "$packRoot/integration/data/editor_test/test_instance/integration.json" -Encoding utf8
& "$JavaHome/bin/javac.exe" -encoding UTF-8 -cp $classPath -d build/test-server tools/ValidateMinecraft.java tools/SpaceEditorStage4GameTest.java
if ($LASTEXITCODE -ne 0) { throw 'Harness compilation failed' }
& "$JavaHome/bin/java.exe" -Xmx1G -cp "$classPath;build/test-server" ValidateMinecraft space_editor_datapack > build/test-server/stage4-command-validation.log 2>&1
if ($LASTEXITCODE -ne 0) { Get-Content build/test-server/stage4-command-validation.log; throw 'Minecraft command validation failed' }
$runPath = Join-Path $projectRoot ('build/test-server/run-stage4-' + [guid]::NewGuid().ToString('N'))
& "$JavaHome/bin/java.exe" -Xmx2G -cp "$classPath;build/test-server" SpaceEditorStage4GameTest $runPath $packRoot > build/test-server/stage4-runtime-validation.log 2>&1
$testExit = $LASTEXITCODE
Write-Output "Test world: $runPath/gametestworld"
Get-Content build/test-server/stage4-command-validation.log | Select-String 'VALIDATION|ERROR'
Get-Content build/test-server/stage4-runtime-validation.log | Select-String 'SPACE_EDITOR_STAGE4_RUNTIME_PASS|ERROR|required tests passed|AssertionError' | ForEach-Object { if ($_.Line.Length -gt 1000) { $_.Line.Substring(0,1000) } else { $_.Line } }
if ($testExit -ne 0) { throw 'Minecraft GameTest failed; inspect build/test-server/stage4-runtime-validation.log' }
