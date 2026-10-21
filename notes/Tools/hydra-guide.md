### Tooling Guide: Hydra
## 1. Executive Summary
Hydra is a high-speed, parallelized network logon cracker. Unlike John the Ripper (which cracks password hashes offline), Hydra performs online brute-force attacks. It physically connects to a target's running service (like SSH, FTP, HTTP, or SMB), submits a username and password, evaluates the server's response, and repeats the process rapidly until it achieves a successful login.

## 2. Operational Mechanics
Online brute-forcing is inherently noisy and slow. Network protocols incorporate latency (like SSH's cryptographic handshake delay) to deter automated guessing.

Because Hydra interacts with live services, it relies on connection threads.

A thread is an independent connection.
If you use 1 thread, Hydra tries one password, waits for the server to say "Access Denied", and then tries the next.
If you use 4 threads, Hydra tries 4 passwords simultaneously.

Warning: Setting the thread count too high against fragile targets (like CTF boxes or older network switches) will overwhelm the service, causing it to crash or drop connections, which results in Hydra failing to find the password even if it is in the wordlist.
## 3. Core Execution Syntax
Single Known User (Optimized Attack)
If your reconnaissance (via enum4linux or web notes) has identified a specific target user, you should always restrict the attack to that single account to save time.

hydra -l jan -P /usr/share/wordlists/rockyou.txt ssh://<Target_IP>

-l jan: Specifies the single, known username (lowercase 'L').
-P: Specifies the path to the password dictionary list (uppercase 'P').
ssh://<Target_IP>: The protocol and target address. (Hydra supports ftp://, smb://, rdp://, etc.).
User List and Password List (Full Brute-Force)
If you do not know the exact username, you can feed Hydra a list of potential users.

hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ftp://<Target_IP>

-L users.txt: Specifies a file containing a list of usernames (uppercase 'L').
Note: This attack vector takes exponentially longer because it tests every password against User 1, then every password against User 2, etc.
Thread Optimization and Verbosity
hydra -l jan -P /usr/share/wordlists/rockyou.txt -t 4 -V ssh://<Target_IP>

-t 4: Limits the concurrent connections to 4 threads (safe for most CTF environments like Hack The Box or TryHackMe).
-V: Enables Verbose mode. Hydra will print every single username and password combination it attempts to the screen in real-time, allowing you to verify the attack is running correctly.

## 4. Professional Use Cases & Limitations
Web Form Cracking: Hydra can crack web-based login forms (like WordPress or custom admin portals) using the http-post-form module, though it requires specific syntax to map the username/password fields and the "failed login" error message.
Limitation: Online cracking is easily defeated by Account Lockout Policies (e.g., locking an account for 15 minutes after 5 failed attempts) or dynamic IP banning via Fail2Ban. This is why enumerating password policies via SMB before launching Hydra is a critical step in a professional methodology.

