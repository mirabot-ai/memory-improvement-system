# Cron Setup Guide

How to schedule automatic nightly memory mining.

## Prerequisites

Before automating, manually run the scripts for several days to:
1. Verify candidate quality
2. Tune heuristics if needed
3. Establish a review habit

## Example cron entry

Run nightly at 2:15 AM:

```cron
15 2 * * * cd /path/to/workspace && python3 /path/to/nightly-memory-mine.py >> /path/to/logs/memory-mine.log 2>&1
```

Generate review summary shortly after:

```cron
20 2 * * * cd /path/to/workspace && python3 /path/to/nightly-memory-review-summary.py >> /path/to/logs/memory-mine.log 2>&1
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

If using OpenClaw, you can schedule via the cron tool:

```
Schedule: kind=cron, expr="15 2 * * *", tz="America/New_York"
Payload: kind=agentTurn, message="Run nightly memory mining and generate review summary"
SessionTarget: isolated
```

## Notification options

After mining completes, optionally notify via:
- Discord webhook to an improvements channel
- Email summary
- Slack message
- Push notification

Example Discord webhook (add to the end of your cron script):

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
