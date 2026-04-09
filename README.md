# Memory Improvement System

A conservative, candidate-first approach to agent memory improvement.

## What this does

This system generates **candidate** memory and skill updates from daily operational records — without directly modifying core memory files. It's designed for safe, reviewable memory improvement.

**Key principle:** Generate candidates first, review and approve later. Never autonomously overwrite curated memory.

## Why candidate-first?

Autonomous memory rewriting is risky:

- Agents can latch onto noise or misinterpretations
- One-off events get promoted to "durable facts"
- Memory drift accumulates silently
- Recovery from bad updates is tedious

The candidate-first model solves this by keeping a human (or a reviewing agent) in the loop:

1. **Mine** — extract potential updates from daily records
2. **Generate** — write candidates to staging files
3. **Review** — approve, dismiss, or defer each candidate
4. **Promote** — only approved candidates become durable memory

## Components

| File | Purpose |
|------|---------|
| `nightly-memory-mine.py` | Extract candidates from daily logs, tasks, outbox |
| `nightly-memory-review-summary.py` | Generate a checklist for reviewing candidates |
| `run-nightly-memory-cycle.sh` | Wrapper to run both scripts for a date (defaults to yesterday) |
| `post-improvements-summary.sh` | Legacy shell posting helper for Discord review summaries |

## Relationship to newer OpenClaw memory features

This repo should now be understood as a **review and promotion safety layer**, not a replacement for native OpenClaw memory.

OpenClaw now provides native memory capabilities such as:
- `MEMORY.md` and `memory/YYYY-MM-DD.md` as the core memory surfaces
- `memory_search` and `memory_get` for retrieval
- hybrid/semantic memory indexing
- optional `DREAMS.md` and Dreaming-based consolidation

The safest operational model is:
1. Native OpenClaw memory handles storage, indexing, and recall.
2. This repo handles **candidate generation, review summaries, and human-visible approval flow**.
3. Dreaming is treated as a secondary review signal, not an autonomous source of truth.

## Directory structure

The system expects this workspace layout:

```
workspace/
├── memory/
│   ├── YYYY-MM-DD.md           # Daily operational logs
│   ├── candidates/             # Memory candidate staging
│   │   ├── YYYY-MM-DD-memory-candidates.md
│   │   └── YYYY-MM-DD-review-summary.md
│   └── skills/
│       ├── *.md                # Approved skill docs
│       └── candidates/         # Skill candidate staging
│           └── YYYY-MM-DD-skill-candidates.md
├── coordination/
│   └── tasks/
│       ├── done/               # Completed task files
│       └── failed/             # Failed task files
└── MEMORY.md                   # Curated long-term memory (never auto-edited)
```

## Usage

### Generate candidates for today

```bash
python3 nightly-memory-mine.py
```

### Generate candidates for a specific date

```bash
python3 nightly-memory-mine.py --date 2026-04-01
```

### Dry run (preview without writing files)

```bash
python3 nightly-memory-mine.py --dry-run
```

### Generate a review summary

After mining, create a checklist for reviewing the candidates:

```bash
python3 nightly-memory-review-summary.py --date 2026-04-01
```

## Configuration

Edit the paths at the top of each script to match your workspace:

```python
WORKSPACE = Path('/path/to/your/workspace')
PATCHBAY = Path('/path/to/agent-workspace')  # optional, for outbox integration
```

## What gets mined

The nightly mining script inspects:

- **Daily memory files** — `memory/YYYY-MM-DD.md`
- **Completed tasks** — `coordination/tasks/done/*.md`
- **Failed tasks** — `coordination/tasks/failed/*.md`
- **Agent outbox** — results from delegated agent work

It generates two candidate files:

1. **Memory candidates** — facts, outcomes, and observations worth keeping
2. **Skill candidates** — reusable workflows and operational patterns

## Review workflow

1. Run the mining script (nightly or manually)
2. Run the review summary script
3. Compare candidate outputs against other memory signals when available:
   - current durable memory in `MEMORY.md`
   - project memory in `memory/projects/`
   - approved skill memory in `memory/skills/`
   - Dreaming output in `DREAMS.md` or `memory/.dreams/` when enabled
4. For each candidate, mark: approve / dismiss / defer
5. Manually promote approved candidates to:
   - `MEMORY.md` (for durable facts)
   - `memory/skills/*.md` (for reusable workflows)
   - `memory/projects/*.md` (for project-specific context)

Recommended roles:
- **Improv**: review, triage, deduplication, promotion recommendations
- **Patchbay**: approved implementation changes to scripts/docs/repos

## What should NOT become durable memory

Avoid promoting:

- One-off chat fragments
- Emotional tone from a single conversation
- Speculative interpretations
- Temporary TODOs
- Weakly supported inferences
- Narrow one-use-only procedures

## What makes a strong candidate

A candidate is worth promoting when it is:

- **Repeated** — appeared more than once
- **Actionable** — changes future behavior usefully
- **Stable** — unlikely to change soon
- **Cross-task** — useful across multiple situations
- **Evidence-backed** — supported by concrete outcomes

## Memory layers

This system assumes a layered memory architecture:

| Layer | Purpose | Update frequency |
|-------|---------|------------------|
| **Long-term** (`MEMORY.md`) | Stable facts, preferences, lessons | Rarely, manually |
| **Daily** (`memory/YYYY-MM-DD.md`) | Operational logs | Daily |
| **Project** (`memory/projects/`) | Project-specific state | Per-project |
| **Skills** (`memory/skills/`) | Reusable workflows | When proven |
| **Candidates** (`*/candidates/`) | Pending proposals | Nightly |

## Nightly automation

### Previous-day timing

When run via cron, the system processes **yesterday's** data, not today's. This makes sense because:

- At 3 AM, "today" has barely started
- Yesterday's logs are complete
- Review happens the following morning

The wrapper scripts default to yesterday when run without arguments.

### Example cron schedule

```cron
# 3:00 AM - generate candidates and review summary for yesterday
0 3 * * * /path/to/run-nightly-memory-cycle.sh >> /path/to/logs/memory-cycle.log 2>&1

# 3:05 AM - post review summary to Discord
5 3 * * * /path/to/post-improvements-summary.sh >> /path/to/logs/improvements-post.log 2>&1
```

### Discord review loop

The operational workflow posts review summaries to a Discord `#improvements` channel:

1. **3:00 AM** — `run-nightly-memory-cycle.sh` generates candidates for yesterday
2. **3:05 AM** — `post-improvements-summary.sh` posts the summary to Discord
3. **Morning** — humans review candidates in the Discord thread
4. **Approval** — approved items are manually promoted or handed to an agent via coordination bus

This keeps the review process visible and collaborative.

## Safe rollout

Recommended sequence:

1. Run manually for several days
2. Inspect candidate quality
3. Adjust prompts and heuristics as needed
4. Wire to cron only after validation
5. Post review summaries to a Discord channel for visibility

## Future extensions

- Project update suggestions
- Improved duplicate detection against `MEMORY.md`, `memory/projects/`, and `memory/skills/`
- More input sources (chat transcripts, coordination state, review artifacts)
- Native OpenClaw cron delivery as the preferred default, with shell wrappers kept as compatibility helpers
- Integration with coordination task system
- Safe comparison of Dreaming candidates vs nightly mined candidates before any semi-automated promotion

## License

MIT
