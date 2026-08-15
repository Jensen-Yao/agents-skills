param(
  [Parameter(Position = 0)]
  [ValidateSet("generate", "edit", "generate-batch")]
  [string]$Command = "",
  [string]$Model = "gpt-image-2",
  [string]$Prompt = "",
  [string]$PromptFile = "",
  [int]$N = 0,
  [string]$Size = "",
  [string]$Quality = "",
  [string]$Background = "",
  [string]$OutputFormat = "",
  [int]$OutputCompression = -1,
  [string]$Moderation = "",
  [string]$OutputPath = "",
  [string]$OutputDir = "",
  [switch]$Force,
  [switch]$DryRun,
  [switch]$Augment,
  [switch]$NoAugment,
  [string]$UseCase = "",
  [string]$Scene = "",
  [string]$Subject = "",
  [string]$Style = "",
  [string]$Composition = "",
  [string]$Lighting = "",
  [string]$Palette = "",
  [string]$Materials = "",
  [string]$Text = "",
  [string]$Constraints = "",
  [string]$Negative = "",
  [int]$DownscaleMaxDim = 0,
  [string]$DownscaleSuffix = "",
  [string[]]$Image = @(),
  [string]$Mask = "",
  [string]$InputFidelity = "",
  [Alias("Input")]
  [string]$BatchInput = "",
  [int]$Concurrency = 0,
  [int]$MaxAttempts = 0,
  [switch]$FailFast,
  [string[]]$ExtraArgs = @(),
  [switch]$PrintArgs,
  [switch]$ShowConfig
)

$ErrorActionPreference = "Stop"

function Read-JsonObject([string]$Path) {
  if (Test-Path -LiteralPath $Path) {
    try {
      return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    } catch {
      Write-Warning "Existing JSON could not be parsed: $Path"
    }
  }
  return $null
}

function Get-PropertyValue($Object, [string]$Name, $Default = $null) {
  if ($Object -and ($Object.PSObject.Properties.Name -contains $Name)) {
    return $Object.$Name
  }
  return $Default
}

function Get-EnvSnapshot([string[]]$Names) {
  $snapshot = @{}
  foreach ($name in ($Names | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique)) {
    $item = Get-Item -LiteralPath "Env:$name" -ErrorAction SilentlyContinue
    $snapshot[$name] = if ($item) { [string]$item.Value } else { $null }
  }
  return $snapshot
}

function Restore-EnvSnapshot($Snapshot) {
  foreach ($name in $Snapshot.Keys) {
    if ($null -eq $Snapshot[$name]) {
      Remove-Item -LiteralPath "Env:$name" -ErrorAction SilentlyContinue
    } else {
      Set-Item -LiteralPath "Env:$name" -Value $Snapshot[$name]
    }
  }
}

function Add-Arg([System.Collections.Generic.List[string]]$ArgList, [string]$Name, [object]$Value) {
  if ($null -eq $Value) { return }
  if ($Value -is [string] -and [string]::IsNullOrWhiteSpace($Value)) { return }
  if ($Value -is [int] -and $Value -le 0) { return }
  $ArgList.Add($Name)
  $ArgList.Add([string]$Value)
}

function Add-SwitchArg([System.Collections.Generic.List[string]]$ArgList, [string]$Name, [bool]$Value) {
  if ($Value) { $ArgList.Add($Name) }
}

function Build-ImageGenArgs {
  $imageArgsList = [System.Collections.Generic.List[string]]::new()
  Add-Arg $imageArgsList "--model" $Model
  Add-Arg $imageArgsList "--prompt" $Prompt
  Add-Arg $imageArgsList "--prompt-file" $PromptFile
  Add-Arg $imageArgsList "--n" $N
  Add-Arg $imageArgsList "--size" $Size
  Add-Arg $imageArgsList "--quality" $Quality
  Add-Arg $imageArgsList "--background" $Background
  Add-Arg $imageArgsList "--output-format" $OutputFormat
  Add-Arg $imageArgsList "--output-compression" $OutputCompression
  Add-Arg $imageArgsList "--moderation" $Moderation
  Add-Arg $imageArgsList "--out" $OutputPath
  Add-Arg $imageArgsList "--out-dir" $OutputDir
  Add-SwitchArg $imageArgsList "--force" $Force
  Add-SwitchArg $imageArgsList "--dry-run" $DryRun
  Add-SwitchArg $imageArgsList "--augment" $Augment
  Add-SwitchArg $imageArgsList "--no-augment" $NoAugment
  Add-Arg $imageArgsList "--use-case" $UseCase
  Add-Arg $imageArgsList "--scene" $Scene
  Add-Arg $imageArgsList "--subject" $Subject
  Add-Arg $imageArgsList "--style" $Style
  Add-Arg $imageArgsList "--composition" $Composition
  Add-Arg $imageArgsList "--lighting" $Lighting
  Add-Arg $imageArgsList "--palette" $Palette
  Add-Arg $imageArgsList "--materials" $Materials
  Add-Arg $imageArgsList "--text" $Text
  Add-Arg $imageArgsList "--constraints" $Constraints
  Add-Arg $imageArgsList "--negative" $Negative
  Add-Arg $imageArgsList "--downscale-max-dim" $DownscaleMaxDim
  Add-Arg $imageArgsList "--downscale-suffix" $DownscaleSuffix

  foreach ($imagePath in $Image) {
    Add-Arg $imageArgsList "--image" $imagePath
  }
  Add-Arg $imageArgsList "--mask" $Mask
  Add-Arg $imageArgsList "--input-fidelity" $InputFidelity
  Add-Arg $imageArgsList "--input" $BatchInput
  Add-Arg $imageArgsList "--concurrency" $Concurrency
  Add-Arg $imageArgsList "--max-attempts" $MaxAttempts
  Add-SwitchArg $imageArgsList "--fail-fast" $FailFast

  foreach ($arg in $ExtraArgs) {
    if (-not [string]::IsNullOrWhiteSpace($arg)) {
      $imageArgsList.Add($arg)
    }
  }

  return $imageArgsList.ToArray()
}

