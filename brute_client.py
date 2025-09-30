#!/usr/bin/env python3
"""
brute_client.py
Client that attempts password guesses from a wordlist against the local fake server.

Usage:
  # Ensure fake_server.py is running locally
  python3 brute_client.py wordlist.txt

wordlist.txt format: one password per line. Username defaults to 'alice' (changeable).
Includes a small delay between attempts to avoid spamming.
"""

import socket
import sys
import time

HOST = "127.0.0.1"
PORT = 5000
USERNAME = "alice"
DELAY_SECONDS = 0.5  # polite delay between attempts

def try_password(password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        s.connect((HOST, PORT))
        payload = f"{USERNAME}:{password}\n"
        s.sendall(payload.encode())
        resp = s.recv(1024).decode(errors="ignore").strip()
        return resp

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 brute_client.py wordlist.txt")
        sys.exit(1)

    wordlist = sys.argv[1]
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            password = line.strip()
            if not password:
                continue
            print("Trying:", password)
            try:
                resp = try_password(password)
            except Exception as e:
                print("Error connecting:", e)
                break
            print("Server:", resp)
            if resp.startswith("OK"):
                print("Password found:", password)
                return
            # handle server rate-limiting response with a pause
            if "rate limit" in resp.lower():
                print("Server rate-limited us. Sleeping 10s")
                time.sleep(10)
            else:
                time.sleep(DELAY_SECONDS)

    print("Finished wordlist - password not found.")
    
if __name__ == "__main__":
    main()
