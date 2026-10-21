### Vulnerability Profile: SQL Injection (SQLi)
## 1. Executive Summary
SQL Injection (SQLi) is a critical web security vulnerability that allows an attacker to interfere with the queries an application makes to its database. It occurs when untrusted user input is directly concatenated into a dynamic SQL query without proper sanitization or parameterization. This flaw can allow attackers to view data they are not normally authorized to retrieve, modify or delete data, and in some cases, escalate privileges to compromise the underlying server.

## 2. Operational Mechanics
Web applications use SQL (Structured Query Language) to interact with backend databases (e.g., MySQL, PostgreSQL, MSSQL).

# The Flaw:
Consider a login script that takes a username and password from a web form:
SELECT * FROM users WHERE username = 'USER_INPUT' AND password = 'PASSWORD_INPUT';

If the application does not validate the input, an attacker can input ' OR 1=1-- into the username field.

The Resulting Query:
# SELECT * FROM users WHERE username = '' OR 1=1--' AND password = '';

[']: Closes the application's string delimiter.
[OR 1=1]: Injects a mathematical truth (1 always equals 1).
[--]: Comments out the rest of the query (ignoring the password check).

The database evaluates 1=1 as True, bypassing authentication and logging the attacker in, typically as the first user in the database (often the administrator).

## 3. Classifications of SQL Injection
# A. In-Band (Classic) SQLi
The attacker uses the same channel of communication to launch the attack and gather results.

Error-Based: The attacker forces the database to generate an error message, which is displayed on the web page. These errors often leak database types, version numbers, or table structures.
Union-Based: The attacker leverages the UNION SQL operator to combine the results of their malicious query with the results of the original query, displaying the stolen data directly on the web page.

# B. Inferential (Blind) SQLi
The application is vulnerable, but its HTTP responses do not contain the results of the relevant SQL query or any database errors.

Boolean-Based (Content): The attacker sends a query asking the database a True/False question. The web page loads differently depending on whether the query was True or False, allowing the attacker to infer data character by character.
Time-Based: The attacker injects a command that pauses the database for a specific amount of time (e.g., SLEEP(10)). By measuring the time it takes the server to respond, the attacker infers if their injected statement was True or False.

## 4. Remediation & Defense (Blue Team)
The most effective defense against SQL injection is separating the SQL code structure from the user-provided data.

Prepared Statements (Parameterized Queries): The developer defines the SQL query structure first, and passes the user input strictly as a parameter. The database treats the input as raw data, not executable code.
Stored Procedures: Similar to prepared statements, the SQL code is defined and stored on the database itself, preventing arbitrary query execution.
Input Validation & Escaping: Enforce strict allow-lists for user input (e.g., an age field must only contain integers). Escape special characters (like quotes) as a defense-in-depth measure.

