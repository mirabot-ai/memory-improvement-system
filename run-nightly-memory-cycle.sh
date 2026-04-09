#!/usr/bin/env bash
#
# Nightly Memory Cycle Wrapper
#
# Runs the mining and review summary generation for a given date.
# Defaults to YESTERDAY when run without arguments, which is the
# intended behavior for 3 AM cron jobs.
#
# Usage:
#   ./run-nightly-memory-cycle.sh              # process yesterday
#   ./run-nightly-memory-cycle.sh 2026-04-01   # process specific date
#
set -euo pipefail

# Edit this to match your workspace location
WORKSPACE="/Users/mirabot/.openclaw/workspace"

# Default to yesterday (cross-platform)
DEFAULT_DATE="$(date -v-1d +%F 2>/dev/null || python3 -c 'from datetime import datetime, timedelta; print((datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))')"
DATE_ARG="${1:-$DEFAULT_DATE}"

echo "Running nightly memory cycle for $DATE_ARG"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 "$SCRIPT_DIR/nightly-memory-mine.py" --date "$DATE_ARG"
python3 "$SCRIPT_DIR/nightly-memory-review-summary.py" --date "$DATE_ARG"

echo "Nightly memory cycle complete for $DATE_ARG"
echo "Generated:"
echo "  - $WORKSPACE/memory/candidates/${DATE_ARG}-memory-candidates.md"
echo "  - $WORKSPACE/memory/skills/candidates/${DATE_ARG}-skill-candidates.md"
echo "  - $WORKSPACE/memory/candidates/${DATE_ARG}-review-summary.md"
