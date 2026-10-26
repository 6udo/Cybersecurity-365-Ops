# OverTheWire: Bandit (Levels 22 - 24)
**Platform:** OverTheWire | **OS:** Linux | **Topic:** Cron Jobs & Automation Exploitation | **Date:** October 2026

## 1. Executive Summary
Levels 22 through 23 of the Bandit wargame focus on exploiting insecure automated system tasks (cron jobs). The exploitation paths demonstrated how predictable dynamic file generation and overly permissive spool directories allow low-privileged users to hijack automated processes and force higher-privileged service accounts to expose sensitive data.

---

## 2. Level 22 $\rightarrow$ 23: Replicating Dynamic Hashes
**Objective:** Recover the Bandit 23 password by predicting the output of an automated script.

### 2.1 Reconnaissance
The cron job configuration for `bandit23` was analyzed to locate the execution script.
```bash
cat /etc/cron.d/cronjob_bandit23
Output: @reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
Output: * * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
```
Reading the target script revealed its operational logic:

```bash
cat /usr/bin/cronjob_bandit23.sh
```
**Script Logic:** The script dynamically determines the user executing it (`bandit23`), appends it to a string, hashes that string using `MD5`, and uses the resulting hash as a filename in `/tmp/` to store the password.

**2.2 Exploitation**
Because the hashing algorithm and input string were visible in plaintext, the cryptographic generation was replicated locally to calculate the exact filename.

```bash
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
Output: 8ca319486bfbbc3663ea0fbe81326349
```
With the filename successfully predicted, the target file was read from the temporary directory, exposing the `bandit23` password.

```bash
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
Output: password 
```
