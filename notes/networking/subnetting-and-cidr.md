An IPv4 address is a 32-bit binary sequence divided into four 8-bit octets, acting as both a street name (the network) and a house number (the host). When operating in a SOC or during a penetration test, the subnet mask is your tactical map—it dictates exactly how large the target environment is, where the routing boundaries lie, and which IP addresses are valid for lateral movement.

# Subnetting & CIDR Core Theory
**Classless Inter-Domain Routing (CIDR) notation**
it is a short hand that counts the number of locked `Network` bits from left to right. the remaining bits are unlocked `hosts` bits used to assign IP addresses to actual machines 
## The 4 pillars of every Subnet
**Network Address** The mathematical base of the subnet. It represents the network itself and cannot be assigned to a device.
First Usable Host: Network Address + 1. Usually assigned to the default gateway (router).
Last Usable Host: Broadcast Address - 1. The absolute highest IP you can ping or exploit in this block.
Broadcast Address: The mathematical ceiling. Packets sent here are replicated and blasted to every machine on the subnet. Cannot be assigned to a device.

## Rapid Block Size Calculation (The Hacker's Method)
Instead of writing out 32 bits of binary, field operators use the "Block Size" or "Magic Number" method.
1- Identify the custom subnet mask decimal value.
2- Subtract that value from 256.
3- The result is your block size (how much each subnet   increments by).