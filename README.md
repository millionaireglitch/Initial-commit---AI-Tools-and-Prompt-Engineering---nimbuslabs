 Nimbus Labs Campus Helpdesk Agent
A modular campus assistant system implementing Agent Skills, Plugins, and MCP Server.
Student: Sneha Chaturvedi | Roll: 150096725200 | Programme: B.Tech CSE (Second Year)

Module Status
- Feature Tests: Verified timetable skill triggers and edge-case handling across 6 prompt suites.
- Security Hook: Enforced absolute path sanitization and JSON return schema for PreToolUse hooks.


## 🚀 Quickstart & Execution

### 1. Test the Timetable Helper Skill
Run the automated test runner to verify triggers, ambiguity resolution, and anti-hallucination defense:
```bash
python3 tests/test_skill.py
