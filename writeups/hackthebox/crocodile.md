# Hack The Box: Crocodile
**Tier:** 1 | **OS:** Linux | **Difficulty:** Very Easy | **Date:** October 2026

## 1. Executive Summary
Crocodile is a Tier 1 Linux machine that demonstrates the severe risks of leaving legacy services (FTP) exposed with anonymous access and failing to implement proper access controls on administrative web portals. The exploitation path involved exfiltrating sensitive credential files from an misconfigured FTP server and utilizing them to breach a hidden authentication endpoint discovered via directory brute-forcing.

## 2. Reconnaissance
Initial network enumeration was conducted using `nmap` to identify active services and operating system details.

```bash
nmap -sC -sV -p- -T4 <Target_IP>
```

| Port | State | Service | Version/Notes     |
| :--- | :---- | :----   | :----             |
| 21   |  Open | FTP     | vsftpd (anonymous)|
| 80   | Open  | HTTP    | Apache http2.4.41 |

## 3. Enumeration
**3.1 FTP Service (Port 21)**
The `nmap` scan indicated that Anonymous FTP login was permitted. An unauthenticated session was established to explore the file system.

```bash
ftp <Target_IP>
# Username: anonymous
# Password: <blank>
```
During the FTP session, two critical files were discovered and downloaded to the local attack machine using the `get` command:
`allowed.userlist`: Contained a list of valid administrative usernames.
`allowed.userlist.passwd`: Contained corresponding plaintext passwords.

**3.2 Web Application (Port 80)**
Navigating to the web server on Port 80 revealed a static HTML site. To uncover hidden infrastructure, a directory brute-force attack was executed using `gobuster`, specifically appending web-centric file extensions (`-x`).

```bash
gobuster dir -u http://<Target_IP> -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
```
**Key Finding:** The scan successfully identified a hidden administrative authentication endpoint at `http://<Target_IP>/login.php.`

## 4. Exploitation
With the hidden login portal identified and a valid set of credentials extracted from the FTP server, a credential stuffing attack was executed.

By inputting the administrative username and the highest-privileged password from the exfiltrated lists into `login.php`, the authentication controls were successfully bypassed.

## 5. Post-Exploitation
Authentication granted access to the Server Manager Dashboard. The root flag was prominently displayed within the administrative interface, confirming total compromise of the target application.

Vulnerabilities Exploited:

Insecure Default Configuration (CWE-1188): Anonymous read access enabled on the FTP server.

Information Exposure (CWE-200): Storing plaintext credentials in web-accessible or publicly readable directories.

Security Through Obscurity: Relying on unlinked directories (`/login.php`) rather than network-level access controls to protect administrative panels.
