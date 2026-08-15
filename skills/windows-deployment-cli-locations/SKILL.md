---
name: windows-deployment-cli-locations
description: Locate and invoke the deployment and database tools installed on this Windows workstation, especially Supabase CLI, Netlify CLI, Neon CLI, Vercel CLI, Cloudflare Wrangler, Railway CLI, PostgreSQL, and Docker checks. Use when a task needs one of these commands, when a command is not on PATH, when checking whether a tool is installed, or before installing another copy.
---

# Windows Deployment CLI Locations

Use the existing installation on this workstation. Verify a launcher before use because versions and PATH entries can change.

## Installed Tools

The following locations were verified on 2026-07-31.

| Tool | Command | Launcher | Package or install directory | Verified version | PATH |
|---|---|---|---|---|---|
| Supabase CLI | `supabase` | `E:\SupabaseCLI\supabase.cmd` | `E:\SupabaseCLI\node_modules\supabase` | `2.110.0` | Not configured |
| Netlify CLI | `netlify` | `E:\NetlifyCLI\netlify.cmd` | `E:\NetlifyCLI\node_modules\netlify-cli` | `27.0.1` | Not configured |
| Neon CLI | `neon` | `E:\NeonCLI\neon.cmd` | `E:\NeonCLI\node_modules\neon` | `2.38.2` | User PATH |
| Vercel CLI | `vercel` | `E:\VercelCLI\vercel.cmd` | `E:\VercelCLI\node_modules\vercel` | `58.1.0` | Not configured |
| Cloudflare Wrangler | `wrangler` | `E:\CloudflareCLI\wrangler.cmd` | `E:\CloudflareCLI\node_modules\wrangler` | `4.115.0` | User PATH |
| Railway CLI | `railway` | `E:\RailwayCLI\railway.cmd` | `E:\RailwayCLI\node_modules\@railway\cli` | `5.30.1` | Not configured |
| PostgreSQL | `psql`, `pg_dump`, `pg_restore`, `pg_isready`, `postgres`, `pg_ctl` | `E:\PostgreSQL\18.4\pgsql\bin` | `E:\PostgreSQL\18.4` | `18.4` | User PATH |

Node.js is installed at `D:\nodejs\node.exe` and is on the machine PATH. The normal npm global package directory is `C:\Users\18052\AppData\Roaming\npm\node_modules`, but the Node-based tools above use their dedicated `E:\*CLI` directories.

## PostgreSQL Layout

Use these verified locations:

- Installation root: `E:\PostgreSQL\18.4`
- Software directory: `E:\PostgreSQL\18.4\pgsql`
- Executables: `E:\PostgreSQL\18.4\pgsql\bin`
- Data directory: `E:\PostgreSQL\18.4\data`
- Server log: `E:\PostgreSQL\18.4\postgres.log`

Prefer an explicit executable path in automation even though the bin directory is on the user PATH:

```powershell
& 'E:\PostgreSQL\18.4\pgsql\bin\psql.exe' --version
& 'E:\PostgreSQL\18.4\pgsql\bin\pg_isready.exe'
```

Do not start, stop, initialize, upgrade, or modify the database cluster unless the user explicitly requests that operation. Preserve the existing `data` directory.

## Docker Status

Docker CLI, Docker Desktop, and a local Docker Engine are not installed. The temporary portable CLI was removed on 2026-07-31, and WSL is not enabled.

- Do not use or reference `E:\DockerCLI\docker.exe`; that file no longer exists.
- Report Docker-dependent local workflows as unavailable. This includes `docker run`, `docker compose`, local image builds, and `supabase start`.
- Do not install a Docker client, WSL, Docker Desktop, or a local engine unless the user explicitly requests it again.
- Installing a local Linux-container engine on this Windows 11 Home system requires administrator access, WSL 2, and normally Docker Desktop.
- If Docker Desktop is requested later, keep the application and WSL data on E drive, verify the engine with `docker info`, and update this skill with the resulting paths.

Confirm the current absence when needed:

```powershell
Get-Command docker -All -ErrorAction SilentlyContinue
Test-Path -LiteralPath 'E:\DockerCLI\docker.exe'
Test-Path -LiteralPath 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
```

## Invocation Workflow

1. Check command resolution first:

   ```powershell
   Get-Command supabase, netlify, neon, vercel, wrangler, docker, railway, psql, pg_dump, pg_restore, pg_isready, postgres, pg_ctl -All -ErrorAction SilentlyContinue
   ```

2. If an installed tool is not on PATH, invoke its launcher explicitly:

   ```powershell
   & 'E:\SupabaseCLI\supabase.cmd' --version
   & 'E:\NetlifyCLI\netlify.cmd' --version
   & 'E:\NeonCLI\neon.cmd' --version
   & 'E:\VercelCLI\vercel.cmd' --version
   & 'E:\CloudflareCLI\wrangler.cmd' --version
   & 'E:\RailwayCLI\railway.cmd' --version
   & 'E:\PostgreSQL\18.4\pgsql\bin\psql.exe' --version
   ```

3. Before a consequential operation, verify the selected launcher:

   ```powershell
   $cli = 'E:\SupabaseCLI\supabase.cmd'
   if (-not (Test-Path -LiteralPath $cli)) { throw "CLI not found: $cli" }
   & $cli --version
   ```

4. Prefer the fixed launcher over `npx`, `npm exec`, or a fresh global install. Those alternatives may download a different version.
5. Do not permanently edit PATH unless the user requests it. For a temporary session, prepend only the required directory to `$env:Path`.
6. Use `neon`, not `neonctl`, for the installed Neon CLI.

## Recheck PATH

The process environment can be older than the registry-backed user or machine PATH. Compare all three before concluding that a launcher is unavailable:

```powershell
$env:Path -split ';'
[Environment]::GetEnvironmentVariable('Path', 'User') -split ';'
[Environment]::GetEnvironmentVariable('Path', 'Machine') -split ';'
```
