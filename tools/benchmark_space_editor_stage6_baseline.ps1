param([string]$BaselineRef = '63df666775715f0c86296062a5faeb6d08ca39ac', [string]$JavaHome = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
if (-not $JavaHome) { $JavaHome = (Get-ChildItem build/test-server/java25 -Directory | Select-Object -First 1).FullName }
$classPath = ((Get-ChildItem build/test-server/libraries -Recurse -Filter '*.jar').FullName + (Resolve-Path 'build/test-server/versions/26.1/server-26.1.jar').Path) -join ';'
$root = Join-Path $projectRoot ('build/test-server/baseline-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory $root | Out-Null
& git archive --format=zip "--output=$root/source.zip" $BaselineRef space_editor_datapack tools/SpaceEditorStage6GameTest.java
if ($LASTEXITCODE -ne 0) { throw 'Baseline export failed' }
Expand-Archive -LiteralPath "$root/source.zip" -DestinationPath "$root/export"
$packRoot = "$root/packs"
New-Item -ItemType Directory -Force "$packRoot/integration/data/editor_test/test_instance" | Out-Null
Copy-Item "$root/export/space_editor_datapack" $packRoot -Recurse
Copy-Item "$root/export/space_editor_datapack/pack.mcmeta" "$packRoot/integration/pack.mcmeta"
'{"type":"minecraft:function","environment":"minecraft:default","function":"editor_test:integration","max_ticks":3000,"required":true,"setup_ticks":1,"structure":"minecraft:empty"}' | Set-Content "$packRoot/integration/data/editor_test/test_instance/integration.json" -Encoding utf8
$source = Get-Content "$root/export/tools/SpaceEditorStage6GameTest.java" -Raw
$source = $source.Replace('SpaceEditorStage6GameTest', 'SpaceEditorStage6BaselineGameTest')
$source = $source.Replace('i<(debug?40:18)', 'i<160')
$source = $source.Replace('long[] times=new long[10];for(int i=0;i<times.length;i++){long t=System.nanoTime();peak=Math.max(peak,measured());times[i]=System.nanoTime()-t;}', 'long[] times=new long[20];int steady=0;for(int i=0;i<times.length;i++){long t=System.nanoTime();int used=measured();steady=Math.max(steady,used);peak=Math.max(peak,used);times[i]=System.nanoTime()-t;}')
$source = $source.Replace('median_ms=%.3f p90_ms=%.3f samples=10', 'steady_max_commands=%d median_ms=%.3f p90_ms=%.3f samples=20')
$source = $source.Replace('peak,times[5]/1e6,times[9]/1e6', 'peak,steady,times[10]/1e6,times[18]/1e6')
$source = $source.Replace('build/test-server/stage6-runtime-report.xml', 'build/test-server/stage6-baseline-report.xml')
$source | Set-Content "$root/SpaceEditorStage6BaselineGameTest.java" -Encoding utf8NoBOM
& "$JavaHome/bin/javac.exe" -encoding UTF-8 -cp $classPath -d $root "$root/SpaceEditorStage6BaselineGameTest.java"
if ($LASTEXITCODE -ne 0) { throw 'Baseline harness compilation failed' }
& "$JavaHome/bin/java.exe" -Xmx2G -cp "$classPath;$root" SpaceEditorStage6BaselineGameTest "$root/run" $packRoot > build/test-server/stage6-baseline-warm.log 2>&1
if ($LASTEXITCODE -ne 0) { throw 'Baseline GameTest failed' }
Get-Content build/test-server/stage6-baseline-warm.log | Select-String 'SPACE_EDITOR_STAGE6_PERF|required tests passed'
Write-Output "Baseline ref: $BaselineRef; artifacts: $root"
