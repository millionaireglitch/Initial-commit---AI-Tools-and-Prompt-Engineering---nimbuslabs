#!/usr/bin/env python3
"""
PreToolUse Security Hook for Nimbus Campus Helpdesk Plugin
Enforces strict path and command sanitization to protect sensitive system assets.
Adheres to the platform specification: Always outputs JSON and exits with code 0.
"""

import sys
import json
import re

BLOCKED_PATTERNS = [
    r"/etc/passwd",
    r"/etc/shadow",
    r"\.env",
    r"id_rsa",
    r"credentials\.json",
    r"api[-_]?key",
    r"rm\s+-rf\s+/",
    r":\(\)\s*\{" # fork bomb pattern
]

def evaluate_payload(text_to_check):
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text_to_check, re.IGNORECASE):
            return False, f"Access blocked: hazardous pattern '{pattern}' detected in payload."
    return True, "Payload authorized."

def main():
    raw_input = ""
    # Support both stdin (runtime hook) and argv (CLI testing)
    if not sys.stdin.isatty():
        raw_input = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        raw_input = " ".join(sys.argv[1:])

    if not raw_input:
        # Default allow if empty
        output = {"decision": "allow", "reason": "Empty input."}
        print(json.dumps(output))
        sys.exit(0)

    # Check if input is structured JSON
    try:
        data = json.loads(raw_input)
        command_str = data.get("CommandLine") or data.get("command") or data.get("Path") or str(data)
    except Exception:
        command_str = raw_input

    is_allowed, reason = evaluate_payload(command_str)

    if is_allowed:
        output = {"decision": "allow", "reason": "Security scan passed."}
    else:
        output = {"decision": "deny", "reason": reason}

    print(json.dumps(output, indent=2))
    # Crucial: Always exit with 0 so the host environment correctly parses the denial JSON
    sys.exit(0)

if __name__ == "__main__":
    main()
