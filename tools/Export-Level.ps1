param([string]$World = "", [string]$Out = "")
$ErrorActionPreference = 'Stop'
if (-not $World) {
    $shellApp = New-Object -ComObject Shell.Application
    $folder = $shellApp.BrowseForFolder(0, 'Space Editor: 保存して閉じたワールドのフォルダを選択', 0, "$env:APPDATA/.minecraft/saves")
    if (-not $folder) { exit 0 }
    $World = $folder.Self.Path
}
$pythonCandidates = @(
    "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",
    "$env:LOCALAPPDATA/Programs/Python/Python314/python.exe",
    "$env:LOCALAPPDATA/Programs/Python/Python313/python.exe",
    "$env:LOCALAPPDATA/Programs/Python/Python312/python.exe",
    "$env:LOCALAPPDATA/Programs/Python/Python311/python.exe"
)
$pythonExe = $pythonCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $pythonExe) {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand) { $pythonExe = $pythonCommand.Source }
}
if (-not $pythonExe) { throw 'Python 3.10以上が必要です。Codex同梱Pythonも自動検出します。' }
if (-not $Out) {
    $outputDir = Join-Path $PSScriptRoot 'exports'
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    $Out = Join-Path $outputDir ('level-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.json')
}
& $pythonExe (Join-Path $PSScriptRoot 'editor_data.py') export $World --out $Out
if ($LASTEXITCODE -ne 0) { throw '書き出しに失敗しました。ワールドの選択と保存状態を確認してください。' }
Write-Output "完了: $Out"
Write-Output 'このJSONをCodexへ渡してください。元ワールドには書き込んでいません。'
