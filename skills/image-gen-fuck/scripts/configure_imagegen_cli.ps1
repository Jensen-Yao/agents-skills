param(
  [string]$ApiKey = "",
  [string]$BaseUrl = "https://code.codingplay.top/v1",
  [string]$ApiKeyEnv = "OPENAI_API_KEY",
  [switch]$Disable,
  [switch]$Show
)

$ErrorActionPreference = "Stop"

function Ensure-Directory([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
  }
}

function Read-JsonObject([string]$Path) {
  if (Test-Path -LiteralPath $Path) {
    try {
      return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    } catch {
      Write-Warning "Existing JSON could not be parsed; creating a fresh object: $Path"
    }
  }
  return [pscustomobject]@{}
}

function Set-Property($Object, [string]$Name, $Value) {
  if ($Object.PSObject.Properties.Name -contains $Name) {
    $Object.$Name = $Value
  } else {
    $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value
  }
}

$codexPlusDir = Join-Path $env:APPDATA "Codex++"
$settingsPath = Join-Path $codexPlusDir "settings.json"
$secretDir = Join-Path $env:USERPROFILE ".codex\secrets"
$secretPath = Join-Path $secretDir "imagegen-openai-key.txt"

Ensure-Directory $codexPlusDir
Ensure-Directory $secretDir

$settings = Read-JsonObject $settingsPath

if ($Show) {
  $enabled = if ($settings.PSObject.Properties.Name -contains "cliWrapperEnabled") { [bool]$settings.cliWrapperEnabled } else { $false }
  $configuredBaseUrl = if ($settings.PSObject.Properties.Name -contains "cliWrapperBaseUrl") { [string]$settings.cliWrapperBaseUrl } else { "" }
  $configuredEnv = if ($settings.PSObject.Properties.Name -contains "cliWrapperApiKeyEnv") { [string]$settings.cliWrapperApiKeyEnv } else { "" }
  $hasSettingsKey = ($settings.PSObject.Properties.Name -contains "cliWrapperApiKey") -and -not [string]::IsNullOrWhiteSpace([string]$settings.cliWrapperApiKey)
  $hasSecretFile = Test-Path -LiteralPath $secretPath
  [pscustomobject]@{
    cliWrapperEnabled = $enabled
    cliWrapperBaseUrl = $configuredBaseUrl
    cliWrapperApiKeyEnv = $configuredEnv
    settingsHasApiKey = $hasSettingsKey
    secretFileExists = $hasSecretFile
    settingsPath = $settingsPath
    secretPath = $secretPath
  } | ConvertTo-Json -Depth 5
  exit 0
}

if ($Disable) {
  Set-Property $settings "cliWrapperEnabled" $false
  Set-Property $settings "cliWrapperBaseUrl" ""
  Set-Property $settings "cliWrapperApiKeyEnv" "OPENAI_API_KEY"
  $settings | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $settingsPath -Encoding UTF8
  Write-Host "ImageGen CLI wrapper disabled in Codex++ settings."
  exit 0
}

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
  $secure = Read-Host "ImageGen API key" -AsSecureString
  $plainPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
  try {
    $ApiKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($plainPtr)
  } finally {
    if ($plainPtr -ne [IntPtr]::Zero) {
      [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($plainPtr)
    }
  }
}

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
  throw "API key is required."
}

if ([string]::IsNullOrWhiteSpace($BaseUrl)) {
  $BaseUrl = "https://code.codingplay.top/v1"
}

if ([string]::IsNullOrWhiteSpace($ApiKeyEnv)) {
  $ApiKeyEnv = "OPENAI_API_KEY"
}

$ApiKey.Trim() | Set-Content -LiteralPath $secretPath -NoNewline -Encoding UTF8

Set-Property $settings "cliWrapperEnabled" $true
Set-Property $settings "cliWrapperBaseUrl" $BaseUrl.Trim()
Set-Property $settings "cliWrapperApiKey" $ApiKey.Trim()
Set-Property $settings "cliWrapperApiKeyEnv" $ApiKeyEnv.Trim()
$settings | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $settingsPath -Encoding UTF8

Write-Host "ImageGen CLI wrapper configured."
Write-Host "Settings: $settingsPath"
Write-Host "Secret:   $secretPath"
Write-Host "Base URL: $($BaseUrl.Trim())"
