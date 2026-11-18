#!/usr/bin/env python3
"""
Timetable Helper Query Utility
Reads and filters mock_timetable.csv with deterministic validation.
"""

import sys
import os
import csv
import json
import argparse

VALID_DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
VALID_BATCHES = {"CS-A", "CS-B"}

def find_timetable_csv():
    # Check local references first, then relative paths
    search_paths = [
        os.path.join(os.path.dirname(__file__), "../references/mock_timetable.csv"),
        os.path.join(os.path.dirname(__file__), "../../data/timetable.csv"),
        os.path.join(os.path.dirname(__file__), "../../../data/timetable.csv"),
        "data/timetable.csv",
        "mock_timetable.csv"
    ]
    for p in search_paths:
        if os.path.exists(p):
            return os.path.abspath(p)
    return None

def query_timetable(batch=None, day=None, subject=None):
    csv_path = find_timetable_csv()
    if not csv_path:
        return {"error": "Timetable database file not found."}

    if day and day.capitalize() not in VALID_DAYS:
        return {"error": f"Invalid day '{day}'. Regular academic classes are held Monday through Friday."}

    if batch and batch.upper() not in VALID_BATCHES:
        return {"error": f"Invalid batch '{batch}'. Active batches are CS-A and CS-B."}

    results = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            match_batch = not batch or row["batch"].upper() == batch.upper()
            match_day = not day or row["day"].capitalize() == day.capitalize()
            match_sub = not subject or subject.lower() in row["subject"].lower()

            if match_batch and match_day and match_sub:
                results.append(row)

    # Sort results chronologically by start_time
    results.sort(key=lambda x: x["start_time"])
    return {"count": len(results), "records": results}

def main():
    parser = argparse.ArgumentParser(description="Query Campus Timetable Data")
    parser.add_argument("--batch", type=str, help="Batch identifier (e.g. CS-A, CS-B)")
    parser.add_argument("--day", type=str, help="Day of week (Monday-Friday)")
    parser.add_argument("--subject", type=str, help="Subject name search filter")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    data = query_timetable(args.batch, args.day, args.subject)

    if args.json or "error" in data:
        print(json.dumps(data, indent=2))
        return

    records = data["records"]
    if not records:
        print(f"No classes found matching criteria: batch={args.batch}, day={args.day}, subject={args.subject}")
        return

    print(f"\nFound {len(records)} class session(s):")
    print(f"| {'Time Slot':<13} | {'Batch':<6} | {'Subject':<32} | {'Room':<10} | {'Faculty':<20} |")
    print(f"|{'-'*15}|{'-'*8}|{'-'*34}|{'-'*12}|{'-'*22}|")
    for r in records:
        slot = f"{r['start_time']} - {r['end_time']}"
        print(f"| {slot:<13} | {r['batch']:<6} | {r['subject']:<32} | {r['room']:<10} | {r['faculty']:<20} |")

if __name__ == "__main__":
    main()
