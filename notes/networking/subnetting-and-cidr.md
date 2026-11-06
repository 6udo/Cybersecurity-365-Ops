An IPv4 address is a 32-bit binary sequence divided into four 8-bit octets, acting as both a street name (the network) and a house number (the host). When operating in a SOC or during a penetration test, the subnet mask is your tactical map—it dictates exactly how large the target environment is, where the routing boundaries lie, and which IP addresses are valid for lateral movement.

# Subnetting & CIDR Core Theory
**Classless Inter-Domain Routing (CIDR) notation**
it is a short hand that counts the number of locked `Network` bits from left to right. the remaining bits are unlocked `hosts` bits used to assign IP addresses to actual machines 
## The 4 pillars of every Subnet
**Network Address** The mathematical base of the subnet. It represents the network itself and cannot be assigned to a device.
This is the absolute bottom number of any block. It identifies the entire network to the outside world. If a router outside the network wants to send traffic to the community, it sends it to this "Street Sign."
`Why you can't use it:` You cannot assign the Network Address to a laptop or a server because it represents the whole street, not a specific house.

**First Usable Host:** Network Address + 1. Usually assigned to the default gateway (router).

**Last Usable Host:** Broadcast Address - 1. The absolute highest IP you can ping or exploit in this block.

**Broadcast Address:** The mathematical ceiling. Packets sent here are replicated and blasted to every machine on the subnet. Cannot be assigned to a device.
This is the absolute top number of any block. If you send a single packet to this address, the switch will duplicate that packet and blast it to every single machine inside the gated community simultaneously.
`Why you can't use it:` If you assigned this IP to a printer, every time the network sent out a broadcast check, the printer would crash from the traffic. It is reserved purely for network-wide shouting.

**Usable hosts per block** If you have a `/26` subnet, your block size is `64` total addresses. But you are not allowed to assign the `Network Address` (the bottom) or the `Broadcast Address` (the top) to a computer.

The Formula: `Block Size - 2 = Usable Hosts.`

Out of 64 total IPs, you can only assign 62 of them to actual laptops, servers, or phones. Those 62 IPs are your `usable hosts.`

## Rapid Block Size Calculation (The Hacker's Method)
Instead of writing out 32 bits of binary, field operators use the "Block Size" or "Magic Number" method.
1- Identify the custom subnet mask decimal value.
2- Subtract that value from 256.
3- The result is your block size (how much each subnet   increments by).

**Common Penetration Testing CIDRs:**
`/24` **(The Standard LAN):** `.0`
-Mask: `255.255.255.0`
-Math: 8 host bits available ($2^8 = 256$).
-Result: `256` total IPs, `254` usable hosts. The network increments by 1 in the third octet.
`/26` **(The Segmented Dept):** `.192`
Mask: `255.255.255.192`
Math: $256 - 192 = 64$.
Result: Subnets increment in blocks of 64 (`.0`, `.64`, `.128`, `.192`). 62 usable hosts per block.
`/28` **(The Hardened DMZ):** `.240`
Mask: `255.255.255.240`
Math: $256 - 240 = 16$.
Result: Subnets increment in blocks of 16 (.0, .16, .32, .48, etc.). 14 usable hosts per block.

# Subnetting Drill
To verify your theoretical grasp before we move to scripting, calculate the four pillars for the following operational scenarios without using `ipcalc` or online calculators.

**Scenario A: Triage**
Your SIEM flags an outbound beacon from a workstation. The IP is `192.168.15.0/24`.
1. What is the First Usable Host?
<details>
<answer> Click to reveal </answer>
/24 masks to `255.255.255.0`
$256 - 0 = 256$ but 256 is not used range is 0 - 255
.0 - .256 is the only block  making the Network address .0 and thus the first usable host .1 
answer = 192.168.15.1
</details>

2. What is the Broadcast Address?
<details>
<answer> Click to reveal </answer>
broadcast address is the absolute maximum volume of the block which is .255 
answer = 192.168.15.255
</details>

**Scenario B: The Red Team Pivot**
You compromise a dual-homed server on a corporate network. You run ip a and discover an internal interface with the IP 10.0.5.100/26. You need to map this segmented department.
3. What is the Block Size of this subnet?
<details>
<answer> Click to reveal </answer>
/26 translates to the mask `255.255.255.192`
thus the block size will be $256 - 192 = 64$ that is `.0` `.64` `.128` and has 62 possible hosts
answer = 64 
</details>

4. What is the Network Address (the base of this specific block)?
<details>
<answer> Click to reveal </answer>
ip = `10.0.5.100` 
block is `.64` because the next block starts at `.128`
so the network address is `10.0.5.64`
</details>

5. What is the Last Usable Host?
<details>
<answer> Click to reveal </answer>
last usable host is the broadcast address -1 
the block is `.64` ending at `.127`
answer = `10.0.5.126`
</details>

**Scenario C: Bespoke Client Architecture**
You are designing a highly restrictive security enclave for a high-net-worth individual's family office. The firewall interface is placed at 172.16.2.45/28.
6. What is the Network Address?
<details>
<answer> Click to reveal </answer>
/28 translates to the mask `255.255.255.240`
$256 - 240 = 16$
the bock size is `16` `.0 .16 .32 .48 .....`
the block is .32 making the network address
`172.16.2.32
</details>

7. What is the Broadcast Address?
<details>
<answer> Click to reveal </answer>
`172.16.2.47`
</details>

