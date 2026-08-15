---
name: libreoffice-local-install
description: Use the existing local LibreOffice installation for CLI document conversion, PDF export, rendering, printing, and Office-format automation on this Windows machine. Trigger when a task mentions LibreOffice, soffice, headless document conversion, DOCX/XLSX/PPTX/ODF conversion, or needs the local LibreOffice executable path. Do not download or reinstall LibreOffice while the recorded executable works.
---

# Local LibreOffice Installation

Use the existing installation instead of searching for, downloading, or installing another copy.

## Fixed Paths

- Installation root: `F:\LibreOffice`
- CLI executable: `F:\LibreOffice\program\soffice.com`
- GUI executable: `F:\LibreOffice\program\soffice.exe`
- Bundled Python: `F:\LibreOffice\program\python.exe`
- Extension manager CLI: `F:\LibreOffice\program\unopkg.com`
- User PATH entry: `F:\LibreOffice\program`
- User `TEMP` and `TMP`: `C:\Users\18052\AppData\Local\Temp`
- Codex renderer launchers: `C:\Users\18052\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\override\soffice.exe` and `libreoffice.exe`

Prefer `soffice.com` for direct command-line work because it preserves console output and exit behavior on Windows. The user PATH and Codex runtime shims allow renderers to resolve both `soffice` and `libreoffice`; use the fixed path as a fallback if command resolution is uncertain.

## Verify

Run this before a workflow only when availability is uncertain:

```powershell
$soffice = 'F:\LibreOffice\program\soffice.com'
if (-not (Test-Path -LiteralPath $soffice)) {
    throw "LibreOffice CLI is missing at $soffice"
}
& $soffice --version
```

The recorded installation version is `26.2.4.2`. Treat the executable output as authoritative if the installed version changes.

## Convert Headlessly

Use absolute input and output paths, create the output directory first, and verify the expected output file after conversion:

```powershell
$soffice = 'F:\LibreOffice\program\soffice.com'
$inputFile = 'C:\absolute\path\document.docx'
$outputDir = 'C:\absolute\path\output'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

& $soffice --headless --convert-to pdf --outdir $outputDir $inputFile
if ($LASTEXITCODE -ne 0) {
    throw "LibreOffice conversion failed with exit code $LASTEXITCODE"
}
```

Use an explicit export filter when output fidelity depends on the source application, for example `pdf:writer_pdf_Export`, `pdf:calc_pdf_Export`, or `pdf:impress_pdf_Export`.

## Operational Rules

1. Use the fixed CLI path directly.
2. Keep `--headless` for automation that must not open a window.
3. Check both the process exit code and the output artifact; LibreOffice can report some conversion problems only in console text.
4. Avoid parallel commands sharing the default LibreOffice user profile. Run conversions sequentially unless a task explicitly configures isolated `UserInstallation` profiles.
5. Download or reinstall LibreOffice only if the fixed executable is missing or unusable, and report that condition first.
6. Keep LibreOffice profiles out of `C:\WINDOWS\TEMP`. The Codex renderer launcher maps legacy `UserInstallation` paths from that directory into the user's local Temp directory and removes the mapped profile after conversion.
