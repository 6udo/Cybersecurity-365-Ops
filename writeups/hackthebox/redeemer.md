**Redeemer**



That is a perfect tactical decision. Knocking out Redeemer will officially complete the Tier 0 Starting Point path on Hack The Box, cleanly wrapping up your introduction to exposed databases before we pivot to TryHackMe.



Redeemer introduces you to Redis (Remote Dictionary Server). Unlike standard databases (like SQL) that write data to a hard drive, Redis stores data entirely in the system's RAM (memory). Because it is incredibly fast, developers use it to cache session tokens, temporary passwords, and high-speed background tasks.



Spin up the Redeemer machine to get your Target IP. Here is your execution plan:



Phase 1: Reconnaissance (Nmap)

Redis does not run on standard web or file-sharing ports. By default, it operates on Port 6379.



To verify the service is running and exposed, run your Nmap scan specifically targeting that port:



Bash

**nmap -sV -sC -p 6379 <Target\_IP>**

You should see the port reported as open and running a redis server.



**nmap**: The network mapper tool used to discover open ports.



**-sV (Service Versioning)**: Interrogates the open port to determine exactly what software and version is running (e.g., confirming it is Redis version 5.0.7).



**-sC (Default Scripts)**: Tells Nmap to run its library of basic security scripts against the port. For Redis, this script often checks if the database allows anonymous login without a password.



**-p 6379**: Restricts the scan strictly to port 6379 (the default port for Redis). Scanning just one port takes a fraction of a second, whereas scanning all 65,535 ports takes minutes.



Phase 2: The Attack (Redis-CLI)

To interact with a Redis server, we don't use Netcat or a web browser. We use the dedicated command-line interface tool.



If your Kali Linux environment doesn't have it installed out of the box, you can grab it quickly by running: sudo apt install redis-tools.



Connect to the target database:



Bash

**redis-cli -h <Target\_IP>**

(Notice we don't provide a username or password. Just like the previous legacy protocols, this server is misconfigured to allow anonymous access).



**redis-cli**: The specific command-line tool built to interact with Redis databases (just like smbclient is for SMB or ftp is for FTP).



**-h (Host)**: Tells the tool that you want to connect to a remote server instead of a database on your local Kali machine. You follow this flag with the target IP address.



Phase 3: Enumeration and Capture

If the connection is successful, your prompt will change to <Target\_IP>:6379>. You are now inside the database memory.



1\. Gather Intelligence:

Type **info** and press Enter. This dumps all the server statistics. Scroll down to the very bottom to the # Keyspace section. You will see a line like db0:keys=4,expires=0. This tells you Database 0 exists and contains four pieces of data.



**info**



Once inside the database, this command asks the server to dump all of its internal statistics. It shows memory usage, connected clients, CPU load, and most importantly, the Keyspace section at the bottom, which reveals how many databases exist and how much data is in them.



2\. Select the Database:

Tell Redis you want to interact with Database 0:



Bash

select 0

3\. List the Keys:

In Redis, data is stored as key-value pairs (like a dictionary). You need to see the names of the keys stored in this database. Ask it to list everything:



select 0



Redis does not name its databases (like "HR\_Data" or "Sales"). It just numbers them: 0, 1, 2, 3, etc. The select command tells the server which database index you want to actively look at. select 0 switches you to the very first database.



Bash

keys \*

You will see a list of four keys. One of them will look suspiciously like a flag.



**keys \***



**keys**: The command to list the names of the data points (keys) stored in the current database.



**\* (Wildcard)**: In Linux and databases, the asterisk means "everything." You are asking the database to list every single key it contains.



**4. Dump the Data:**

Once you spot the name of the key containing the flag (e.g., flag or flag.txt), use the get command to read the value stored inside it:



**Bash**

**get <name\_of\_flag\_key>**

Copy the flag, type exit to drop back to your Kali terminal, and submit it to the platform!



**Real-World Application: In-Memory Data Leaks and RCE**

Redis is strictly designed to be an internal tool, hidden deep behind firewalls so only local web servers can talk to it. It has zero built-in security or encryption by default because it prioritizes raw speed.



However, developers frequently make mistakes in their Docker or cloud configurations, accidentally exposing Port 6379 to the public internet.



When a penetration tester finds an exposed Redis server, it is a goldmine. Because Redis caches active web sessions, the attacker can use the keys \* and get commands to steal live session cookies from legitimate users, allowing the attacker to hijack administrator accounts on the company's main website without ever knowing a password.



Furthermore, if the Redis server is running with root privileges, advanced attackers can actually use Redis to maliciously write an SSH Public Key directly into the server's authorized\_keys file, instantly granting the attacker a permanent root SSH shell.



