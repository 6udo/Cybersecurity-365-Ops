**Bounty Hacker**

**# TryHackMe: Bounty Hacker Write-up**

**\*\*Date:\*\* 2026-10-06**

**\*\*Platform:\*\* TryHackMe**

**\*\*Difficulty:\*\* Easy**

**\*\*Focus Area:\*\* Service Enumeration, Dictionary Attacks, and Sudo Privilege Escalation**



**## Objective**

**The goal of this machine is to chain an initial service misconfiguration (Anonymous FTP) into an intelligence-gathering phase, weaponize that intelligence via an online brute-force attack (SSH), and finally abuse a system binary misconfiguration (`sudo tar`) to achieve root-level privilege escalation.**



**---**



**## Phase 1: Reconnaissance**

**The engagement began with a standard Nmap service scan to map the exposed attack surface.**



**```bash**

**nmap -sC -sV <Target\_IP>**



**Results:**



**Port 21 (FTP): vsftpd 3.0.3. The Nmap default scripts (-sC) successfully identified that Anonymous FTP login is allowed.**



**Port 22 (SSH): OpenSSH 7.2p2.**



**Port 80 (HTTP): Apache httpd 2.4.18.**



**Phase 2: Initial Access \& Intelligence Gathering**

**Leveraging the open FTP port, an anonymous connection was established. The FTP server is an unencrypted text protocol, allowing a seamless bypass of authentication using the anonymous credential.**



**ftp <Target\_IP>**

**> Name: anonymous**

**> Password: \[Blank]
ftp -a <target\_ip> also works without needing credentials**



**Once inside the restricted FTP shell, directory enumeration revealed two files of interest. These were downloaded to the local attack machine using the get command:**



**1)task.txt: A text file containing operational notes, which revealed a valid system username: lin.**



**2)locks.txt: A custom text file containing a list of potential passwords.**



**Phase 3: Brute Force Attack**

With a confirmed username (lin) and a highly targeted custom dictionary (locks.txt), an online brute-force attack was launched against the SSH service (Port 22) using Hydra.



**bash**

hydra -l lin -P locks.txt ssh://<Target\_IP>



Hydra successfully cracked the authentication, revealing the password for user lin. This credential was used to establish a secure shell session and capture user.txt.



**Bash**

**ssh lin@<Target\_IP>**

**password from the hydra brute force \[RedDr4gonSynd1cat3]**

**cat user.txt**



**Phase 4: Privilege Escalation**

**After securing a foothold as a low-privileged user, internal enumeration commenced. Checking the user's sudo privileges is a critical first step to identifying local misconfigurations.**



**Bash**

**sudo -l**



**Output: (root) NOPASSWD: /bin/tar**



**The system administrator erroneously granted user lin the ability to run the tape archiver (tar) as root without requiring a password.**



**By referencing GTFOBins, a known bypass for tar was identified. The archiver contains a --checkpoint-action feature designed to execute commands when an archive reaches a specific size. By creating a junk archive and forcing this checkpoint immediately, tar can be tricked into spawning a system shell (/bin/sh). Because tar was executed with sudo, the resulting shell inherited root permissions.**



**The Exploit: sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh**



**Validation \& Capture: # whoami**

**root**

**# cat /root/root.txt**



**Key Takeaways**

**Never expose FTP with anonymous login unless explicitly hosting public-facing, non-sensitive data.**



**Custom wordlists are highly effective. Gathering OSINT directly from a target yields a vastly higher success rate than blindly spraying massive standard dictionaries (like rockyou.txt).**



**Strictly audit sudo permissions. System binaries with execution capabilities (like tar, find, or awk) should never be granted passwordless sudo execution for standard users.**



