# Web Application Directory and File Enumeration using Security Tools
Initially, a vulnerable machine was deployed using the TryHackMe platform to practice web enumeration. The tools below were tested on this environment.

## Phase 1: Gobuster
Gobuster is a fast command-line tool used for brute-forcing directories and discovering hidden resources using wordlists and it was written using go

### Basic Directory Scan

```bash
gobuster dir -u http://vuln-machine -w /usr/share/wordlists/dirb/common.txt
```
<img width="724" height="468" alt="image" src="https://github.com/user-attachments/assets/25a0f51f-ec0d-44f0-afcd-ff7fc7559d37" />

### Show Important Status Codes

```bash
gobuster dir -u http://vuln-machine -w /usr/share/wordlists/dirb/common.txt -s 200,403
```

### Exclude 404 Responses

```bash
gobuster dir -u http://vuln-machine -w /usr/share/wordlists/dirb/common.txt -b 404
```

### Increase Threads

```bash
gobuster dir -u http://vuln-machine -w /usr/share/wordlists/dirb/common.txt -t 20
```
<img width="900" height="492" alt="image" src="https://github.com/user-attachments/assets/d77fb1d4-250c-4eef-af13-f53cded65acc" />

### File Extension Fuzzing

```bash
gobuster dir -u http://vuln-machine -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
```
<img width="742" height="595" alt="image" src="https://github.com/user-attachments/assets/91934799-9246-4c71-9092-90d385165106" />

### Save Output

```bash
gobuster dir -u http://vuln-machine -w /usr/share/wordlists/dirb/common.txt -o gobuster_results.txt
```
<img width="838" height="438" alt="image" src="https://github.com/user-attachments/assets/8e8f68fb-3777-43fa-85fb-00aa7cf2dc96" />

### Custom User-Agent

```bash
gobuster dir -u http://vuln-machine -w /usr/share/wordlists/dirb/common.txt -a "Mozilla/5.0"
```

### Bruteforce Login Example

```bash
gobuster dir -u http://vuln-machine -w /usr/share/wordlists/dirb/common.txt -U joker -P hannah
```
<img width="900" height="494" alt="image" src="https://github.com/user-attachments/assets/f4b1d672-54d7-4d12-9be1-aba4fd68517d" />

### NOTE:
Gobuster is fast and simple but not very flexible which i realized after trying out ffuf.

---

## Phase 2: ffuf (Fuzz Faster U Fool)
ffuf is a high-speed web fuzzing tool used to find hidden endpoints, parameters, and directories.

### Installation of ffuf

```bash
sudo apt install ffuf
```

### Installation of seclists

```bash
sudo apt install seclists -y
```

### Basic Fuzzing

```bash
ffuf -u http://vuln-ip/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt
```
<img width="800" height="490" alt="image" src="https://github.com/user-attachments/assets/57bf3b2a-55be-40c3-8a21-8a9279595680" />

### Filter by Status Codes

```bash
ffuf -u http://vuln-ip/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt -mc 200,403
```
<img width="804" height="439" alt="image" src="https://github.com/user-attachments/assets/bcab3eb6-fc93-4c14-800e-35a321da62c3" />

### Increase Threads

```bash
ffuf -u http://vuln-ip/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt -t 20
```

### Filter by Response Size

```bash
ffuf -u http://vuln-ip/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt -fs 0
```

### File Fuzzing

```bash
ffuf -u http://vuln-ip/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-files-lowercase.txt -e .php,.txt
```
<img width="784" height="718" alt="image" src="https://github.com/user-attachments/assets/3894a3f6-0496-486a-a722-9579bbe510c5" />

### Find Extensions

```bash
ffuf -u http://vuln-ip/indexFUZZ -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt
```

### Save Results

```bash
ffuf -u http://vuln-ip/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt -o ffuf_results.json
```

### Recursive Scanning

```bash
ffuf -u http://vuln-ip/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt -recursion
```
<img width="752" height="677" alt="image" src="https://github.com/user-attachments/assets/2158b03a-1759-46a2-a73f-df07aa1b6c38" />


### Parameter Discovery

```bash
ffuf -u 'http://vuln-ip/sqli-labs/Less-1/?FUZZ=1' -c -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words-lowercase.txt
```

### NOTE:
ffuf felt confusing at first, but it's actually very powerful and nice once understood.

---

## Phase 3: SimpleScanner
A custom Python-based tool was developed to replicate basic enumeration functionality 
Check it in this repo

### 🔸 Features

* Multi-threading
* File extension fuzzing
* Response filtering
* Output saving
* Verbose mode
