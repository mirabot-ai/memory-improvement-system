# Memory Architecture

This document describes the local-first multi-agent memory design and candidate-first safety model.

OpenClaw native memory is the underlying memory substrate. This repo sits above it as a conservative review and promotion layer.

## Design goals

1. **Improve durably** — build useful long-term memory without breaking workflows
2. **Stay interpretable** — keep memory human-readable and inspectable
3. **Separate layers** — native memory storage/recall vs. candidate review/promotion
4. **Enable review** — generate candidates, not direct rewrites
5. **Support multi-agent** — work with delegated agents and coordination systems

## Core operating rule

- agents write locally
- Improv reviews globally
- shared memory promotes conservatively

## Memory layers

### 1. Long-term curated memory

**File:** `MEMORY.md`

**Purpose:**
- Stable facts about users, projects, and preferences
- Validated workflows that proved useful
- Durable lessons from repeated experience

**Rules:**
- Do NOT dump raw chat history here
- Prefer distilled facts over verbose context
- Update conservatively and manually

### 2. Daily operational logs

**Files:** `memory/YYYY-MM-DD.md`

**Purpose:**
- Raw or lightly processed record of each day
- Tasks, decisions, experiments, conversations, failures, outcomes

**Rules:**
- Each active workspace keeps its own local daily log
- Okay to be rough and verbose
- Source material for nightly mining
- Channel activity should usually be summarized into the owning agent's local log rather than treated as a separate unmanaged memory universe

### 3. Project memory

**Directory:** `memory/projects/`

**Purpose:**
- Project-specific state, separate from global memory
- Status, decisions, open questions, stakeholders, outputs

**Rules:**
- One file per project: `memory/projects/<project-slug>.md`
- Update as project evolves
- Archive when project completes

### 4. Skill memory

**Directory:** `memory/skills/`

**Purpose:**
- Reusable operational patterns discovered through work
- Guides future task routing and approach selection

**Rules:**
- Each skill is a markdown file describing trigger, workflow, and examples
- Only promote patterns that proved useful more than once
- Merge similar skills rather than creating duplicates

### 5. Agent-scoped memory

**Files and directories:**
- local `MEMORY.md`
- local `memory/projects/`
- local `memory/skills/`
- local candidate files when useful

**Purpose:**
- Keep agent-local operating knowledge separate from shared canon
- Preserve persona, role conventions, and routing behavior without overpromoting them

**Rules:**
- Keep findings local unless they clearly matter beyond one agent
- Do not treat agent-local conventions as shared truth by default
- Promote only after review demonstrates project or lab-wide value

### 6. Candidate staging and review outputs

**Directories:**
- `memory/candidates/`
- `memory/skills/candidates/`
- `memory/projects/candidates/`
- `memory/reviews/`

**Purpose:**
- Stage promotion proposals from nightly review
- Record cross-agent coverage and synthesis
- Never automatically promote to curated memory

**Rules:**
- Review daily or periodically
- Approve, dismiss, defer, or keep local
- Keep evidence pointers so promotions remain auditable

## Candidate-first policy

The nightly automation should generate candidates first. It should **NOT** directly rewrite:

- `MEMORY.md`
- Core workflow docs
- Delegation policy docs
- Established skill files

This keeps memory updates:
- **Reviewable** — humans or Improv can inspect before promotion
- **Reversible** — bad candidates are simply deleted
- **Auditable** — you can see what was proposed vs. what was accepted
- **Aligned with OpenClaw** — native memory remains the source of storage and recall truth

## What makes a good candidate

### Strong candidates

- **Repeated** — appeared in multiple contexts
- **Actionable** — changes future behavior usefully
- **Stable** — unlikely to change soon
- **Cross-task** — useful across multiple situations
- **Evidence-backed** — supported by concrete outcomes

### Weak candidates (avoid promoting)

- One-off chat fragments
- Emotional tone from a single conversation
- Speculative interpretations
- Temporary TODOs
- Weakly supported inferred preferences
- Narrow procedures with no reuse potential

## Dreaming and review signals

If Dreaming is enabled, treat Dreaming output as a supervised secondary signal.

Use it to:
- compare overlap with mined candidates
- spot durable themes that may deserve review
- catch possible omissions

Do not use Dreaming output as an autonomous source of truth or as a direct promotion path.

## Multi-agent implications

As more agents are added:

| Memory layer | Scope |
|--------------|-------|
| Local `MEMORY.md` | Agent-scoped, durable, local by default |
| Local daily logs | Per-agent operational evidence |
| Project (`memory/projects/`) | Carries project context across agents |
| Shared/global `MEMORY.md` | Sparse and stable, only after promotion |
| Skills | Captures reusable workflows |
| Reviews | Cross-agent synthesis and coverage |
| Dreaming | Secondary comparison signal only |

Recommended operating roles:
- **Agents generally** write local logs and local durable memory
- **Improv** reviews, triages, compares across agents, and recommends promotion actions
- **Patchbay** implements approved repo, script, doc, and workflow changes

## Evolution path

### Phase 1 (current)
- Architecture defined
- Candidate directories created
- Nightly mining generates candidates only
- Manual review and promotion

### Phase 2 (current reviewed extension)
- Review candidate quality across active workspaces
- Refine cross-agent mining heuristics
- Add project update suggestions, shared skill candidates, and global memory candidates
- Produce review artifacts such as agent coverage and cross-agent review summaries

### Phase 3 (future)
- Better duplicate detection against local and shared memory surfaces
- Integration with notification channels
- Coordination task creation for review
- Optional comparison tooling between Dreaming output and mined candidates
