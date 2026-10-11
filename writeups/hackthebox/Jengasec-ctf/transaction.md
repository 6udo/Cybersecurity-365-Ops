Here is a structured, Markdown-ready penetration testing report. This format translates cleanly into version control, making it an excellent template to commit directly to your public portfolio to document your daily hands-on practice. It covers both the offensive exploitation path and the defensive remediation concepts.



Penetration Test Report: Cart.htb

Executive Summary

This report details the exploitation path for the cart.htb target environment. The machine exhibited three critical security vulnerabilities that, when chained together, allowed for complete authentication bypass and unauthorized access. The attack path consisted of client-side parameter tampering to bypass payment requirements, forced error generation to exploit an exposed Werkzeug debugger, and cryptographic forgery to bypass a Two-Factor Authentication (2FA) gateway.



1\. Reconnaissance \& Enumeration

Network Scanning:

Initial reconnaissance identified two open ports:



Port 22: OpenSSH 8.2p1



Port 80: Werkzeug httpd 2.2.2 (Python 3.8.10) running a Flask application out of /root/app/app.py.



Web Enumeration:

Directory brute-forcing (via Gobuster) revealed several endpoints on the primary web server, including /console, /transaction, /buy, /pay, and /payment.



During dynamic interaction with the application, a redirect to a secondary payment gateway was observed, revealing the use of virtual host routing. Local DNS routing was required to access this new attack surface.



Action Taken:

Added the virtual host to the local routing table:



Bash

sudo nano /etc/hosts

<TARGET\_IP> cart.htb pay.cart.htb

A secondary Gobuster scan against \[http://pay.cart.htb](http://pay.cart.htb) confirmed the existence of the /transaction and /console endpoints on the payment vhost.



2\. Vulnerability 1: Business Logic Flaw (Parameter Tampering)

Description:

The application handles shopping cart pricing exclusively via client-side JavaScript (SessionStorage) and hidden HTML form fields, violating the principle of never trusting user input.



Exploitation:

While intercepting the checkout process, the backend was found to expect a specific item ID (ssh) with a hardcoded price of $500. By bypassing the broken frontend JavaScript and manipulating the Document Object Model (DOM) directly via browser developer tools, the hidden input value for the SSH access cost was altered.



Payload:



HTML

<!-- Original HTML -->

<input id="Server SSH Access" type="hidden" name="ssh" value="500">



<!-- Manipulated HTML -->

<input id="Server SSH Access" type="hidden" name="ssh" value="0">

Submitting the manipulated form successfully bypassed the payment wall and advanced the application state to the 2FA/OTP verification stage.



3\. Vulnerability 2: Information Disclosure (Exposed Debugger)

Description:

The Python/Flask backend was deployed in a production-facing environment with Werkzeug's Debug Mode enabled. When an application encounters a fatal error in debug mode, it generates a highly verbose stack trace that leaks source code and the exact contents of local variables currently loaded in server memory.



Exploitation:

By navigating to \[http://pay.cart.htb/transaction](http://pay.cart.htb/transaction) (an endpoint known to lack proper parameter handling), a 500 Internal Server Error was intentionally triggered.



Analyzing the resulting Werkzeug stack trace revealed the backend validation logic for the transaction, as well as a hardcoded cryptographic secret:



Python

secret\_key = b"NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"

h = hmac.new(secret\_key, b'SUCCESS', hashlib.sha256).hexdigest()

h1 = hmac.new(secret\_key, b'FUNDS\_ERR', hashlib.sha256).hexdigest()

r\_h = request.args.get('h')

4\. Vulnerability 3: Cryptographic Forgery \& 2FA Bypass

Description:

The 2FA validation logic relies on an HMAC-SHA256 hash passed via the URL parameter h to verify transaction integrity. Because the secret\_key was leaked via the previous vulnerability, the cryptographic signature could be forged entirely offline.



Exploitation:

A local Python environment was used to recreate the exact server-side HMAC generation process. By providing the leaked secret\_key and the target string b'SUCCESS', a valid signature was computed.



Exploit Script:



Python

import hmac

import hashlib



secret\_key = b"NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"

h = hmac.new(secret\_key, b'SUCCESS', hashlib.sha256).hexdigest()

print(h)

\# Output generated the valid hash

The forged hash was then passed to the transaction endpoint via a GET request:

\[http://pay.cart.htb/transaction?code=SUCCESS\&h=](http://pay.cart.htb/transaction?code=SUCCESS\&h=)<FORGED\_HASH>



This successfully bypassed the OTP requirement and validated the transaction, resulting in the retrieval of the flag.



5\. Defensive Remediation (Blue Team Considerations)

To secure this environment against similar attack chains, the following controls must be implemented:



Server-Side State Management: Cart totals and item pricing must never rely on hidden HTML inputs or client-side storage. Prices should be fetched securely from a backend database at the moment of checkout, referencing only a sanitized item ID provided by the user.



Disable Debug Environments: Ensure that app.run(debug=True) or FLASK\_ENV=development is strictly disabled in any production-facing configuration. Werkzeug debuggers must never be exposed to external network interfaces.



Secure Secret Storage: Cryptographic keys (secret\_key) must not be hardcoded directly into the application source code. They should be generated securely, stored in environment variables, and accessed via a secrets management system.

