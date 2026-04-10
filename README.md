# Memory Improvement System

A conservative, candidate-first memory review and promotion layer for local-first multi-agent memory.

## What this does

This system packages the reviewed safety layer around OpenClaw memory. Agents write memory locally, nightly review synthesizes evidence across active workspaces, and shared memory is promoted conservatively from candidate files rather than direct autonomous rewrites.

**Key principle:** agents write locally, Improv reviews globally, and curated shared memory only changes after review.

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
| `nightly-memory-mine.py` | Repo demo script for candidate extraction and staging |
| `nightly-memory-review-summary.py` | Repo demo script for generating a review checklist |
| `run-nightly-memory-cycle.sh` | Wrapper to run both scripts for a date (defaults to yesterday) |
| `post-improvements-summary.sh` | Legacy shell posting helper for Discord review summaries |
| `docs/ARCHITECTURE.md` | Local-first multi-agent memory architecture and promotion rules |
| `docs/CRON-SETUP.md` | Nightly scheduling guidance for the review layer |
| `examples/` | Sample candidate and review outputs |

## Local-first multi-agent model

The approved operating model is:

1. Each agent or workspace owns its own local `MEMORY.md`.
2. Each agent or workspace keeps local daily logs at `memory/YYYY-MM-DD.md`.
3. Local memory stays local by default.
4. Improv reviews agent-local evidence across active workspaces.
5. Shared or global memory is promoted conservatively from reviewed evidence.

This repo should therefore be read as the review layer for a broader memory system, not as the only place memory lives.

## Relationship to newer OpenClaw memory features

This repo should now be understood as a **review and promotion safety layer**, not a replacement for native OpenClaw memory.

OpenClaw now provides native memory capabilities such as:
- `MEMORY.md` and `memory/YYYY-MM-DD.md` as the core memory surfaces
- `memory_search` and `memory_get` for retrieval
- hybrid/semantic memory indexing
- optional `DREAMS.md` and Dreaming-based consolidation

The safest operational model is:
1. Native OpenClaw memory handles storage, indexing, and recall.
2. Agents append meaningful work to local daily logs and update local `MEMORY.md` only for durable local knowledge.
3. Improv reviews cross-agent evidence and produces scoped candidate outputs.
4. This repo documents and demonstrates the **candidate generation, review summaries, and human-visible approval flow** around that process.
5. Dreaming is treated as a secondary review signal, not an autonomous source of truth.

## Directory structure

The broader local-first system expects per-workspace local memory plus shared review outputs:

```
workspace/
├── MEMORY.md
├── memory/
│   ├── YYYY-MM-DD.md
│   ├── candidates/
│   │   ├── YYYY-MM-DD-memory-candidates.md
│   │   ├── YYYY-MM-DD-global-memory-candidates.md
│   │   └── YYYY-MM-DD-review-summary.md
│   ├── projects/
│   │   ├── <project-slug>.md
│   │   └── candidates/
│   │       └── YYYY-MM-DD-project-update-candidates.md
│   ├── reviews/
│   │   ├── YYYY-MM-DD-agent-coverage.md
│   │   └── YYYY-MM-DD-cross-agent-review.md
│   └── skills/
│       ├── *.md
│       └── candidates/
│           └── YYYY-MM-DD-shared-skill-candidates.md
├── coordination/
│   └── tasks/
│       ├── done/
│       └── failed/
└── agents or sibling workspaces with their own local MEMORY.md and memory/
```

In practice, the scripts in this repo are a conservative reference implementation. A full lab deployment may also use companion helpers for appending agent-local daily logs and agent-local durable memory before nightly review runs.

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

The nightly mining layer now conceptually inspects:

- **Agent-local daily memory files** — `memory/YYYY-MM-DD.md` across active workspaces
- **Agent-local `MEMORY.md` files** — for durable local context
- **Local candidate files** — when already present in agent workspaces
- **Completed tasks** — `coordination/tasks/done/*.md`
- **Failed tasks** — `coordination/tasks/failed/*.md`
- **Agent outbox** — results from delegated agent work

It produces or supports these review outputs:

1. **Agent coverage** — what workspaces and evidence sources were reviewed
2. **Cross-agent review** — what stayed local vs project or global
3. **Global memory candidates** — durable shared findings worth promotion
4. **Shared skill candidates** — reusable workflows seen across work
5. **Project update candidates** — project-scoped updates with supporting evidence
6. **Review summary** — a compact approval checklist for human or Improv review

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
- **Agents generally**: write meaningful daily logs locally, keep durable agent-specific knowledge local by default
- **Improv**: review, triage, cross-agent synthesis, deduplication, promotion recommendations
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

## Helper scripts in the wider lab setup

In the reviewed local-first deployment, companion helpers may exist outside this repo for tasks such as:

- appending agent-local daily logs
- appending agent-local durable memory
- running cross-agent nightly mining
- generating cross-agent review summaries

Those helpers support the same candidate-first policy. This repo remains the documentation and reference package for the review model.

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

- Better duplicate detection against local and shared memory surfaces
- More input sources, including carefully reviewed transcript evidence
- Native OpenClaw cron delivery as the preferred default, with shell wrappers kept as compatibility helpers
- Integration with coordination task system
- Safe comparison of Dreaming candidates vs nightly mined candidates before any semi-automated promotion

## Current packaging note

This update documents the approved multi-agent local-first operating model without redesigning the system. It does not require autonomous memory promotion, and it keeps the candidate-first safety posture intact.

## License

MIT
