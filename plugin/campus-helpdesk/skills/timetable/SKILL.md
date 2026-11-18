---
name: timetable
description: Custom slash command /timetable to quickly query lecture schedules by batch and weekday.
---

# `/timetable` Slash Command

## Usage
`/timetable [batch] [day]`

Example:
- `/timetable CS-A Monday`
- `/timetable CS-B Wednesday`

## Behavior
When invoked, this command extracts the `batch` and `day` arguments, validates them against official campus cohorts (`CS-A`, `CS-B`) and weekdays (`Monday` to `Friday`), queries `references/mock_timetable.csv`, and outputs an immediate chronological timetable summary table.
