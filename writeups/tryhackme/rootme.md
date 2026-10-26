**TryHackMe Write-up: RootMe**



**1. Executive Summary**

\-Target: TryHackMe: RootMe

\-OS: Linux

\-Vulnerabilities: Unrestricted File Upload (Extension Filter Bypass), SUID Misconfiguration

\-Objective: Obtain initial access via web shell and escalate privileges to root.



**2. Reconnaissance**

*Nmap Port Scan:*

Identified open ports for SSH (22) and HTTP (80).

\[nmap -sV -sC <Target\_IP>]



*Directory Busting (Gobuster):*

Brute-forced the web server using ***common.txt*** to uncover hidden directories.

\[gobuster dir -u http://<Target\_IP> -w /usr/share/wordlists/dirb/common.txt]

Discovered Directories: \[/panel] (Upload form) and \[/uploads] (Storage).



**3. Initial Foothold**

*Vulnerability: Unrestricted File Upload.*

The \[/panel] directory contained an upload form. The server blocked standard \[.php] extensions but failed to sanitize alternative PHP extensions. 



**Execution:**

1\. Copied the standard \[php-reverse-shell.php] payload from the Kali \[webshells] directory.

*\[locate php-reverse-shell.php]*

*\[cp filepath revshell.php]*

2\. Modified the payload to point back to the local Kali VPN IP on port 4444.

*\[nano revshell.php] \[modified ip and port:4444]*

3\. Renamed the file to \[revshell.phtml] to bypass the \[.php] filter.

4\. Uploaded the payload and started a Netcat listener *(nc -lvnp 4444)*.

5\. Navigated to \[/uploads/revshell.phtml] to execute the script and catch the reverse shell as \[www-data].

6\. Captured the \[user.txt flag.]

*\[find / -type f -name user.txt] \[cat filepath/user.txt]*



**4. Privilege Escalation**

*Vulnerability: SUID Misconfiguration.*

Searched for files with the SUID bit set to identify potential privilege escalation vectors.

*\[find / -type f -user root -perm -4000 2>/dev/null]*



**Execution:**

1\. Identified \[/usr/bin/python] in the SUID list, which is highly abnormal.

2\. Leveraged GTFOBins techniques to abuse the Python SUID binary.

3\. Executed the privilege escalation command:

&#x20;  *\[python -c 'import os; os.execl("/bin/sh", "sh", "-p")']*

4\. Gained \[root] shell and captured \[root.txt].

*\[find / -type f -name root.txt] \[cat filepath/root.txt]*



We know /usr/bin/python is an anomaly through basic system context, not because its permissions look different than other SUID files. Standard Linux operating systems only apply the SUID bit to programs that legitimately require temporary root access to function for standard users.



Normal SUID: /usr/bin/passwd (Needs root to write your new password to the deeply protected /etc/shadow file).



Normal SUID: /usr/bin/ping (Needs root to open raw network sockets).



Anomaly: /usr/bin/python is an open-ended programming language interpreter. It never requires root privileges to run standard scripts. Seeing the SUID bit on Python, Bash, Netcat, or Vim means an administrator either made a massive configuration error or deliberately left a backdoor for themselves.



The Python Payload Breakdown



The command *\[python -c 'import os; os.execl("/bin/sh", "sh", "-p")']* forces the SUID Python binary to replace itself with a root-level command prompt.



Here is the exact mechanical sequence:



python -c: The -c (command) flag tells Python to execute the text string immediately following it as code, rather than looking for a .py script file on the hard drive.



import os;: Imports the Python Operating System library, giving the script permission to interact directly with the Linux kernel and execute system-level commands.



os.execl(...): The "execute and leave" function. It tells the system to completely replace the currently running Python process with a brand new process.



"/bin/sh", "sh": Specifies that the new process to launch is the Bourne Shell (your command prompt).



"-p": This is the privilege flag. By default, many modern shells will notice they are being run by a low-level user (like www-data) and automatically drop any root SUID privileges as a safety measure. The -p (privileged) flag explicitly overrides this safety feature, forcing the new shell to retain the root permissions granted by the SUID bit.



**5. Lessons Learned / Remediation**

\- \*\*Validation Bypass:\*\* Never rely solely on blocking specific file extensions (like `.php`). Use an explicit whitelist of allowed extensions (e.g., `.jpg`, `.png`) and validate file contents.

\- \*\*Least Privilege:\*\* Web application upload directories should never have execute permissions.

\- \*\*SUID Hardening:\*\* Standard application binaries like Python should never have the SUID bit set, as it allows arbitrary command execution with root privileges.
