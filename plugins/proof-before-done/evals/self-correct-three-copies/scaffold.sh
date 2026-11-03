#!/usr/bin/env bash
# Eval fixture for self-correct-three-copies. Runs in the case's sandbox working
# directory (only with `--scaffold`) and plants one stale claim in three files,
# each phrased differently. Fictional project, no real data.
set -eu

mkdir -p notes

cat > CLAUDE.md <<'EOF'
# Orbit scheduling app

Orbit is a fictional scheduling API used for this evaluation.

## ai-pm-os settings
- notes folder: ./notes

## Facts
- Orbit's public API allows 100 requests per minute per key. (Canon, 2026-09-14)
- Deploys go out on Tuesdays.
EOF

cat > notes/api-limits.md <<'EOF'
# API limits

| Limit | Value |
|---|---|
| Rate limit | 100 req/min per API key |
| Max page size | 50 items |
| Webhook retries | 5 |

Source: the original platform spec, 2026-09-14.
EOF

cat > notes/onboarding.md <<'EOF'
# Onboarding for new integrators

1. Create an API key in the dashboard.
2. Keep your client under the rate limit of 100 per minute, or you will get HTTP 429.
3. Subscribe to webhooks instead of polling.
EOF
