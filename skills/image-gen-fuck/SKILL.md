---
name: image-gen-fuck
description: Auxiliary workflow for $imagegen when Codex needs high-quality image generation but the built-in image_gen tool is unavailable or not exposed. Use this with $imagegen to run the installed image_gen.py CLI through a separate temporary drawing API key, preferably configured in Codex++ cliWrapper settings, defaulting to OPENAI_BASE_URL=https://code.codingplay.top/v1, without changing the Codex desktop/chat model API configuration.
---

# Image Gen Fuck

## Purpose

Use this as an operational add-on to `$imagegen`, not as a replacement for it. It preserves normal Codex chat/model behavior while routing image-only CLI calls through a separate configured drawing API.

## Rules

- Still load and follow `$imagegen` first for prompt shaping, transparent-image rules, output handling, and fallback boundaries.
- Use this skill only when the built-in `image_gen` tool is unavailable or not exposed and the user has agreed to the CLI fallback.
- In CLI fallback, prefer `scripts/invoke_imagegen_cli.ps1` instead of calling `$imagegen`'s `image_gen.py` directly. The wrapper reads Codex++ settings or the fallback key file, sets temporary environment variables, runs the Python CLI, and restores the previous environment.
- Do not reject CLI fallback only because the current shell does not already have `OPENAI_API_KEY`; first run `scripts/invoke_imagegen_cli.ps1 -ShowConfig` and check `effectiveHasApiKey`.
- Do not set persistent user or system environment variables for the drawing API key.
- Do not ask the user to paste secrets in chat.
- Do not modify `$imagegen`'s bundled `image_gen.py`.
- Clear temporary environment variables after every CLI command, even on failure.

## Secret Location

Prefer Codex++ settings when available:

```text
%APPDATA%\Codex++\settings.json
```

Read these fields:

```json
{
  "cliWrapperEnabled": true,
  "cliWrapperBaseUrl": "https://code.codingplay.top/v1",
  "cliWrapperApiKey": "<drawing api key>",
  "cliWrapperApiKeyEnv": "OPENAI_API_KEY"
}
```

If Codex++ settings are absent, disabled, or missing a key, fall back to the local key file:

```text
%USERPROFILE%\.codex\secrets\imagegen-openai-key.txt
```

If it does not exist, guide the user to create it:

```powershell
New-Item -ItemType Directory "$env:USERPROFILE\.codex\secrets" -Force
notepad "$env:USERPROFILE\.codex\secrets\imagegen-openai-key.txt"
Test-Path "$env:USERPROFILE\.codex\secrets\imagegen-openai-key.txt"
```

The file should contain only the drawing API key.

To configure both Codex++ settings and the fallback key file, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\image-gen-fuck\scripts\configure_imagegen_cli.ps1"
```

To inspect current configuration without printing the key:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\image-gen-fuck\scripts\invoke_imagegen_cli.ps1" -ShowConfig
```

## Default Endpoint

Default to:

```text
https://code.codingplay.top/v1
```

Use `OPENAI_BASE_URL`, not a CLI argument, because the installed `$imagegen` CLI currently constructs `OpenAI()` / `AsyncOpenAI()` and does not expose `--base-url`.

If the request fails with a path or method error such as `404`, `405`, or an HTML nginx response, ask the user for the correct OpenAI-compatible image base URL. Mention that this CLI needs an endpoint compatible with `/v1/images/generations` and `/v1/images/edits`.

## Command Pattern

Run image CLI calls through the wrapper:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\image-gen-fuck\scripts\invoke_imagegen_cli.ps1" generate `
  -PromptFile '<prompt-file>' `
  -Model 'gpt-image-2' `
  -Size '1024x1024' `
  -Quality 'medium' `
  -OutputPath '<output.png>' `
  -Force
```

For reference-grounded image generation, use the CLI `edit` subcommand and pass repeated `--image` arguments:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\image-gen-fuck\scripts\invoke_imagegen_cli.ps1" edit `
  -PromptFile '<prompt-file>' `
  -Image '<reference-or-layout-1.png>','<reference-or-layout-2.png>' `
  -Model 'gpt-image-2' `
  -Size '1536x1024' `
  -Quality 'medium' `
  -OutputPath '<output.png>' `
  -Force
```

The wrapper sets `OPENAI_API_KEY` and `OPENAI_BASE_URL` only for the Python child process and restores the prior environment in `finally`.
Use PowerShell-native wrapper parameters such as `-OutputPath`, not raw Python CLI flags such as `--out`; raw `--...` flags may be parsed by PowerShell before they reach `image_gen.py`.
When troubleshooting argument passing, add `-PrintArgs`; it prints the Python CLI argument list and only reports key presence as `hasApiKey`, never the API key value.

## Failure Handling

- If the key file is missing, tell the user how to create it and stop.
- If Codex++ is installed, prefer asking the user to open the injected `绘图设置` button or run `scripts/configure_imagegen_cli.ps1`.
- If the API returns authentication errors, ask the user to verify the key file for the drawing API.
- If the API returns `405 Not Allowed` when using `https://code.codingplay.top`, retry once with `https://code.codingplay.top/v1`.
- If `https://code.codingplay.top/v1` also fails with endpoint/path errors, ask for the correct base URL.
- If generation succeeds but the command times out, check whether the output file exists and validates before retrying.
- Always report whether `OPENAI_API_KEY` and `OPENAI_BASE_URL` were cleared after the command.

## Relationship To Codex

This CLI is not Codex CLI. It is the `$imagegen` Python script:

```text
%USERPROFILE%\.codex\skills\.system\imagegen\scripts\image_gen.py
```

Codex runs it through the shell. The drawing key and base URL affect only that shell command and its Python child process when set with the wrapper above; they do not change Codex desktop's normal chat/model API configuration.

## Codex++ UI Helper

This skill may install a Codex++ user script at:

```text
%APPDATA%\Codex++\user_scripts\imagegen-cli-settings.js
```

The script adds a `绘图设置` button to Codex++-launched Codex. It uses Codex++ bridge routes `/settings/get` and `/settings/set` to manage `cliWrapperEnabled`, `cliWrapperBaseUrl`, `cliWrapperApiKey`, and `cliWrapperApiKeyEnv`.

Because browser-injected user scripts should not write arbitrary local files, use the bundled PowerShell helper when a fallback key file also needs to be synchronized.