$settingsPath = Join-Path $env:APPDATA "Codex++\settings.json"
$secretPath = Join-Path $env:USERPROFILE ".codex\secrets\imagegen-openai-key.txt"
$imageGenCli = Join-Path $env:USERPROFILE ".codex\skills\.system\imagegen\scripts\image_gen.py"
$settings = Read-JsonObject $settingsPath

$enabled = [bool](Get-PropertyValue $settings "cliWrapperEnabled" $false)
$settingsKey = [string](Get-PropertyValue $settings "cliWrapperApiKey" "")
$secretKey = if (Test-Path -LiteralPath $secretPath) { (Get-Content -LiteralPath $secretPath -Raw).Trim() } else { "" }
$apiKey = if ($enabled -and -not [string]::IsNullOrWhiteSpace($settingsKey)) { $settingsKey.Trim() } else { $secretKey }
$baseUrl = if ($enabled -and -not [string]::IsNullOrWhiteSpace([string](Get-PropertyValue $settings "cliWrapperBaseUrl" ""))) {
  [string](Get-PropertyValue $settings "cliWrapperBaseUrl" "")
} else {
  "https://code.codingplay.top/v1"
}
$envName = if ($enabled -and -not [string]::IsNullOrWhiteSpace([string](Get-PropertyValue $settings "cliWrapperApiKeyEnv" ""))) {
  [string](Get-PropertyValue $settings "cliWrapperApiKeyEnv" "")
} else {
  "OPENAI_API_KEY"
}

if ($ShowConfig) {
  [pscustomobject]@{
    cliWrapperEnabled = $enabled
    cliWrapperBaseUrl = $baseUrl
    cliWrapperApiKeyEnv = $envName
    settingsHasApiKey = -not [string]::IsNullOrWhiteSpace($settingsKey)
    secretFileExists = Test-Path -LiteralPath $secretPath
    effectiveHasApiKey = -not [string]::IsNullOrWhiteSpace($apiKey)
    imageGenCliExists = Test-Path -LiteralPath $imageGenCli
    settingsPath = $settingsPath
    secretPath = $secretPath
    imageGenCli = $imageGenCli
  } | ConvertTo-Json -Depth 5
  exit 0
}

if ([string]::IsNullOrWhiteSpace($Command)) {
  throw "Command is required. Use generate, edit, or generate-batch."
}

if ([string]::IsNullOrWhiteSpace($apiKey)) {
  throw "ImageGen API key is missing. Configure Codex++ settings or create: $secretPath"
}

if (-not (Test-Path -LiteralPath $imageGenCli)) {
  throw "Cannot find image_gen.py: $imageGenCli"
}

$envNames = @($envName, "OPENAI_API_KEY", "OPENAI_BASE_URL")
$snapshot = Get-EnvSnapshot $envNames

try {
  Set-Item -LiteralPath "Env:$envName" -Value $apiKey
  $env:OPENAI_API_KEY = $apiKey
  $env:OPENAI_BASE_URL = $baseUrl.Trim()

  $imageGenArgs = Build-ImageGenArgs
  if ($PrintArgs) {
    [pscustomobject]@{
      command = $Command
      pythonArgs = @($imageGenArgs)
      envName = $envName
      hasApiKey = -not [string]::IsNullOrWhiteSpace($apiKey)
      baseUrl = $env:OPENAI_BASE_URL
    } | ConvertTo-Json -Depth 10
  }
  & python $imageGenCli $Command @imageGenArgs
  $exitCode = if ($LASTEXITCODE -is [int]) { $LASTEXITCODE } else { 0 }
} finally {
  Restore-EnvSnapshot $snapshot
}

exit $exitCode
