#!/usr/bin/env bash
# Bloque le commit si un token ressemble à une clé Meraki, un token ThousandEyes ou un token Webex.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

patterns=(
  '[0-9a-f]{40}'                                                    # clé API Meraki
  '[0-9a-f]{4}-[0-9a-f]{2}-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'  # token ThousandEyes
  '[A-Za-z0-9]{64}_[A-Za-z0-9]{4}_[0-9a-f-]{36}'                    # token Webex
)

found=0
for p in "${patterns[@]}"; do
  if git grep -nIE "$p" -- . ':!scripts/check-secrets.sh'; then found=1; fi
done

if [ "$found" -eq 1 ]; then
  echo "❌ Secret détecté. Remplacez-le par un placeholder <...> avant de commiter."
  exit 1
fi
echo "✅ Aucun secret détecté."
