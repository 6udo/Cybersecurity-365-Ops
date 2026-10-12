CTF Writeup: Racecar

1\. Executive Summary

Target: Racecar

Vulnerability: Time-of-Check to Time-of-Use (TOCTOU) Race Condition / DNS \& CORS Misconfigurations

Objective: Bypass business logic to obtain more than 2 months of an active premium subscription using a single-use 1-month trial code.



2\. Reconnaissance

Initial enumeration began with an Nmap scan to identify open ports and running services.



Port 22/tcp: OpenSSH 8.9p1 Ubuntu



Port 80/tcp: HTTP (Web Server)



Navigating to the web server via its raw IP address yielded a login portal with a registration option. A curl inspection revealed a 302 Found redirect to /login with a Vary: Cookie header, indicating strict session management.



3\. Web Application Analysis

Attempts to register an account via the raw IP address failed. Inspecting the HTTP traffic in Burp Suite revealed two critical routing issues:



DNS Resolution Failure: The frontend JavaScript attempted to send POST requests to /api/register and /api/login hosted on racecar.htb. Because the local machine lacked this DNS mapping, the requests timed out.



CORS Preflight Blocking: Attempting to force the request resulted in the browser sending an OPTIONS request. The API server did not return the correct Cross-Origin Resource Sharing (CORS) headers, causing the browser to silently drop the actual POST request containing the credentials.



Resolution:

The target domain was manually mapped to the machine's IP address in the local hosts file:



Bash

sudo nano /etc/hosts

<TARGET\_IP> racecar.htb

Navigating to \[http://racecar.htb](http://racecar.htb) bypassed the CORS restriction, allowing successful account registration and login.



4\. Vulnerability Discovery

Upon authenticating, the user profile dashboard presented a specific objective: obtain more than 2 months of an active subscription. The application provided a promotional trial code, TRIAL31, which granted exactly 1 month of premium access.



Manual testing confirmed the business logic:



Submitting TRIAL31 successfully incremented the subscription by 1 month.



Submitting it a second time returned a "success":"fail" message.



This single-use limitation, combined with the machine's name ("Racecar"), strongly indicated a potential Race Condition vulnerability in the coupon processing endpoint.



5\. Exploitation (TOCTOU Race Condition)

To exploit the vulnerability, the attack had to be executed while the coupon was still in an "unused" state in the database.



Account Reset: Registered and authenticated into a newly created account to ensure a clean database state for the TRIAL31 code.



Traffic Interception: Navigated to the profile page, entered the trial code, and intercepted the POST request using Burp Suite before it left the browser.



Payload Preparation: Forwarded the intercepted request to Burp Suite's Repeater. The request was duplicated 10 times into a single Tab Group. The original intercepted request was dropped to prevent the database from processing it prematurely.



Parallel Execution: Utilizing Burp Suite's "Send group (parallel)" feature, all 10 requests were fired at the exact same microsecond.



Result: The simultaneous requests forced a Time-of-Check to Time-of-Use (TOCTOU) logic failure. The database verified the coupon was valid for all 10 concurrent requests before it could update the coupon's status to "used."



Refreshing the profile dashboard confirmed the subscription had been incremented well beyond the 2-month threshold, completing the objective and capturing the flag.



Vulnerability Report: Time-of-Check to Time-of-Use (TOCTOU) Race Condition

1\. Vulnerability Description

A Time-of-Check to Time-of-Use (TOCTOU) race condition exists in the application's promotional code processing logic. The endpoint responsible for applying subscription coupons fails to lock the database transaction between the verification phase (checking if the coupon is valid) and the execution phase (crediting the account and marking the coupon as used).



2\. Mechanism of Attack

The vulnerability is exploited by sending a high volume of concurrent identical HTTP POST requests applying the same coupon code (e.g., TRIAL31).



Time of Check: All parallel requests hit the database simultaneously. The database verifies that the coupon has not been used by the account.



Time of Use: Because the database has not yet updated the coupon status to "used" from the first request, all concurrent requests pass the validation check.



Execution: The application grants the subscription extension for every request that passed the check, bypassing the intended single-use business logic.



3\. Business Impact

Attackers can bypass application business logic to gain unauthorized resources, elevated privileges, or financial benefits. In this instance, a single-use one-month subscription code was leveraged to grant multiple months of premium access. In a financial application, this same flaw could be used to multiply account balances or bypass withdrawal limits.



4\. Remediation \& Mitigation

To resolve this vulnerability, the "check" and "update" phases must be tightly coupled into a single atomic operation. Developers should implement one of the following architectural changes:



Atomic Database Updates (Recommended):

Rely on the database to handle the condition within the update query itself. Check the number of affected rows to determine success.



SQL

UPDATE user\_coupons 

SET status = 'used' 

WHERE user\_id = 123 AND coupon\_code = 'TRIAL31' AND status = 'unused';

(If the query returns 0 affected rows, the coupon was already used, and the application should abort the subscription extension).



Pessimistic Locking:

Explicitly lock the database row when it is first read so that no other concurrent request can read or modify it until the entire transaction is complete.



SQL

SELECT status FROM user\_coupons WHERE user\_id = 123 FOR UPDATE;

Unique Constraints:

Enforce a unique index on the database level (e.g., a composite key combining user\_id and coupon\_code) to ensure the database physically rejects duplicate entries if the application logic fails.

