**-Level 10-11 -** the data.txt is base64 encoded

&#x20;             Base64 is a translation mechanism, not an encryption protocol. It

&#x20;             takes raw binary data (which might contain unprintable characters

&#x20;             that break text-based systems like email or HTTP) and translates

&#x20;             it into a safe alphabet of 64 characters: A-Z, a-z, 0-9, +, and

&#x20;             /. It is purely used to safely transport data, offering zero

&#x20;             security. You can easily spot Base64 because it often ends with

&#x20;             one or two equal signs (= or ==), which are used as "padding" to

&#x20;             make the data fit the correct size.
command used \[base64 -d data.txt] he base64 utility is built into

&#x20;             Linux for this exact purpose. By passing the -d (decode) flag and

&#x20;             pointing it at data.txt, the command reads the obfuscated string,

&#x20;             translates it back into its original ASCII format, and prints the

&#x20;             plaintext password to your terminal.
another way to solve \[cat data.txt | base64 -d]
**-Level 11-12** - ROT13 (Rotate by 13 places) is a simple substitution cipher. It

&#x20;              replaces a letter with the 13th letter after it in the alphabet

&#x20;              (A becomes N, B becomes O, etc.). Because the English alphabet

&#x20;              has 26 letters, ROT13 is symmetric—if you rotate a letter 13

&#x20;              spaces, and then 13 spaces again, you end up exactly where you

&#x20;              started. It was popular in early internet forums to hide movie

&#x20;              spoilers, but it is cryptographically worthless.
**-Level 12-13 -** 

Concept Required: Magic Numbers, Hexdumps, and File Archives/Compression.



**What are these and what do they do?**



Hexdump: A hexadecimal (base-16) representation of a binary file. It allows humans to read raw computer bytes on a screen.



Magic Numbers: Linux does not care if a file is named picture.jpg or document.pdf. It identifies files by reading their "Magic Number"—the first few bytes of the file which contain a hidden signature.



Compression vs. Archiving: tar (Tape Archive) bundles multiple files together without shrinking them. gzip and bzip2 are mathematical algorithms that find repeated patterns in data to shrink the file size.
**The command(s) to solve the level:**



\[mkdir /tmp/myworkspace123 \&\& cp data.txt /tmp/myworkspace123/ \&\& cd /tmp/myworkspace123/]



\[xxd -r data.txt > output.bin]



The loop: file output.bin, then rename based on the output (mv output.bin output.gz), then decompress (gzip -d output.gz). Repeat.



**Explanation of what the command does:**

You first create a sterile workspace in /tmp because you cannot write files in the home directory. The xxd -r command takes the hex text and reverses it back into raw binary (output.bin). From there, the file command reads the magic numbers to tell you what the file actually is. You use mv to give it the proper extension so the decompression tools (gzip, bzip2, tar) accept it and strip away the layer.



**Level 13-14 (SSH Private Keys)**

Concept Required: Asymmetric Cryptography (Public Key Infrastructure).



**What is it and what does it do?**

Passwords are "symmetric"—both you and the server must know the same secret. If the server is hacked, your password is stolen. Asymmetric cryptography fixes this by generating a mathematically linked pair of keys.



Public Key: Given to the server. It acts like a padlock. Anyone can lock it, but no one can unlock it.



Private Key: Stays strictly on your machine. It is the only thing that can unlock the padlock.



**The command to solve the level:**

ssh -i sshkey.private bandit14@localhost -p 2220



**Explanation of what the command does:**

You are running an SSH command while already inside the SSH server to log in as the next user on the same machine (localhost). The -i (Identity) flag points the SSH client directly to your private key file. The server challenges you, your private key mathematically proves you are the owner without ever leaving your machine, and you are logged in without typing a password.

**Update** : this method although could work was removed from the overthewire servers to solve it you will need to cat sshkey.private , copy the contents from \[-- BEGIN RSA to KEY----] and exit the server and paste the contents to a new file \[bandit14.key] \[you can use nano or a text editor you prefer, ctrl+o enter , then ctrl+X] once you have copied the contents change the permissions to prevent errors preferrably only user read and write that is \[chmod 600 bandit14.key] then log in to bandit14 using the command \[ssh -i bandit14.key bandit14@bandit.labs.overthewire.org -p 2220] it will not require a password



