#!/usr/bin/env python3
"""
Nightly Memory Review Summary Generator

Creates a review checklist from mined memory and skill candidates.
Run this after nightly-memory-mine.py to generate a summary for
next-day review and approval.

Usage:
    python3 nightly-memory-review-summary.py                    # for today
    python3 nightly-memory-review-summary.py --date 2026-04-01  # specific date

Output:
    memory/candidates/YYYY-MM-DD-review-summary.md
"""

import argparse
from datetime import datetime
from pathlib import Path

# ============================================================
# CONFIGURATION - Edit this path for your environment
# ============================================================

WORKSPACE = Path('/Users/mirabot/.openclaw/workspace')

# ============================================================


def read_text(path: Path) -> str:
    """Safely read a file, returning empty string on error."""
    try:
        return path.read_text()
    except Exception:
        return ''


def collect_items(text: str, prefix: str) -> list[list[str]]:
    """
    Extract items that start with prefix, along with their sub-items.
    Returns list of [main_item, sub_item1, sub_item2, ...]
    """
    items = []
    current = None
    for line in text.splitlines():
        if line.startswith(prefix):
            current = line[len(prefix):].strip()
            items.append([current])
        elif current and line.startswith('  - '):
            items[-1].append(line[4:].strip())
    return items


def generate_review_summary(day: str, mem_items: list, skill_items: list) -> list[str]:
    """Generate the review summary content."""
    lines = [
        f'# Review Summary - {day}',
        '',
        'Review checklist for nightly-generated memory and skill candidates.',
        '',
        '## Review guidance',
        '',
        '**Approve** candidates that are:',
        '- Stable and unlikely to change',
        '- Actionable for future tasks',
        '- Supported by concrete evidence',
        '- Useful across multiple situations',
        '',
        '**Dismiss** candidates that are:',
        '- One-off noise or chat fragments',
        '- Speculative or weakly supported',
        '- Already captured elsewhere',
        '- Too narrow to be reusable',
        '',
        '---',
        '',
        f'## Memory candidates ({len(mem_items)})',
        ''
    ]

    if mem_items:
        for item in mem_items:
            lines.append(f'- [ ] **{item[0]}**')
            lines.append('  - Decision: `approve` / `dismiss` / `move to project memory`')
            # Include first supporting note if present
            for extra in item[1:2]:
                if not extra.startswith('Suggested action'):
                    lines.append(f'  - {extra}')
    else:
        lines.append('- _No memory candidates found for this date._')

    lines.extend(['', f'## Skill candidates ({len(skill_items)})', ''])

    if skill_items:
        for item in skill_items:
            lines.append(f'- [ ] **{item[0]}**')
            lines.append('  - Decision: `approve` / `dismiss` / `merge with existing`')
            # Include supporting notes
            for extra in item[1:3]:
                if not extra.startswith('Suggested action'):
                    lines.append(f'  - {extra}')
    else:
        lines.append('- _No skill candidates found for this date._')

    lines.extend([
        '',
        '---',
        '',
        '## After review',
        '',
        '1. Mark approved items above',
        '2. Manually promote approved candidates to:',
        '   - `MEMORY.md` for durable facts/preferences',
        '   - `memory/skills/*.md` for reusable workflows',
        '   - `memory/projects/*.md` for project-specific context',
        '3. Delete or archive dismissed candidates',
    ])

    return lines


def main():
    parser = argparse.ArgumentParser(
        description='Generate a review summary for mined memory/skill candidates.'
    )
    parser.add_argument(
        '--date',
        help='Date in YYYY-MM-DD format (defaults to today)'
    )
    args = parser.parse_args()

    day = args.date or datetime.now().strftime('%Y-%m-%d')

    # Read candidate files
    mem_file = WORKSPACE / 'memory' / 'candidates' / f'{day}-memory-candidates.md'
    skill_file = WORKSPACE / 'memory' / 'skills' / 'candidates' / f'{day}-skill-candidates.md'
    out_file = WORKSPACE / 'memory' / 'candidates' / f'{day}-review-summary.md'

    mem_text = read_text(mem_file)
    skill_text = read_text(skill_file)

    if not mem_text and not skill_text:
        print(f'No candidate files found for {day}. Run nightly-memory-mine.py first.')
        return

    # Extract items
    mem_items = collect_items(mem_text, '- Candidate: ')
    # Also capture coordination outcomes
    mem_items.extend(collect_items(mem_text, '- Completed task: '))
    skill_items = collect_items(skill_text, '- Title: ')

    # Generate and write summary
    lines = generate_review_summary(day, mem_items, skill_items)
    out_file.write_text('\n'.join(lines).rstrip() + '\n')
    print(f'Wrote {out_file}')


if __name__ == '__main__':
    main()
