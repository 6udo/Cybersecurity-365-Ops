# NETWORKING LAYER MECHANICS
# TCP Handshake & Scanning under the Hood
#when 2 computers communicate over TCP the OS must track state. Web browsers do not send packets directly to the network wire the kernel instead creates a machine called a Transmission Control Block (TCB)

Client Kernel                                Server kernel   
[Closed]                                      [Listen]
    |                                              |
    | -----Segment 1: SYN (Seq=1000, Ack=0)------> |(Allocates SYN Queue memory)
    |
    
    