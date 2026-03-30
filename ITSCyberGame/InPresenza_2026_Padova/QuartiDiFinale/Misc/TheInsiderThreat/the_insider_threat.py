#!/usr/bin/env python3
import sys
import sqlite3
from datetime import datetime


def main(db_path: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    SELECT e.first_name, e.last_name, ft.timestamp, ft.protocol, ft.destination_ip
    FROM file_transfers ft
    JOIN employees e ON e.id = ft.employee_id
    WHERE ft.destination_ip IS NOT NULL
      AND ft.proxy_used = 0
      AND ft.file_size_mb > 500
    ORDER BY ft.timestamp DESC
    LIMIT 1
    """)

    row = cur.fetchone()
    if not row:
        print("No matching transfer found.")
        return 2

    first, last, ts, proto, ip = row
    try:
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    except Exception:
        dt = None

    last_octet = ip.split('.')[-1]

    if dt:
        timestr = dt.strftime("%Y%m%d_%H%M")
    else:
        timestr = ts.replace(' ', '_')

    flag = f"flag{{{first.lower()}_{last.lower()}_{timestr}_{proto}_{last_octet}}}"
    print(flag)
    return 0


if __name__ == '__main__':
    db = sys.argv[1] if len(sys.argv) > 1 else 'datavault_incident.db'
    sys.exit(main(db))
