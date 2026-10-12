CTF Write-up: Invoice

Status: Solved (3/3)

Vulnerability Classes: Insecure Cryptographic Storage, Business Logic Flaw (Type Juggling)



1\. Initial Reconnaissance \& Enumeration

The engagement began with a standard port scan, revealing a typical web server setup.



Port 22 (SSH): Open, but no credentials available.



Port 80 (HTTP): Open, hosting the target web application.



Directory brute-forcing (using Gobuster/ffuf) revealed the application's core structure and access controls:



/news (200 OK)



/login (200 OK) - Allowed account registration.



/invoices (302 Redirect ➔ /login)



/profile (302 Redirect ➔ /login)



/pay (308 Redirect ➔ /pay/)



After registering a user account and authenticating, the /profile page showed a starting balance of 25 EUR. The /invoices page displayed a target invoice of 1000 with a hint stating: "To get the flag you need to pay the invoice."



Passive enumeration on the /news endpoint revealed two critical developer hints:



"Due to the energy crisis we are freezing customer invoices..."



"We now support paying with different currencies: eur, usd, gbp, and jpy."



Additionally, navigating directly to /pay/ via GET request triggered a Python backend error (AttributeError: 'NoneType' object has no attribute 'strip'), confirming the backend was a Python-based framework expecting specific parameters.



2\. Authorization Bypass (Flask Session Forgery)

Attempting to pay the invoice immediately resulted in a "not authorized to pay" error. This tied back to the "frozen invoices" hint.



Inspection of the HTTP headers in Burp Suite revealed a session cookie format indicative of a Flask application (header.payload.signature in Base64). Decoding the payload section of the cookie revealed the authorization mechanism:



JSON

{"canPay": false, "isLoggedIn": true, "name": "sudo"}

To elevate privileges, the Flask SECRET\_KEY was required to forge a new signature. The tool flask-unsign was utilized to brute-force the signature offline against the rockyou.txt wordlist.



Troubleshooting the Brute-force:



Decompression: Kali Linux ships rockyou.txt.gz compressed. It was extracted using:



Bash

sudo gunzip /usr/share/wordlists/rockyou.txt.gz

Integer Parsing Error: flask-unsign initially crashed with a TypeError when encountering purely numeric passwords in the wordlist, as Python interpreted them as integers instead of strings. This was bypassed using the --no-literal-eval flag.



Bash

flask-unsign --unsign --cookie '<ORIGINAL\_COOKIE>' --wordlist /usr/share/wordlists/rockyou.txt --no-literal-eval

The brute-force successfully recovered the weak secret key. A forged cookie was then generated granting the canPay privilege:



Bash

flask-unsign --sign --cookie "{'canPay': True, 'isLoggedIn': True, 'name': 'sudo'}" --secret '<RECOVERED\_KEY>'

3\. Exploiting the Business Logic Flaw

With the authorization block bypassed, the remaining obstacle was the insufficient balance (25 EUR vs 1000 Invoice).



Intercepting the POST /api/makePayment request in Burp Suite revealed that the frontend dictated the currency to the backend:



JSON

{"id": 1, "currency": "eur"}

Based on the /news hint regarding JPY support, a Type Juggling/Business Logic attack was tested. Modifying the cur=jpy parameter in a GET request proved that 25 EUR dynamically converted to roughly 3528 JPY.



The backend properly converted the user balance into the requested currency, but failed to normalize the static invoice amount (1000). By paying in JPY, the user balance of 3528 easily covered the 1000 cost.



4\. Execution \& Resolution

The attack chain was executed in Burp Suite Repeater by combining both vulnerabilities:



Replacing the Cookie: session=... header with the forged canPay: True cookie.



Modifying the JSON payload to exploit the exchange rate:



HTTP

POST /api/makePayment HTTP/1.1

Host: <TARGET\_IP>

Cookie: session=<FORGED\_COOKIE>

Content-Type: application/json

Referer: http://<TARGET\_IP>/pay/?id=1\&cur=jpy



{"id": 1, "currency": "jpy"}

The server responded with "ok". The forged cookie was injected into the browser's Developer Tools (Storage > Cookies), and refreshing the /invoices page revealed the invoice was successfully paid, yielding the flag.

