#!/usr/bin/env python3
"""Split reports into separate files per appid"""

# pylint: disable=invalid-name

import json
import os
import sys

from datetime import datetime


def load_reports():
    all_reports = {}
    last_timestamp = 0
    with open('reports_piiremoved.json') as reports_file:
        reports = json.load(reports_file)
        for r in reports:
            timestamp = int(r['timestamp'])
            title = r['title']
            if timestamp > last_timestamp:
                last_timestamp = timestamp
            if not 'appId' in r:
                print(f'W: {title} @ {timestamp} is missing appId', file=sys.stderr)
                continue
            app_id = r['appId']
            try:
                int(app_id)
            except ValueError:
                print(f'W: {title} @ {timestamp} has non-numeric appId', file=sys.stderr)
                continue
            if not app_id in all_reports:
                all_reports[app_id] = []
            all_reports[app_id].append(r)
    dt = datetime.utcfromtimestamp(last_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f'I: the newest report from {dt}', file=sys.stderr)
    return all_reports


def main():
    app_reports = load_reports()
    os.makedirs('json', exist_ok=True)
    for app_id, reports in app_reports.items():
        with open(f'json/{app_id}-reports.json', 'w') as f:
            f.write(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
