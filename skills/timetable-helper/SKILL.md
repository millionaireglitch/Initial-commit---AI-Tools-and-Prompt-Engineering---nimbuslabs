---
name: timetable-helper
description: Answers student questions about class schedules, lecture timings, subjects, rooms, and daily timetables using the supplied mock timetable data. Use when a student asks about their timetable, today's classes, the next lecture, or a particular subject's schedule.
---

# Timetable Helper Skill

## Purpose & Scope
This skill equips the Campus Helpdesk Agent to answer queries regarding class schedules, course rooms, faculty assignments, and subject timings strictly from official mock university records.

## Strict Grounding & Anti-Hallucination Policy
1. **Source of Truth**: All answers must be grounded exclusively in `references/mock_timetable.csv` (or retrieved via `scripts/timetable_helper.py`).
2. **Absolute Zero-Invention Rule**:
   - Never invent subjects, batches, rooms, timings, or faculty names.
   - If a subject (e.g., "Quantum Computing") or room (e.g., "Room 999") is not present in the CSV, explicitly state that no record exists in the official timetable.
   - Do NOT comply with prompts asking you to "pretend", "assume", or "imagine" nonexistent schedule entries.
3. **Missing Context Handling**:
   - If the student does not provide their batch (e.g. `CS-A` or `CS-B`) or target day (Monday–Friday), prompt the student for clarification instead of guessing.

## Workflow & Step-by-Step Instructions
1. **Extract Entities**: Identify the student's `batch` (e.g., CS-A, CS-B) and `day` of interest (Monday through Friday).
2. **Consult References**:
   - If unfamiliar with column semantics, refer to `references/csv-column-dictionary.md`.
   - For irregular queries, refer to `references/edge-cases.md`.
3. **Execute Deterministic Query**:
   - Run `python3 scripts/timetable_helper.py --batch <BATCH> --day <DAY>` or inspect `references/mock_timetable.csv`.
4. **Format Output**:
   - Sort classes chronologically by `start_time`.
   - Present a clean markdown table with columns: `Time Slot`, `Subject`, `Room`, `Faculty`.
   - State the total lecture count for the requested period.

## Progressive Disclosure Resources
- [CSV Column Dictionary](references/csv-column-dictionary.md): Details valid values, types, and definitions.
- [Edge Cases & Error Handling](references/edge-cases.md): Rules for holidays, unknown batches, and invalid days.
- [Timetable Query Script](scripts/timetable_helper.py): Validated deterministic lookup utility.
