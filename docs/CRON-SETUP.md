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

If using OpenClaw, prefer the native cron tool over shell wrappers whenever practical.

```
Schedule: kind=cron, expr="0 3 * * *", tz="America/New_York"
Payload: kind=agentTurn, message="Run nightly memory mining for yesterday and generate review summary"
SessionTarget: isolated
```

Native OpenClaw cron is preferred because it provides:
- cleaner channel delivery
- explicit session targeting
- better run logs and delivery status
- better alignment with agent-owned channels such as Improv in `#improvements`

Use shell wrappers only when you specifically need compatibility with an external scheduler or a standalone repo demo.

## Discord review loop

The recommended operational workflow:

1. **3:00 AM** — native OpenClaw cron or `run-nightly-memory-cycle.sh` generates candidates for yesterday
2. **3:05 AM** — native OpenClaw cron delivery or `post-improvements-summary.sh` posts to Discord `#improvements`
3. **Morning** — humans and/or Improv review candidates in the Discord channel
4. **Approval** — approved items are manually promoted to memory, or handed to Patchbay via coordination bus
5. **Optional comparison lane** — if Dreaming is enabled, compare Dreaming suggestions against the nightly candidate set before promotion

This keeps the review visible and collaborative. Configure the Discord channel ID in `post-improvements-summary.sh` only if you are using the legacy shell helper.

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
