# Memory Architecture

This document describes the memory layer design and candidate-first safety model.

## Design goals

1. **Improve durably** — build useful long-term memory without breaking workflows
2. **Stay interpretable** — keep memory human-readable and inspectable
3. **Separate layers** — raw logs vs. curated memory vs. project context
4. **Enable review** — generate candidates, not direct rewrites
5. **Support multi-agent** — work with delegated agents and coordination systems

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
- Okay to be rough and verbose
- Source material for nightly mining
- Delete or archive old logs as needed

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

### 5. Candidate staging

**Directories:**
- `memory/candidates/` — memory candidate proposals
- `memory/skills/candidates/` — skill candidate proposals

**Purpose:**
- Pending proposals from nightly mining
- Never automatically promoted to curated memory

**Rules:**
- Review daily or periodically
- Approve, dismiss, or defer each candidate
- Delete after processing

## Candidate-first policy

The nightly automation should generate candidates first. It should **NOT** directly rewrite:

- `MEMORY.md`
- Core workflow docs
- Delegation policy docs
- Established skill files

This keeps memory updates:
- **Reviewable** — humans can inspect before promotion
- **Reversible** — bad candidates are simply deleted
- **Auditable** — you can see what was proposed vs. what was accepted

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

## Multi-agent implications

As more agents are added:

| Memory layer | Scope |
|--------------|-------|
| Long-term (`MEMORY.md`) | Sparse and stable, shared |
| Project (`memory/projects/`) | Carries most context |
| Coordination | Tracks delegated agent work |
| Skills | Captures reusable workflows |
| Daily logs | Per-agent or combined |

## Evolution path

### Phase 1 (current)
- Architecture defined
- Candidate directories created
- Nightly mining generates candidates only
- Manual review and promotion

### Phase 2 (future)
- Review candidate quality over time
- Refine mining heuristics
- Add project update suggestions

### Phase 3 (future)
- Optional semi-automatic promotion for high-confidence updates
- Integration with notification channels
- Coordination task creation for review
