#!/usr/bin/env bash
# Bug bounty recon script — AUTHORIZED TARGETS ONLY.
# Usage: bash recon.sh <domain> [outdir]
# Missing tools are skipped automatically (check output warnings).
set -uo pipefail

TARGET="${1:?Usage: bash recon.sh example.com [outdir]}"
OUT="${2:-recon-$TARGET}"
mkdir -p "$OUT"

have() { command -v "$1" >/dev/null 2>&1; }
step() { echo "[*] $1"; }
warn() { echo "[!] missing tool: $1 (skipped)"; }

: > "$OUT/subs.txt"
: > "$OUT/urls.txt"

# 1. Subdomain enumeration (passive)
if have subfinder; then
  step "subfinder: $TARGET"
  subfinder -d "$TARGET" -all -silent >> "$OUT/subs.txt"
else
  warn subfinder
fi

# 2. crt.sh certificate transparency fallback (may be slow)
step "crt.sh: $TARGET"
curl -s --max-time 90 "https://crt.sh/?q=%25.$TARGET&output=json" \
  | grep -oE '"name_value":"[^"]+"' | sed 's/"name_value":"//;s/"$//' \
  | sort -u | sed 's/^\*\.//' >> "$OUT/subs.txt" || true

sort -u "$OUT/subs.txt" -o "$OUT/subs.txt"

# 3. Historical URLs from public archives
if have gau; then
  step "gau: $TARGET"
  gau --subs "$TARGET" >> "$OUT/urls.txt" || true
else
  warn gau
fi

# 4. Alive hosts + status code + title + tech fingerprint
if have httpx && [ -s "$OUT/subs.txt" ]; then
  step "httpx probe"
  httpx -l "$OUT/subs.txt" -sc -title -tech-detect -rate-limit 100 -o "$OUT/alive.txt" || true
else
  warn httpx
fi

# 5. Port scan (top 100, TCP connect — no admin required)
if have nmap; then
  step "nmap top-100 ports (rate-limited)"
  nmap -sT --top-ports 100 -Pn -T3 --max-rate 300 "$TARGET" -oN "$OUT/ports.txt" || true
else
  warn nmap
fi

# 6. Nuclei templates (medium and above) on alive hosts
if have nuclei && [ -s "$OUT/alive.txt" ]; then
  step "nuclei scan"
  nuclei -l "$OUT/alive.txt" -severity medium,high,critical -rl 50 -c 25 -o "$OUT/nuclei.txt" || true
else
  warn nuclei
fi

# 7. Summary
step "summary:"
echo "  subdomains : $(wc -l < "$OUT/subs.txt")"
[ -s "$OUT/urls.txt" ]   && echo "  urls       : $(wc -l < "$OUT/urls.txt")"
[ -s "$OUT/alive.txt" ]  && echo "  alive      : $(wc -l < "$OUT/alive.txt")"
[ -s "$OUT/nuclei.txt" ] && echo "  nuclei hits: $(wc -l < "$OUT/nuclei.txt")"
echo "[+] done -> $OUT"