**Level 14-15 (Raw Network Sockets)**

Concept Required: TCP/IP Sockets, Ports, and Client/Server Communication.



**What is a socket/port and what does it do?**

An IP address directs network traffic to a specific computer. A Port (a number between 0 and 65535) directs that traffic to a specific application running on that computer. Think of the IP address as an apartment building, and the Port as the specific apartment number.



A "socket" is the software pipe that connects your terminal directly to that door. In this level, a background program (a daemon) is sitting inside apartment 30000, waiting for someone to slide the current password under the door. If the password is correct, it slides the Level 15 password back out.



**The command to solve the level:**

echo "paste\_your\_bandit14\_password\_here" | nc localhost 30000



**Explanation of what the command does:**



**echo**: Simply prints your password text.



**|** (Pipe): Instead of printing the password to your screen, it forces the text into the next command.



**nc (Netcat)**: Known as the "Swiss Army Knife" of networking, Netcat reads and writes raw data across network connections.



**localhost:** This is a special loopback address (127.0.0.1). It tells the network card, "Do not go out to the internet; route this connection right back into my own machine."



**30000:** The specific port Netcat is connecting to.



Altogether, the command instantly opens a raw network pipe to the local application, shoves your password through it, reads the response (the Level 15 password), prints it to your screen, and closes the connection.



**Other ways we can solve the level:**



Interactive Netcat: You can run it manually by typing nc localhost 30000 and hitting Enter. The terminal will seem to freeze. It is actually waiting for your input. Paste your password, hit Enter, and it will spit the next password back.



Telnet: Telnet does the exact same thing for unencrypted connections: telnet localhost 30000.



Bash Pseudo-devices: You can actually bypass tools entirely and use Linux's built-in file system routing: echo "\[password]" > /dev/tcp/localhost/30000



**Level 15-16 (TLS/SSL Encrypted Sockets)**

Concept Required: Transport Layer Security (TLS/SSL) and Cryptographic Handshakes.



**What is TLS and what does it do?**

When you used Netcat in the previous level, your password was sent in plain text. If a hacker was intercepting your network traffic (using a tool like Wireshark), they would have seen your password clearly.



TLS (Transport Layer Security) fixes this by wrapping your network socket in an armored, encrypted tunnel. Before any actual data (like your password) is allowed to be transmitted, your computer and the server perform a complex "Handshake." They verify each other's digital certificates and mathematically agree on a temporary, symmetric encryption key. Once the handshake is complete, everything sent through the port is scrambled into unreadable ciphertext to anyone listening on the outside.



**The command to solve the level:**

\[openssl s\_client -connect localhost:30001 -ign\_eof]



Note: When you press Enter, your screen will flood with a massive wall of text detailing the digital certificate and handshake process. Wait for it to stop, paste your Level 15 password, and hit Enter again.



**Explanation of what the command does:**

Because Port 30001 demands encryption, standard Netcat will immediately fail and disconnect.



**openssl**: The premier cryptography toolkit in Linux.



**s\_client**: This module tells OpenSSL to act as a generic SSL/TLS client (like a secure version of Netcat).



**-connect localhost:30001**: Specifies the target IP and port.



**-ign\_eof (Ignore End of File)**: This is the critical flag. When you paste text and hit Enter, Linux sometimes sends an invisible EOF (End of File) signal. OpenSSL is programmed to immediately tear down the encrypted tunnel the millisecond it sees EOF. The -ign\_eof flag forces OpenSSL to keep the tunnel open, giving the Bandit application enough time to verify your password and send the Level 16 password back to you.



**Other ways we can solve the level:**



**Ncat (Advanced Netcat)**: The developers of Nmap created an upgraded version of Netcat that supports SSL natively. You can solve the level with a single pipeline: echo "\[password]" | ncat --ssl localhost 30001.



**Socat**: Another highly advanced socket tool that can handle encryption: socat - OPENSSL:localhost:30001,verify=0

