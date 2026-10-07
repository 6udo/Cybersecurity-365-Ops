**Level 16-17**



To conquer this level, we must combine the port scanning skills you used on Hack The Box with the OpenSSL skills from Bandit 15.



Instead of guessing which port to connect to, you will programmatically scan the system to identify active services, filter out the decoys, and extract a cryptographic key to gain access to the next level.



**Phase 1: Reconnaissance (Nmap)**

You know the target is on localhost (the machine you are currently logged into) somewhere between ports 31000 and 32000. You need to find which ports are open and which ones speak SSL.



Run this command in your Bandit 16 terminal:

\[nmap -sV -p 31000-32000 localhost]



**Explanation:**



**\[-p 31000-32000]**: Restricts Nmap to only scan this specific 1,000-port block, speeding up the scan immensely.



**\[-sV] (Service Versioning)**: This is the critical flag. Instead of just telling you a port is "open," Nmap will aggressively interact with the port to figure out exactly what software is running on it.



The output will list a few open ports (usually 31046, 31518, 31691, 31790, and 31960). Notice the service names. Most are labeled echo (meaning they just bounce your text back to you). You are looking for the port running an unrecognized SSL service—typically 31790.



**Phase 2: The Attack (OpenSSL)**

Now that you have isolated the correct port, establish the encrypted tunnel.



**Run the command:**

**\[openssl s\_client -connect localhost:31790]**



Once the SSL certificate data scrolls past and the connection holds open, paste your Bandit 16 password and press Enter.



**Phase 3: The Capture (SSH Private Keys)**

The server will not reply with a standard password string. It will output a massive block of text starting with \[-----BEGIN RSA PRIVATE KEY-----].



This is an SSH Private Key. It is a cryptographic file that proves your identity to a server, completely replacing the need for a typed password.



To use it, you must save it to a file and lock down its permissions:



Copy the entire block of text, exactly from the -----BEGIN line down to the -----END line.



Create a temporary workspace you own: \[mkdir /tmp/b17ops \&\& cd /tmp/b17ops]



Create a new file: \[nano sshkey.private]



Paste the key into the file, press Ctrl+O to save, Enter to confirm, and Ctrl+X to exit.



Lock the permissions: chmod 600 sshkey.private (If you do not do this, SSH will throw a security error and refuse to use the key because it is readable by other users on the system).



Log into Level 17: \[ssh -i sshkey.private bandit17@localhost -p 2220]



Note: The -i flag stands for "identity file." It tells the SSH client to use your file for authentication instead of asking for a password.



**Update** : we are not able to ssh to level 17 while in level 16 so we take the key exit the server create a new file, change permissions to user owner only \[chmod 600 .file] then procced to ssh to bandit 17 \[ssh -i examplekey.private bandit17@bandit.labs.overthewire.org -p 2220] no password is required proceed to root \[cd /etc/bandit\_pass , cat bandit17 ] copy the password then save it to log in later



**Real-World Application: Hidden Services \& Identity Theft**

In corporate networks, developers frequently spin up temporary internal services on high, non-standard ports (like 31000+) for debugging, and simply forget to shut them down. Because these ports are obscure, network administrators miss them. A penetration tester will use nmap -sV -p- (scanning all 65,535 ports) to find these forgotten "shadow IT" services.



Furthermore, discovering an exposed SSH Private Key is a critical severity finding. If a hacker finds a private key (perhaps accidentally left in a public GitHub repository, an exposed web directory, or an unprotected FTP server), they can bypass password authentication entirely. Password policies (like requiring 16 characters and special symbols) become useless. The hacker can silently log into the network as the administrator, leaving zero "failed password" logs for the security team to detect.



**Bandit 17-18**



The objective for Bandit Level 17 to 18 is all about identifying deviations from a known baseline.



Here is the exact prompt from the platform:



There are 2 files in the homedirectory: passwords.old and passwords.new. The password for the next level is in passwords.new and is the only line that has been changed between passwords.old and passwords.new.



If you run ls -la, you will see both of those files. If you look at their sizes, you will see they are exactly the same size (3,300 bytes) and contain hundreds of identical lines. Finding the single changed line manually by reading them would be a nightmare.



Instead, you are going to use the core Linux comparison tool.



The Execution Sequence

1\. Compare the Files:

Run the diff command. The order you place the files matters—always put the "old" (baseline) file first, and the "new" (changed) file second.



