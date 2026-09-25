Day 1: Hypervisor Isolation Runbook

 Objective
Establish a sterile operational environment by forcing an existing Kali Linux VM ("Odin") to route all traffic through a Whonix-Gateway Tor node.

 1. VirtualBox Network Configuration
-Whonix-Gateway: Left on default settings (Adapter 1: NAT, Adapter 2: Internal Network 'Whonix').
-Kali Linux (Odin): Removed the default NAT adapter to sever direct internet access. 
- Added a new adapter set to Internal Network and named it `Whonix`.

 2. Troubleshooting: DHCP & Name Resolution Failures
After attaching Kali to the internal network, `curl` commands failed to resolve hosts. 
 Cause: The Whonix-Gateway intentionally disables DHCP to prevent IP leaks, meaning Kali had no IP address or DNS server assigned.

Fix 1: Hostname Resolution
The `sudo` command threw an `unable to resolve host Odin` warning because the machine had no network. Mapped the hostname to the local loopback address:
`echo "127.0.1.1 Odin" | sudo tee -a /etc/hosts`

Fix 2: Static IP Assignment
Manually assigned the static IP and pointed the DNS and Gateway directly to the Whonix-Gateway's internal IP (10.152.152.10) using NetworkManager:
`sudo nmcli connection modify "Wired connection 1" ipv4.addresses 10.152.152.11/18 ipv4.gateway 10.152.152.10 ipv4.dns 10.152.152.10 ipv4.method manual`
`sudo nmcli connection up "Wired connection 1"`

## 3. Verification
Executed a CLI test to verify the Tor circuit was routing correctly:
`curl https://check.torproject.org`
**Result:** "Congratulations. This browser is configured to use Tor."