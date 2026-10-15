\# TryHackMe Write-up: RootMe



\## 1. Executive Summary

\- \*\*Target:\*\* TryHackMe: RootMe

\- \*\*OS:\*\* Linux

\- \*\*Vulnerabilities:\*\* Unrestricted File Upload (Extension Filter Bypass), SUID Misconfiguration

\- \*\*Objective:\*\* Obtain initial access via web shell and escalate privileges to root.



\## 2. Reconnaissance

\*\*Nmap Port Scan:\*\*

Identified open ports for SSH (22) and HTTP (80).

`nmap -sV -sC <Target\_IP>`



\*\*Directory Busting (Gobuster):\*\*

Brute-forced the web server using `common.txt` to uncover hidden directories.

`gobuster dir -u http://<Target\_IP> -w /usr/share/wordlists/dirb/common.txt`

\*Discovered Directories:\* `/panel` (Upload form) and `/uploads` (Storage).



\## 3. Initial Foothold

\*\*Vulnerability:\*\* Unrestricted File Upload.

The `/panel` directory contained an upload form. The server blocked standard `.php` extensions but failed to sanitize alternative PHP extensions. 



\*\*Execution:\*\*

1\. Copied the standard `php-reverse-shell.php` payload from the Kali `webshells` directory.

2\. Modified the payload to point back to the local Kali VPN IP on port 4444.

3\. Renamed the file to `revshell.php5` to bypass the `.php` filter.

4\. Uploaded the payload and started a Netcat listener (`nc -lvnp 4444`).

5\. Navigated to `/uploads/revshell.php5` to execute the script and catch the reverse shell as `www-data`.

6\. Captured the `user.txt` flag.



\## 4. Privilege Escalation

\*\*Vulnerability:\*\* SUID Misconfiguration.

Searched for files with the SUID bit set to identify potential privilege escalation vectors.

`find / -type f -user root -perm -4000 2>/dev/null`



\*\*Execution:\*\*

1\. Identified `/usr/bin/python` in the SUID list, which is highly abnormal.

2\. Leveraged GTFOBins techniques to abuse the Python SUID binary.

3\. Executed the privilege escalation command:

&#x20;  `python -c 'import os; os.execl("/bin/sh", "sh", "-p")'`

4\. Gained `root` shell and captured `root.txt`.



\## 5. Lessons Learned / Remediation

\- \*\*Validation Bypass:\*\* Never rely solely on blocking specific file extensions (like `.php`). Use an explicit whitelist of allowed extensions (e.g., `.jpg`, `.png`) and validate file contents.

\- \*\*Least Privilege:\*\* Web application upload directories should never have execute permissions.

\- \*\*SUID Hardening:\*\* Standard application binaries like Python should never have the SUID bit set, as it allows arbitrary command execution with root privileges.

