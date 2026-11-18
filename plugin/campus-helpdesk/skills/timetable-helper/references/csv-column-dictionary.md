# CSV Column Dictionary: `mock_timetable.csv`

| Column Name | Data Type | Permitted Values / Pattern | Description |
|---|---|---|---|
| `batch` | String | `CS-A`, `CS-B` | Academic section / cohort identifier. |
| `day` | String | `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday` | Weekday of scheduled session. Weekend days are not tracked in regular academic timetables. |
| `start_time` | String (24-hour HH:MM) | `09:00` to `16:45` | Commencing time of lecture or lab session. |
| `end_time` | String (24-hour HH:MM) | `10:00` to `16:45` | Concluding time of session. |
| `subject` | String | Course Name (e.g., `Operating Systems`, `Data Structures & Algorithms`) | Official registered course title. |
| `room` | String | `Room 101` - `Room 205`, `Lab 1` - `Lab 3` | Designated physical room or lab facility. |
| `faculty` | String | Professor Name with academic title | Assigned faculty instructor for the course. |
