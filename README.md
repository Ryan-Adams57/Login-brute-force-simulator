# Login-brute-force-simulator

A safe, local, educational demonstration of login brute-force mechanics using a fake server and a simple client.

> ⚠️ **Security & legal warning**  
> This project is only for learning. Do **not** attempt brute-force attacks against systems you do not own or do not have explicit written permission to test.

## What this repo contains

- `fake_server.py` — a local TCP "login" server (binds to 127.0.0.1:5000 by default), with per-IP rate limiting and logging.
- `brute_client.py` — a small client that tries passwords from a wordlist against the fake server.
- `sample_wordlist.txt` — small example wordlist.
- Helper files for packaging and contribution.

## Why this is safe to run locally

- The server only binds to `127.0.0.1` by default (local loopback). You can change host/port with CLI args.
- Server implements a simple rate limiter (attempts per window), and logs attempts.
- The client includes an adjustable `--delay` to avoid hammering the server.

## Quickstart

1. Start the fake server in one terminal:
```bash
python3 fake_server.py
