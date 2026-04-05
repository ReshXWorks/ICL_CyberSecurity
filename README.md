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
- Verbose mode for debugging
- Command-line interface (CLI)

---

## How It Works? 
It takes a target URL and a wordlist, then attempts to discover hidden directories and files by sending HTTP requests. It analyzes response status codes and filters results based on user input.

```bash
git clone https://github.com/ReshXWorks/ICL_CyberSecurity.git
cd ICL_CyberSecurity
pip install requests
```

## Basic Usage

```bash
python main.py -u http://example.com -w wordlist.txt
```

### Options Explained

| Option | Full Form    | Description                                                                           | Example                 |
| ------ | ------------ | ------------------------------------------------------------------------------------- | ----------------------- |
| `-u`   | `--url`      | Target URL to scan                                                                    | `-u http://example.com` |
| `-w`   | `--wordlist` | Path to wordlist file                                                                 | `-w wordlist.txt`       |
| `-t`   | `--threads`  | Number of concurrent threads (default: 10)                                            | `-t 20`                 |
| `-s`   | `--show`     | Status codes to display (comma-separated)                                             | `-s 200,403`            |
| `-e`   | `--ext`      | File extensions to brute-force (comma-separated). Include empty value for directories | `-e .php,.html,.txt,`   |
| `-o`   | `--output`   | Save results to file (optional)                                                       | `-o results.txt`        |
| `-v`   | `--verbose`  | Show all requests                                                                     | `-v`                    |

## Advanced Usage Examples

### 1. Show only valid and restricted pages

```bash
python main.py -u http://example.com -w wordlist.txt -s 200,403
```

### 2. Use more threads for faster scanning

```bash
python main.py -u http://example.com -w wordlist.txt -t 30
```

### 3. Enable file extension fuzzing

```bash
python main.py -u http://example.com -w wordlist.txt -e .php,.html,.txt,
```

### 4. Save results to a file

```bash
python main.py -u http://example.com -w wordlist.txt -o results.txt
```

### 5. Full featured scan

```bash
python main.py -u http://example.com -w wordlist.txt -t 20 -s 200,403 -e .php,.html,.txt, -o results.txt
```

### 6. Verbose mode
```bash
python simplescanner.py -u http://example.com -w wordlist.txt -v
```

---

## Example Target

```bash
python main.py -u http://testphp.vulnweb.com -w wordlist.txt -t 20 -o results.txt
```

## 📊 Sample Output

```
[200] http://example.com/admin (size: 5321)
[403] http://example.com/dashboard (size: 1200)
```

---




