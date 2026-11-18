# Timetable Edge Cases and Handling Protocols

### 1. Unknown or Invalid Batch Identifier
- **Condition**: User provides a batch identifier not in the registry (e.g. `CS-Z`, `MECH-1`, `MBA-A`).
- **Response**: "The requested batch '<BATCH>' is not recognized in our campus records. Currently tracked batches are `CS-A` and `CS-B`. Please verify your cohort."

### 2. Invalid or Weekend Day
- **Condition**: User asks for Saturday, Sunday, or an invalid weekday like `Funday`.
- **Response**: "No regular classes are scheduled on <DAY>. Academic timetables operate Monday through Friday."

### 3. Missing Parameters (Ambiguous Input)
- **Condition**: User asks "What classes do I have tomorrow?" or "Where is my lecture?" without batch or specific day.
- **Response**: "Could you please specify your batch (e.g., CS-A or CS-B) and the target day so I can retrieve your exact schedule?"

### 4. Non-Existent Subject Query (Adversarial / Accidental)
- **Condition**: User queries a subject not in the syllabus (e.g., "Quantum Computing", "Advanced Astrophysics") or asks the model to pretend.
- **Response**: "Subject '<SUBJECT>' is not part of the active timetable for batch <BATCH>. I cannot generate fictional or unverified course schedules."

### 5. Overlapping / Multi-Hour Sessions
- **Condition**: Lab sessions spanning multiple hours (e.g. 14:45–16:45).
- **Response**: Display continuous slot clearly: `14:45 - 16:45 (2 Hours)`.
