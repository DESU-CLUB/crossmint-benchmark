#!/usr/bin/env bash
# Pre-commit hook: scan staged files in jobs/ for leaked secrets.
# Install: cp scripts/check-secrets.sh .git/hooks/pre-commit

set -euo pipefail

PATTERNS=(
  'sk-ant-[a-zA-Z0-9_-]{20,}'       # Anthropic API key
  'sk_staging_[a-zA-Z0-9]{20,}'      # Crossmint API key (staging)
  'sk_production_[a-zA-Z0-9]{20,}'   # Crossmint API key (production)
  'xmsk1_[a-f0-9]{20,}'             # Crossmint signer secret
  'e2b_[a-f0-9]{20,}'               # E2B API key
  'pk_[a-zA-Z0-9]{40,}'             # Pochi API key
  'as-[a-zA-Z0-9]{20,}'             # Modal token secret
)

COMBINED=$(IFS='|'; echo "${PATTERNS[*]}")

# Get staged files (added/modified), filter to jobs/ directory
FILES=$(git diff --cached --name-only --diff-filter=ACM -- 'jobs/' || true)

if [ -z "$FILES" ]; then
  exit 0
fi

FOUND=0
while IFS= read -r file; do
  if grep -qE "$COMBINED" "$file" 2>/dev/null; then
    echo "SECRET DETECTED in: $file"
    grep -nE "$COMBINED" "$file" | head -5 | while IFS= read -r line; do
      echo "  $line" | cut -c1-120
    done
    FOUND=1
  fi
done <<< "$FILES"

if [ "$FOUND" -eq 1 ]; then
  echo ""
  echo "Commit blocked: secrets found in staged files."
  echo "Redact the values above before committing."
  exit 1
fi
