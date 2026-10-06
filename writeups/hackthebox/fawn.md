**Fawn**

**step 1 :** establishing a line of sight \[ping -c 4 ip]
**step 2 :** network mapping (port discovery) \[nmap -sV ip], port \[21/tcp], service \[vsftpd 3.0.3], operating system unix

**step 3 :** vulnerability research, how to log in using ftp \[ftp -?] we are able to log in using the credential anonymous as default password

**step 4 : interaction,** \[ftp -a ip] enables anonymous login without credentials but we cannot read files so we transfer them to our host machie with the \[get file.txt] command to get the flag



**File transfer protocol** \[ftp]

found on port 21/tcp

FTP sends data in the clear, without any encryption. What acronym is used for a later protocol designed to provide similar functionality to FTP but securely, as an extension of the SSH protocol? \[SFTP] ssh file transfer protocol

to log in using ftp we use \[ftp -a ip] or \[ftp p] then type the login \[anonymous] as the default pass
for ftp we cannot read the contents of a file instead we download using the command get filename

