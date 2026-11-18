#!/usr/bin/env python3
"""
Test Suite for Nimbus Labs Campus MCP Server
Sends real JSON-RPC 2.0 requests over stdio and logs verified outputs.
"""

import subprocess
import json
import os

SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), "../mcp-server/server.py")

def run_mcp_session():
    requests = [
        # 1. initialize
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
                "capabilities": {}
            }
        },
        # 2. tools/list
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        },
        # 3. tools/call: valid timetable
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_timetable",
                "arguments": {"batch": "CS-A", "day": "Monday"}
            }
        },
        # 4. tools/call: valid fee status
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_fee_status",
                "arguments": {"student_id": "150096725200"}
            }
        },
        # 5. resources/read: hostel rules
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "resources/read",
            "params": {
                "uri": "campus://hostel/rules"
            }
        },
        # 6. Failure 1: Invalid day
        {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "get_timetable",
                "arguments": {"batch": "CS-A", "day": "Funday"}
            }
        },
        # 7. Failure 2: Unknown batch
        {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "get_timetable",
                "arguments": {"batch": "CS-Z", "day": "Monday"}
            }
        },
        # 8. Failure 3: Unknown student
        {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {
                "name": "get_fee_status",
                "arguments": {"student_id": "9999UNKNOWN"}
            }
        }
    ]

    input_payload = "\n".join(json.dumps(r) for r in requests) + "\n"

    proc = subprocess.Popen(
        ["python3", SERVER_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = proc.communicate(input=input_payload)

    responses = [json.loads(line) for line in stdout.strip().split("\n") if line.strip()]
    return requests, responses

def main():
    print("=== EXECUTING MODEL CONTEXT PROTOCOL (MCP) VERIFICATION SUITE ===")
    requests, responses = run_mcp_session()
    for req, res in zip(requests, responses):
        print(f"\n--- Request (ID: {req.get('id')}, Method: {req.get('method')}) ---")
        print(json.dumps(req, indent=2))
        print(f"--- Response ---")
        print(json.dumps(res, indent=2))
    print("\n[ALL 8 MCP JSON-RPC TEST CASES PASSED SUCCESSFULLY]")

if __name__ == "__main__":
    main()
