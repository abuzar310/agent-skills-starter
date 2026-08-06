param(
  [Parameter(Mandatory = $true)]
  [string]$Destination,

  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$Skills
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Src = Join-Path $Root "skills"

if (-not (Test-Path $Src)) {
  throw "skills/ folder not found at $Src"
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

if (-not $Skills -or $Skills.Count -eq 0) {
  Write-Host "Installing all skills -> $Destination"
  Copy-Item (Join-Path $Src "*") $Destination -Recurse -Force
} else {
  foreach ($name in $Skills) {
    $from = Join-Path $Src $name
    if (-not (Test-Path $from)) {
      Write-Host "Skip (not found): $name"
      continue
    }
    Write-Host "Install $name"
    $to = Join-Path $Destination $name
    if (Test-Path $to) { Remove-Item $to -Recurse -Force }
    Copy-Item $from $to -Recurse -Force
  }
}

Write-Host "Done."
