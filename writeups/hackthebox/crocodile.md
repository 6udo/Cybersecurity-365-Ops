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

# 3. Enumeration
## 3.1 FTP Service (Port 21)
The `nmap` scan indicated that Anonymous FTP login was permitted. An unauthenticated session was established to explore the file system.

```bash
ftp <Target_IP>
# Username: anonymous
# Password: <blank>
```
