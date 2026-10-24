#!/usr/bin/env python3
import dns.resolver
import sys

#!/usr/bin/env python3 $rightarrow$ do not use bash instead use python3
#import statements : Python is modular. By default, it doesn't know how to query DNS servers or read terminal commands to save memory.
#`import dns.resolver` - brings in the specialized DNS toolkit you installed via `pip`
#`import sys`- (System) brings in the toolkit that lets Python talk directly to your Kali Linux terminal environment.

if len(sys.argv) != 2:
    print("Usage: python3 dns_enum.py <domain>")
    sys.exit()

target_domain = sys.argv[1]
print(f"[*] Starting DNS Enumeration for: {target_domain}")

#`sys.argv` (Argument Vector): When you type a command in the terminal like `python3 dns_enum.py tryhackme.com`, Python chops that sentence into a list of words.
#`sys.argv[0]` is the first word `dns_enum.py`
#`sys.argv[1]` is the second word `tryhackme.com`
#The Safety Check (`if len != 2`): This checks the length of that list. If you just typed `python3 dns_enum.py` and forgot to type the domain, the length is only 1. The script prints a helpful instruction on how to use it, and `sys.exit()` cleanly kills the script before it crashes.
#`f"..."` (F-Strings): Putting an `f` before a string allows you to inject variables directly into the text using curly brackets `{target_domain}`.

record_types = ["A", "AAAA", "MX", "TXT", "NS"]

#This is a List (also called an array). Instead of writing the DNS query code five different times for five different records, we store our targets in a list so we can automate it.

for record in record_types:
    try:
        answers = dns.resolver.resolve(target_domain, record)
        # ... printing code ...

#`for record in record_types:` This is a Loop. It tells Python: "Grab the first item in the list `(A)`, assign it to the temporary variable `record`, and run the code below. When you finish, go back up, grab the next item `(AAAA)`, and do it again."
#`try:` The Safety Net): Networks are unpredictable. If you ask a DNS server for an MX record and it doesn't have one, Python's default behavior is to throw a massive red error and kill the entire script. Putting the network request inside a try block tells Python, "Attempt to do this, but if it fails, don't panic; I will tell you how to handle it below."
#`answers = dns.resolver.resolve(...)`: This is the actual weapon. It fires the network packet to the internet, asks for the specific record, and stores the server's response inside the `answers` variable.

    except dns.resolver.NoAnswer:
        print(f"\n[-] No {record} Records found.")
    except dns.resolver.NXDOMAIN:
        print(f"\n[!] Error: The domain {target_domain} does not exist.")
        break

#`except` blocks: These are the catchers for the `try` block's safety net.
#If the server replies, "I exist, but I don't have an MX record," it triggers `NoAnswer`. We print a clean message and the loop continues to the next record.
#If the server replies, "This website does not exist at all," it triggers `NXDOMAIN`. Since the website is dead, there is no point in checking the rest of the list. The `break` command violently forces Python to exit the `for` loop entirely and jump to the end of the script.