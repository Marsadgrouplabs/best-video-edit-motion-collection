# Installs Best Video Edit & Motion Collection for Claude Code and/or Codex on this computer.
# Usage: powershell -ExecutionPolicy Bypass -File .\install.ps1 [-Target claude|codex|both] [-Components all|recommended|id1,id2,...]
# Without -Components it shows the parts and asks. Parts already installed are kept. The list is in COMPONENTS.md.
param(
    [ValidateSet('claude', 'codex', 'both')][string]$Target = 'both',
    [string]$Components = '',
    [string]$HomeDir = $HOME
)
$ErrorActionPreference = 'Stop'
$Name = 'best-video-edit-motion-collection'
$Source = Join-Path $PSScriptRoot "skills\$Name"
if (-not (Test-Path (Join-Path $Source 'SKILL.md'))) { throw "Skill files not found in $Source" }
$Manifest = Get-Content (Join-Path $Source 'components.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$AllIds = @($Manifest.components | ForEach-Object { $_.id })
$Recommended = @($Manifest.components | Where-Object { $_.recommended } | ForEach-Object { $_.id })

if (-not $Components) {
    Write-Host "Parts you can install (details in COMPONENTS.md):"
    foreach ($c in $Manifest.components) {
        $mark = if ($c.recommended) { '*' } else { ' ' }
        $warn = if ($c.warning) { "  !! $($c.warning)" } else { '' }
        Write-Host ((" {0} {1,-18} {2,-12} {3}" -f $mark, $c.id, $c.group, $c.size) + $warn)
    }
    Write-Host "(* = recommended)"
    try { $Components = Read-Host "Type all, recommended, or part IDs separated by commas [recommended]" } catch { $Components = '' }
    if (-not $Components) { $Components = 'recommended' }
}
switch ($Components.Trim().ToLower()) {
    'all' { $Chosen = $AllIds }
    'recommended' { $Chosen = $Recommended }
    default {
        $Chosen = @($Components.Split(',') | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        $Unknown = @($Chosen | Where-Object { $AllIds -notcontains $_ })
        if ($Unknown.Count) { throw "Unknown part(s): $($Unknown -join ', '). Known: $($AllIds -join ', ')" }
    }
}

$Roots = @()
if ($Target -in 'claude', 'both') { $Roots += (Join-Path $HomeDir '.claude\skills') }
if ($Target -in 'codex', 'both') { $Roots += (Join-Path $HomeDir '.agents\skills') }

function Copy-Part([string]$Rel, [string]$Dest) {
    $From = Join-Path $Source $Rel
    if (-not (Test-Path $From)) { return }
    $To = Join-Path $Dest $Rel
    New-Item -ItemType Directory -Force -Path (Split-Path $To -Parent) | Out-Null
    Copy-Item -LiteralPath $From -Destination $To -Recurse -Force
}

foreach ($Root in $Roots) {
    New-Item -ItemType Directory -Force -Path $Root | Out-Null
    $Dest = Join-Path $Root $Name
    $Ids = @($Chosen)
    if (Test-Path $Dest) {
        foreach ($c in $Manifest.components) {
            if ($Ids -notcontains $c.id -and (Test-Path (Join-Path $Dest $c.paths[0]))) { $Ids += $c.id }
        }
        $Backup = Join-Path $Root (".$Name.backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
        Move-Item -LiteralPath $Dest -Destination $Backup
        Write-Host "Previous version kept at: $Backup"
    }
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    foreach ($Rel in $Manifest.core) { Copy-Part $Rel $Dest }
    foreach ($c in $Manifest.components) {
        if ($Ids -contains $c.id) { foreach ($Rel in $c.paths) { Copy-Part $Rel $Dest } }
    }
    Write-Host "Installed: $Dest"
    Write-Host "Parts: core, $($Ids -join ', ')"
}
Write-Host 'Done. Start a new session to use the skill. Run this again with other part IDs to add parts later.'
