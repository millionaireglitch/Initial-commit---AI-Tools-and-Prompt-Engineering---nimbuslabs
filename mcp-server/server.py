#!/usr/bin/env python3
"""
Nimbus Labs Campus Helpdesk MCP Server
Implements Model Context Protocol (MCP) over stdio using JSON-RPC 2.0.
Exposes Tools (get_timetable, get_fee_status) and Resources (campus://hostel/rules).
"""

import sys
import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
TIMETABLE_CSV = os.path.join(PROJECT_DIR, "data", "timetable.csv")
FEES_JSON = os.path.join(PROJECT_DIR, "data", "mock_fees.json")
HOSTEL_RULES_MD = os.path.join(BASE_DIR, "resources", "hostel-rules.md")

VALID_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
VALID_BATCHES = ["CS-A", "CS-B"]

def load_fees_data():
    if os.path.exists(FEES_JSON):
        with open(FEES_JSON, "r", encoding="utf-8") as f:
            return json.load(f).get("students", {})
    return {}

def handle_get_timetable(args):
    batch = args.get("batch", "").strip()
    day = args.get("day", "").strip().capitalize()

    # Validate Day
    if not day or day not in VALID_DAYS:
        return {
            "content": [{"type": "text", "text": f"Validation Error: Invalid day '{day}'. Valid days are Monday through Friday."}],
            "isError": True
        }

    # Validate Batch
    if not batch or batch.upper() not in VALID_BATCHES:
        return {
            "content": [{"type": "text", "text": f"Validation Error: Unknown batch '{batch}'. Valid batches are CS-A and CS-B."}],
            "isError": True
        }

    matches = []
    if os.path.exists(TIMETABLE_CSV):
        with open(TIMETABLE_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["batch"].upper() == batch.upper() and row["day"].capitalize() == day:
                    matches.append(row)

    if not matches:
        return {
            "content": [{"type": "text", "text": f"No timetable records found for batch '{batch}' on {day}."}],
            "isError": False
        }

    matches.sort(key=lambda x: x["start_time"])
    lines = [f"Timetable for {batch.upper()} on {day}:"]
    for m in matches:
        lines.append(f"- {m['start_time']} - {m['end_time']}: {m['subject']} ({m['room']}) | Faculty: {m['faculty']}")

    return {
        "content": [{"type": "text", "text": "\n".join(lines)}],
        "isError": False
    }

def handle_get_fee_status(args):
    student_id = str(args.get("student_id", "")).strip()
    if not student_id:
        return {
            "content": [{"type": "text", "text": "Validation Error: 'student_id' parameter is required."}],
            "isError": True
        }

    fees_data = load_fees_data()
    if student_id not in fees_data:
        return {
            "content": [{
                "type": "text",
                "text": f"Student record not found for ID '{student_id}'. Fictional fee information cannot be fabricated."
            }],
            "isError": True
        }

    info = fees_data[student_id]
    result_text = (
        f"Fee Status for {info['student_name']} (Roll: {info['roll_number']}):\n"
        f"- Programme: {info['programme']} (Sem {info['semester']})\n"
        f"- Total Fee: ₹{info['total_fee']:,}\n"
        f"- Amount Paid: ₹{info['amount_paid']:,}\n"
        f"- Outstanding Dues: ₹{info['outstanding_dues']:,}\n"
        f"- Status: {info['payment_status']}\n"
        f"- Receipt: {info['receipt_number']} (Paid on {info['last_payment_date']})"
    )
    return {
        "content": [{"type": "text", "text": result_text}],
        "isError": False
    }

def handle_resources_read(uri):
    if uri == "campus://hostel/rules":
        if os.path.exists(HOSTEL_RULES_MD):
            with open(HOSTEL_RULES_MD, "r", encoding="utf-8") as f:
                content = f.read()
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "text/markdown",
                        "text": content
                    }
                ]
            }
        else:
            return {
                "contents": [{"uri": uri, "mimeType": "text/plain", "text": "Error: Hostel rules file missing."}],
                "isError": True
            }
    return {
        "contents": [{"uri": uri, "mimeType": "text/plain", "text": f"Error: Resource '{uri}' not found."}],
        "isError": True
    }

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except Exception as e:
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        response = None

        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "nimbus-campus-server",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {
                            "listChanged": False
                        },
                        "resources": {
                            "subscribe": False,
                            "listChanged": False
                        },
                        "prompts": {
                            "listChanged": False
                        }
                    }
                }
            }
        elif method == "notifications/initialized":
            # Notifications do not return a response
            continue
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_timetable",
                            "description": "Retrieve daily class schedule for a designated academic batch and weekday from verified campus records.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "batch": {
                                        "type": "string",
                                        "description": "Student cohort/batch identifier (e.g. 'CS-A', 'CS-B')"
                                    },
                                    "day": {
                                        "type": "string",
                                        "description": "Day of the week (Monday through Friday)"
                                    }
                                },
                                "required": ["batch", "day"]
                            }
                        },
                        {
                            "name": "get_fee_status",
                            "description": "Look up fee payment records and pending dues for a student using their roll number.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "student_id": {
                                        "type": "string",
                                        "description": "Unique student roll number (e.g. '150096725200')"
                                    }
                                },
                                "required": ["student_id"]
                            }
                        }
                    ]
                }
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            if tool_name == "get_timetable":
                res = handle_get_timetable(tool_args)
                response = {"jsonrpc": "2.0", "id": req_id, "result": res}
            elif tool_name == "get_fee_status":
                res = handle_get_fee_status(tool_args)
                response = {"jsonrpc": "2.0", "id": req_id, "result": res}
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method/Tool '{tool_name}' not found"}
                }
        elif method == "resources/list":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "resources": [
                        {
                            "uri": "campus://hostel/rules",
                            "name": "Hostel Residence Regulations & Curfew Policy",
                            "description": "Official rules, gate timings, and residential conduct policies for campus hostels.",
                            "mimeType": "text/markdown"
                        }
                    ]
                }
            }
        elif method == "resources/read":
            uri = params.get("uri")
            res = handle_resources_read(uri)
            response = {"jsonrpc": "2.0", "id": req_id, "result": res}
        elif method == "ping":
            response = {"jsonrpc": "2.0", "id": req_id, "result": {}}
        else:
            if req_id is not None:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not found"}
                }

        if response:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
