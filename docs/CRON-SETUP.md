# Cron Setup Guide

How to schedule automatic nightly memory mining.

## Prerequisites

Before automating, manually run the scripts for several days to:
1. Verify candidate quality
2. Tune heuristics if needed
3. Establish a review habit

## Previous-day timing

The nightly cycle processes **yesterday's** data, not today's. At 3 AM, "today" has barely started, so we review the previous day's complete record.

The wrapper scripts (`run-nightly-memory-cycle.sh`, `post-improvements-summary.sh`) default to yesterday when run without arguments.

## Example cron entries

```cron
# 3:00 AM - generate candidates and review summary for yesterday
0 3 * * * /path/to/run-nightly-memory-cycle.sh >> /path/to/logs/memory-cycle.log 2>&1

# 3:05 AM - post review summary to Discord improvements channel
5 3 * * * /path/to/post-improvements-summary.sh >> /path/to/logs/improvements-post.log 2>&1
```

Or run the scripts directly:

```cron
0 3 * * * cd /path/to/workspace && python3 /path/to/nightly-memory-mine.py >> /path/to/logs/memory-mine.log 2>&1
5 3 * * * cd /path/to/workspace && python3 /path/to/nightly-memory-review-summary.py >> /path/to/logs/memory-mine.log 2>&1
```

## Systemd timer alternative

For systems using systemd, create a timer unit:

**`/etc/systemd/system/memory-mine.timer`**
```ini
[Unit]
Description=Nightly memory mining

[Timer]
OnCalendar=*-*-* 02:15:00
Persistent=true

[Install]
WantedBy=timers.target
```

**`/etc/systemd/system/memory-mine.service`**
```ini
[Unit]
Description=Run memory mining script

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/nightly-memory-mine.py
WorkingDirectory=/path/to/workspace
User=youruser
```

Enable:
```bash
sudo systemctl enable memory-mine.timer
sudo systemctl start memory-mine.timer
```

## OpenClaw cron integration

If using OpenClaw, you can schedule via the native cron tool:

```
Schedule: kind=cron, expr="0 3 * * *", tz="America/New_York"
Payload: kind=agentTurn, message="Run nightly memory mining for yesterday and generate review summary"
SessionTarget: isolated
```

For recurring Discord posts, prefer native OpenClaw cron delivery over shell wrappers when possible. Native cron provides:
- Cleaner channel delivery
- Explicit session targeting
- Better run logs and delivery status

## Discord review loop

The recommended operational workflow:

1. **3:00 AM** — cron runs `run-nightly-memory-cycle.sh` (generates candidates for yesterday)
2. **3:05 AM** — cron runs `post-improvements-summary.sh` (posts to Discord `#improvements`)
3. **Morning** — humans review candidates in the Discord channel
4. **Approval** — approved items are manually promoted to memory, or handed to an agent via coordination bus

This keeps the review visible and collaborative. Configure the Discord channel ID in `post-improvements-summary.sh`.

## Notification options

After mining completes, you can notify via:
- Discord channel post (via `post-improvements-summary.sh`)
- Discord webhook
- Email summary
- Slack message

Example Discord webhook (alternative to the posting script):

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"content": "Memory mining complete. Review candidates at memory/candidates/"}' \
  "$DISCORD_WEBHOOK_URL"
```

## Monitoring

Check that mining is running:

```bash
# View recent candidate files
ls -la memory/candidates/

# Check cron logs
grep memory-mine /var/log/syslog
```

## Troubleshooting

**No candidates generated:**
- Check that daily memory files exist (`memory/YYYY-MM-DD.md`)
- Verify path configuration in scripts
- Run with `--dry-run` to debug

**Candidates too noisy:**
- Adjust `summarize_bullets()` filters
- Add more patterns to skip list
- Increase quality thresholds

**Missing permissions:**
- Ensure cron user can read/write to workspace
- Check directory ownership