**Bash**

**\[diff passwords.old passwords.new]**



2\. Read the Output:

The terminal will output three lines that look something like this:



Plaintext

42c42

< \[some\_random\_string]

\---

> \\\[another\\\_random\\\_string]

How to interpret this:



42c42: Tells you that line 42 changed.



< (Left Arrow): This is the line from the first file you typed (passwords.old). This is the old password.



> (Right Arrow): This is the line from the second file you typed (passwords.new). This is your flag for Bandit 18.



Copy the string next to the > arrow, log out of Bandit 17, and log into Bandit 18!



**Real-World Application: Configuration Auditing \& Incident Response**

The concept of "diffing" a current state against a known-good baseline is one of the most fundamental techniques in cybersecurity.



Imagine you are a security analyst for a bank. You have a massive, 5,000-line firewall configuration file. One night, a junior administrator accidentally changes a single line, accidentally exposing an internal database to the public internet. Or worse, a hacker silently sneaks in and adds a single backdoor rule.



You cannot read 5,000 lines of code every morning to check for errors. Instead, you run a script that diffs the live firewall configuration against a secure backup from the day before. The tool will instantly highlight the exact line the hacker added (labeled with a >), allowing you to instantly spot the backdoor and delete it. This is the foundation of automated Change Management and File Integrity Monitoring (FIM).



**Bandit 18-19**



The objective for Bandit Level 18 to 19 introduces a hostile environment. You are going to encounter your first "booby trap."



Here is the prompt from the platform:



The password for the next level is stored in a file readme in the homedirectory. Unfortunately, someone has modified .bashrc to log you out when you log in with SSH.



If you try to log in normally with ssh bandit18@..., you will authenticate successfully, but the server will instantly print "Byebye!" and terminate your connection. You never even get a prompt.



**The Problem: The .bashrc Trap**

When you log into a Linux machine interactively, the system automatically runs a hidden configuration script in your home directory called .bashrc. It is usually used to set up colors and aliases. However, in this level, the administrator (or a malicious actor) has added an exit command inside that script. The moment the system tries to load your terminal, the script fires and kicks you out.



**The Execution Sequence (The Bypass)**

To bypass this trap, you need to tell the SSH client to execute a specific command instead of loading a full, interactive terminal. If you don't ask for a full terminal, the .bashrc script never triggers.



Run this command from your local Kali machine:



Bash

**\[ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme]**

(When prompted, paste the password you found using diff in Level 17).



**Explanation of the bypass:**

By appending cat readme to the very end of your SSH string, you are changing the behavior of the protocol. SSH will connect, authenticate, execute only that single command, print the output (the password for Level 19) directly to your Kali terminal, and then gracefully close the connection.



**Real-World Application: Automation and Restricted Shells**

This concept of "remote command execution over SSH" is heavily used by both system administrators and attackers.



For Administrators (DevOps): Tools like Ansible use this exact mechanism to manage enterprise networks. If a SysAdmin needs to check the disk space on 5,000 servers, they don't log into each one interactively. They write a script that loops through the IP addresses and runs ssh admin@server df -h. The command executes invisibly in the background and returns the data.



\*\*For Attackers (Bypassing Restricted Shells): Sometimes, a company will give a contractor SSH access, but they will lock them into a "Restricted Shell" (like rbash) that prevents them from running certain commands or changing directories. Attackers frequently bypass these restrictions by executing the command directly through the SSH connection string, bypassing the restricted environment entirely.

Bandit 19-20\*\*



**Bandit 19-20**



The objective for Bandit Level 19 to 20 introduces one of the most critical concepts in Linux privilege escalation: SUID Binaries.



Here is the prompt from the platform:



To gain access to the next level, you should use the setuid binary in the homedirectory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit\_pass), after you have used the setuid binary.



**The Concept: Set User ID (SUID)**

Normally in Linux, when you execute a program, that program runs with your permissions. If you run a script, it can only access files you are allowed to access.



However, administrators can apply a special permission flag to a binary called SUID (Set Owner User ID). When a file has the SUID bit set, it executes with the privileges of the owner of the file, regardless of who is actually running it. This is useful for things like the passwd command, which allows a normal user to change their password (which requires writing to a deeply protected root file).



In this level, there is a custom binary designed to run commands as bandit20.



**The Execution Sequence**

