#!/usr/bin/env bash
#
# Post Review Summary to Discord
#
# Posts the nightly review summary to a Discord channel for human review.
# Defaults to YESTERDAY when run without arguments.
#
# Requires OpenClaw CLI with configured Discord delivery.
#
# Usage:
#   ./post-improvements-summary.sh              # post yesterday's summary
#   ./post-improvements-summary.sh 2026-04-01   # post specific date
#
set -euo pipefail

# Edit these to match your setup
WORKSPACE="/Users/mirabot/.openclaw/workspace"
CHANNEL_ID="1489250456567025744"  # Discord #improvements channel

# Default to yesterday
DEFAULT_DATE="$(date -v-1d +%F 2>/dev/null || python3 -c 'from datetime import datetime, timedelta; print((datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))')"
DATE_ARG="${1:-$DEFAULT_DATE}"
SUMMARY_FILE="$WORKSPACE/memory/candidates/${DATE_ARG}-review-summary.md"

if [[ ! -f "$SUMMARY_FILE" ]]; then
  echo "Summary file not found: $SUMMARY_FILE" >&2
  exit 1
fi

TMP_MESSAGE="$(mktemp)"
{
  echo "**Nightly memory-improvement review summary for ${DATE_ARG}**"
  echo
  echo "Review the candidate items below. Approve, dismiss, or mark for merge/update."
  echo "If an approved item needs implementation, it can be handed to Patchbay via the coordination bus."
  echo
  # Truncate to avoid Discord message limits
  sed -n '1,220p' "$SUMMARY_FILE"
} > "$TMP_MESSAGE"

# Post via OpenClaw agent delivery
openclaw agent \
  --agent main \
  --message "Post the following review summary to the Discord improvements channel:" \
  --deliver \
  --reply-channel discord \
  --reply-account default \
  --reply-to "$CHANNEL_ID"

rm -f "$TMP_MESSAGE"
echo "Posted review summary for $DATE_ARG to Discord channel $CHANNEL_ID"
