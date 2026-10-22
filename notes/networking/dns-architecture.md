# Network Theory: DNS Architecture

If IP addresses are the geographic coordinates of a server, the Domain Name System (DNS) is the internet's GPS application. Humans cannot memorize `142.250.190.46`, so we type `google.com`. DNS servers act as a decentralized global phonebook that translates human-readable domain names into machine-readable IP addresses.
DNS operates primarily on `Port 53 (UDP/TCP)`. During reconnaissance, interrogating a target's DNS server can reveal hidden infrastructure, internal subdomains, and mail server configurations.

# Core DNS Record Types
When you query a domain, you are asking for specific "records." You must know what these do to exploit them

* **A Record (Address):** Maps a domain name directly to an IPv4 address (e.g., `test.com` $\rightarrow$ `192.168.1.10`)
* **AAAA Record:** Maps a domain name to an IPv6 address.
* **MX Record (Mail Exchange):** Specifies the exact server responsible for receiving emails on behalf of the domain. (Critical for phishing and mail spoofing recon).
* **TXT Record (Text):** Allows administrators to insert arbitrary text into the DNS record. Modern security relies on TXT records to prove domain ownership and establish email validation rules (SPF, DKIM, DMARC).