**1. Identify the SUID Binary:**

Log into Bandit 19. Once inside, list the files with detailed permissions:



Bash

ls -la

You will see a file named bandit20-do. Look closely at its permissions: -rwsr-x---.

Notice that s where the x normally is. That s indicates the SUID bit is active. You will also see the owner of the file is bandit20.



**2. Understand the Tool:**

Run the binary with no arguments to see how it works, as the prompt suggested:



Bash

**./bandit20-do**

Output: Run a command as another user. Example: **./bandit20-do id**



**3. Execute the Exploit:**

Because this binary temporarily grants you the powers of bandit20, you can use it to read a file that your current user (bandit19) is strictly forbidden from viewing.



Run this command:



Bash

**\[./bandit20-do cat /etc/bandit\_pass/bandit20]**

The binary will elevate its privileges to bandit20, read the password file, and print the flag to your terminal. Copy that password, log out, and log into Bandit 20!



**Real-World Application: SUID Privilege Escalation**

You actually just utilized this concept in the real world when you rooted the TryHackMe: Bounty Hacker machine yesterday.



While Bounty Hacker relied on sudo (which uses a configuration file to grant permissions), SUID is baked directly into the file's permissions on the hard drive.



In corporate environments, System Administrators frequently write custom C programs or bash scripts to allow lower-level IT helpdesk staff to perform a specific restricted action (like restarting a web server or clearing a cache) without giving them full root access. They compile the tool and add the SUID bit.



If the administrator writes that code poorly—perhaps it allows the helpdesk user to input a file path without sanitizing it, or it calls a system command without absolute paths—a penetration tester will hijack that SUID binary. Just like you did with the tar command via GTFOBins, the attacker forces the poorly written SUID binary to execute /bin/sh. Because the binary is owned by root and has the SUID bit set, the resulting shell instantly drops them into a root prompt, taking full control of the server.



**Bandit 20-21**



The objective for Bandit Level 20 to 21 introduces port binding and network listeners. You are going to act as the server, and force the target binary to connect to you.



Here is the prompt from the platform:



There is a setuid binary in the homedirectory that does the following: it makes a connection to localhost on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).



**The Concept: Reverse Connections \& Netcat Listeners**

Up until now, you have always used Netcat or OpenSSL as a client to connect to a remote server. In this level, you must use Netcat to create a server. You will open a network port on the machine, wait for the SUID binary to connect to it, send it the current password, and receive the flag.



Because a listener blocks your terminal while it waits for a connection, the easiest way to execute this attack is using two separate terminal windows.



**The Execution Sequence**

**1. Set Up the Listener (Terminal A)**

Open a second terminal window on your Kali machine and establish a second SSH connection to Bandit 20.

In this new window, tell Netcat to listen (-l) on a specific port (let's use 4444) for incoming connections:



Bash

**\[nc -l -p 4444]**

Your terminal will appear to freeze. It is now actively listening on Port 4444.



**2. Trigger the SUID Binary (Terminal B)**

Go back to your original terminal window (already logged into Bandit 20).

Look at the files in your directory (ls -la) and you will see the SUID binary suconnect. Execute it and tell it to connect to your listening port:



Bash

**\[./suconnect 4444]**

**3. Execute the Trade (Terminal A)**

The moment you run the binary in Terminal B, switch your eyes back to Terminal A. The connection has been established.

Paste your Bandit 20 password into Terminal A and press Enter.



The binary on the other side of the connection will verify the password, and instantly print the Bandit 21 password back into your Netcat listener!



Copy that new password, close both SSH sessions, and log into Bandit 21.



Real-World Application: Bind Shells and Command \& Control (C2)

This dynamic—setting up a listener and waiting for a system to connect—is the fundamental mechanic of remote malware administration.



When you get a victim to click a malicious link or execute a payload (like the tar exploit you used yesterday), you rarely have direct access to their network because of corporate firewalls. Firewalls block incoming traffic, but they almost always allow outgoing traffic (so employees can browse the web).



Attackers bypass firewalls using Reverse Shells. They set up a Netcat listener on their own Kali machine (just like you did in Terminal A). When the victim clicks the malware, the payload executes a script (like suconnect in Terminal B) that silently reaches out across the internet and connects back to the attacker's listener. The attacker now has a live command prompt on the victim's machine, bypassing the firewall entirely.



