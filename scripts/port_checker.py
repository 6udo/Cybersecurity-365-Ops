#!/usr/bin/env python3
import socket

target_host = "scanme.nmap.org"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(2.0)

status = client.connect_ex((target_host, target_port))

if status == 0:
    print(f"[+] Success: Port {target_port} is OPEN!")
else:
    print(f"[+] Port {target_port} is CLOSED!")

client.close()

##!/usr/bin/env python3: This "shebang" tells your Linux system to run this file using Python 3.
#import socket: Brings in the networking toolkit.
#target_host & target_port: Our variables holding the destination coordinates.
#client = socket.socket(...): We create a new socket object. AF_INET means we are using an IPv4 address, and SOCK_STREAM means we are using a TCP connection (the 3-way handshake we just learned about)
#client.settimeout(2.0): Tells the script to wait a maximum of 2 seconds for a response.
#status = client.connect_ex(...): This is the core action. It attempts to connect to the target. If it succeeds, it returns a 0. If it fails, it returns an error code (like 111). We store that result in the status variable.
#if status == 0:: We check our variable. If it equals 0, we print a success message. else, we print that it is closed.
#client.close(): We close the connection to be polite to the server and free up resources on our machine.!