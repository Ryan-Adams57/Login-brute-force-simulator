#!/usr/bin/env python3
"""
fake_server.py
A simple local TCP "login" server for educational brute-force testing.

Usage:
  python3 fake_server.py

Notes:
  - Binds to 127.0.0.1:5000 by default.
  - Single valid credential can be changed in VALID_CREDENTIAL.
  - Rate limiting: max_attempts per window_seconds per remote address.
  - Designed for learning; only run locally.
"""

import socket
import threading
import time
from collections import defaultdict

HOST = "127.0.0.1"
PORT = 5000

VALID_CREDENTIAL = ("alice", "S3cure-P@ss")  # change for tests

# rate limiting settings
max_attempts = 5
window_seconds = 60

# store attempts per address
attempts = defaultdict(list)  # addr -> [timestamps]

def is_rate_limited(addr):
    now = time.time()
    window = [t for t in attempts[addr] if now - t <= window_seconds]
    attempts[addr] = window
    return len(window) >= max_attempts

def handle_client(conn, addr):
    ip = addr[0]
    with conn:
        data = conn.recv(1024).decode(errors="ignore").strip()
        # Expect data in "username:password" format
        print(f"[{time.strftime('%H:%M:%S')}] Received from {ip}: {data}")
        if is_rate_limited(ip):
            reply = "ERROR: rate limit exceeded\n"
            conn.sendall(reply.encode())
            print(f"Rate-limited {ip}")
            return
        attempts[ip].append(time.time())

        if ":" not in data:
            conn.sendall(b"ERROR: bad format\n")
            return
        user, pwd = data.split(":", 1)
        if user == VALID_CREDENTIAL[0] and pwd == VALID_CREDENTIAL[1]:
            conn.sendall(b"OK: authenticated\n")
            print(f"Successful login for {user} from {ip}")
        else:
            conn.sendall(b"FAIL: invalid credentials\n")

def main():
    print("Fake login server (local only) listening on", f"{HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    main()
