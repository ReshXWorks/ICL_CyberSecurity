import requests
from concurrent.futures import ThreadPoolExecutor
import argparse

# save results to file
def save_result(line):
    with open("results.txt", "a") as f:
        f.write(line + "\n")


#scan each word with extensions
def scan_url(base_url, word, extensions, show_codes):
    word = word.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (DirHunter Scanner)"
    }

    for ext in extensions:
        url = f"{base_url.rstrip('/')}/{word}{ext}"

        try:
            response = requests.get(url, headers=headers, timeout=3)

            #ignore very small responses since likely false positives
            if response.status_code in show_codes and len(response.text) > 50:
                output = f"[{response.status_code}] {url} (size: {len(response.text)})"
                print(output)
                save_result(output)

        except requests.exceptions.RequestException:
            pass


def main():
    parser = argparse.ArgumentParser(description="DirHunter - Directory Enumeration Tool")

    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-w", "--wordlist", required=True, help="Wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("-s", "--show", default="200,301,302,403",
                        help="Status codes to show (comma-separated)")
    parser.add_argument("-e", "--ext", default=".php,.html,.txt,",
                        help="File extensions (comma-separated, include empty for dirs)")

    args = parser.parse_args()

    base_url = args.url
    wordlist_path = args.wordlist
    threads = args.threads
    show_codes = list(map(int, args.show.split(",")))
    extensions = args.ext.split(",")

    print(f"\n[+] Target: {base_url}")
    print(f"[+] Threads: {threads}")
    print(f"[+] Status codes: {show_codes}")
    print(f"[+] Extensions: {extensions}\n")

    # Clear old results
    open("results.txt", "w").close()

    try:
        with open(wordlist_path, "r") as f:
            words = f.readlines()
    except FileNotFoundError:
        print("[-] Wordlist not found!")
        return

    # Multithreading
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for word in words:
            executor.submit(scan_url, base_url, word, extensions, show_codes)


if __name__ == "__main__":
    main()
