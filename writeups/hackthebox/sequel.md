# Hack The Box: Sequel
**Tier:** 1 | **OS:** Linux | **Difficulty:** Very Easy | **Date:** October 2026

## 1. Executive Summary
Sequel is a Tier 1 Linux machine that highlights the critical dangers of exposing backend infrastructure directly to the public internet. The exploitation path demonstrated how an insecure default database configuration—specifically, a MariaDB instance running without encryption and permitting unauthenticated root access—leads to immediate and total data compromise. 

## 2. Reconnaissance
Network enumeration was conducted using `nmap` to identify active services and pinpoint exposed infrastructure.

```bash
nmap -sC -sV -p- -T4 <Target_IP>
```
**nmap results**
| Port | State | Service | Version/Notes    |
| :--- | :---  | :----   | :------------    |
| 3306 | Open  | Mysql   | MariaDB (anauthen|
                           ticated access)
## 3. Enumeration & Initial Access
**3.1 Bypassing TLS/SSL Restrictions**
The `nmap` scan revealed that Port 3306 was exposed. An attempt was made to connect to the database as the `root` user without supplying a password.

The initial connection attempt failed with `ERROR 2026 (HY000): TLS/SSL error`, indicating that the modern Kali Linux client required encrypted transit, but the legacy target server lacked SSL certificates. This security control was intentionally bypassed by appending the `--skip-ssl` flag to force an unencrypted, cleartext connection. 

```bash
mysql -h <Target_IP> -u root --skip-ssl
```
## 4. Exploitation & Data Extraction
With administrative access to the database secured, standard SQL enumeration commands were executed to map the internal data structures and locate the flag.

**Step 1: Enumerate Databases**
```bash
SHOW DATABASES;
```
**Step 2: Context Switching & Table Enumeration**
```bash
USE htb;
SHOW TABLES;
```
**Finding:** Identified two primary tables: config and users.

**Step 3: Structural Analysis**
To understand the schema before extraction, the table structure was analyzed.
```bash
DESCRIBE config;
```
**Step 4: Data Exfiltration**
The contents of the `config` table were dumped to the terminal to hunt for hardcoded credentials or flags.
```bash
SELECT * FROM config;
```
**Result:** The query successfully returned the root flag, confirming total compromise of the database.

## 5. Vulnerability Analysis
**Improper Access Control (CWE-284):** The database was exposed to the public internet rather than being restricted to localhost or an internal backend subnet.

**Insecure Default Configuration (CWE-1188):** The `root` database user was left without a password, allowing immediate, unauthenticated administrative access.

**Cleartext Transmission of Sensitive Information (CWE-319):** The database lacked TLS/SSL configuration, meaning any intercepted traffic (including the exfiltrated flag) was transmitted in plaintext.

