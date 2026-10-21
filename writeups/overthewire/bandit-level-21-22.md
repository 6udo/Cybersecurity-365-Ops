# OverTheWire Bandit: Level 21 -> 22
Difficulty: Easy | Date: 2026-10-21 | Category: Linux Enumeration & Privilege Escalation
## Objective
A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

## Summary
what is cron job?
A cron job is simply a Linux system's recurring alarm clock.

Instead of playing a sound when the alarm goes off, the Linux cron daemon [a program running invisibly in the background] wakes up, checks its schedule, and automatically executes a script or command.

System administrators use cron jobs to automate repetitive tasks: backing up databases every night at 2:00 AM, clearing temporary files every Sunday, or checking for security updates every hour.

# The Mechanics of Cron
The schedule for these tasks is written in a table called a crontab (cron table). System-wide cron jobs are typically stored as text files inside the [/etc/cron.d/] directory.

If you read a file in /etc/cron.d/, it looks like a cryptic string of stars followed by a command:
[* * * * * bandit22 /usr/bin/cronjob_bandit22.sh]

Here is exactly how to read that line:

The Five Stars [* * * * *]: This is the time schedule. From left to right, they stand for: [Minute], [Hour], [DayofMonth], [Month], [DayofWeek]. Five stars means "run this every single minute of every single day."

The User [bandit22]: This tells the system who should run the script. This is the critical security flaw for this level. Even though you are logged in as bandit21, the system is automatically running this script with the elevated privileges of bandit22.

The Target (/usr/bin/cronjob_bandit22.sh): This is the exact script the system executes.

## Exploitation
Because the system administrator (the wargame creator) configured this cron job to run as bandit22, it has the security clearance to read the bandit22 password file.

You didn't need to break in; you just needed to read the schedule, find the script, and see where the script was dropping the password.

```bash
bandit21@bandit:~$ cd /etc/cron.d/
bandit21@bandit:/etc/cron.d$ ls -al
cronjob_bandit22
bandit21@bandit:/etc/cron.d$ cat cronjob_bandit22
 [* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null]
* * * * * tells the cron daemon to run this task every single minute
bandit22 is the user whose permissions will be used to run the task.
/usr/bin/cronjob_bandit22.sh is the actual script being executed.
bandit21@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh

```bash
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv -----> [this file is readable by the current user] 
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv ---------> [every minute the password is being output with bandit22 privileges then being transfered to the temporary file path which we can read]

bandit21@bandit:/etc/cron.d$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
the password is output

