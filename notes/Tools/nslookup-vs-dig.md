# nslookup
`nslookup` $\rightarrow$ Name server lookup

```bash
user$ nslookup target.com
-- returns basic A record ipv4 ip address
```
# dig
`dig` $\rightarrow$ Domain Information Groper
Security engineers prefer dig because it provides raw, granular output showing exactly how the DNS server responded, including query times and specific record filtering

`dig target.com +short` $\rightarrow$ returns just the ip address
`dig target.com MX` $\rightarrow$ asks for the mail exchange records (Critical for phishing and mail spoofing recon)
`dig axfr @<DNS_Server_IP> target.com` (Attempts a Zone Transfer —a massive vulnerability where a misconfigured DNS server hands you a copy of every single subdomain it knows about).

 `@<DNS_Server_IP` **(The Interrogated Server):** This tells dig who you are asking.
 `target.com` **(The Subject):** This tells dig what you are asking about.
* **Why this is necessary:** If you just run `dig axfr target.com`, your computer asks your local ISP (or Google DNS) for the zone transfer. Public DNS servers will automatically reject this request. To execute a zone transfer, you must directly interrogate the target's Authoritative Name Server (the server they own and operate).
In a real engagement, you find their DNS server first `dig target.com NS`, take that IP address, and then point your `axfr` attack directly at it using the `@` symbol.

If you want to see absolutely everything the server is willing to tell you (A, AAAA, MX, TXT, and NS records), you can use the ANY flag:
```bash
user$ dig target.com ANY
```
