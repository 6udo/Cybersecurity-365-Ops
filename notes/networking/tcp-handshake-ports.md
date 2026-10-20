# NETWORKING LAYER MECHANICS
# TCP Handshake & Scanning under the Hood
#when 2 computers communicate over TCP the OS must track state. Web browsers do not send packets directly to the network wire the kernel instead creates a machine called a Transmission Control Block (TCB)

# TCP 3 WAY HANDSHAKE AND PORTS
Port 21(FTP)File Transfer Protocol - Often misconfigured to allow "Anonymous" access
Port 22(SSH)Secure Shell - Secure command line access
Port 80(HTTP) unsecure web server
Port 443(HTTPS) secure web servers
Port 445(SMB)Server message board - Windows/Linux file sharing and network administration

When you connect to these ports using the Transmission Control Protocol (TCP), the devices must perform a signaling phase to synchronize their timers and sequence numbers before a single byte of application data (like a webpage) is sent. This is the 3-Way Handshake:

SYN (Synchronize): Your Kali machine sends a packet to the target port with the SYN flag enabled. This translates to: "I want to open a connection. My starting sequence number is 1000."

SYN-ACK (Synchronize-Acknowledge): If the port is open and a service is listening, the target server replies with both SYN and ACK flags. "I acknowledge your 1000 (here is 1001). I am ready to talk, and my starting sequence number is 5000."

ACK (Acknowledge): Your Kali machine sends a final packet. "I acknowledge your 5000 (here is 5001). Connection established."

If you send a SYN packet to a port where no service is running (a closed port), the target server immediately replies with an RST (Reset) flag. "No one lives in this apartment. Drop the connection."
    
    