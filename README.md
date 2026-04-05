# SImpleScanner
Its a lightweight web application directory and file enumeration tool built in Python. It is designed to demonstrate the core concepts of directory brute-forcing used in cybersecurity and penetration testing.

---

## Features
- Multi-threaded scanning for faster performance
- Directory and file brute-forcing
- Extension-based fuzzing (.php, .html, .txt, etc.)
- Smart response filtering to reduce false positives
- Custom User-Agent support
- Optional output file saving
- Command-line interface (CLI)

---

## How It Works? 
It takes a target URL and a wordlist, then attempts to discover hidden directories and files by sending HTTP requests. It analyzes response status codes and filters results based on user input.
