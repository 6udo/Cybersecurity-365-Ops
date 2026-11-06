Automating your workflow is what separates a manual tester from a red team operator. When you compromise a machine, you won't have a graphical interface; you will have a raw terminal. If you want to ping 254 hosts on a /24 subnet, you cannot do it manually. You need Bash.

Here is the operational breakdown of how to build dynamic, context-aware scripts.

## 1. Variables (Storing Data)
In Bash, variables store strings or numbers, like a target IP or a wordlist path.

Definition: Do not use spaces around the equals sign. `TARGET="10.10.10.5"`

Calling: Always use the dollar sign to call the variable. `echo "Scanning $TARGET..."`

## 2. Positional Arguments (Making Scripts Dynamic)
Hardcoding IPs into a script is a bad habit. You want to pass the target IP to the script from the command line, like this: `./recon.sh 10.10.10.5.`
Bash automatically assigns these inputs to special built-in variables:

`$0`: The name of the script itself (`./recon.sh`).

`$1`: The first argument provided (`10.10.10.5`).

`$2`: The second argument (e.g., a port number like `80`).

`$#`: The total number of arguments provided. (Critical for checking if a user forgot to provide an IP).

`$@`: All arguments combined into a single string.

## 3. Exit Codes & Conditionals (Script Intelligence)
Every command in Linux silently returns a hidden number when it finishes running, called the Exit Code.

`0` = Success.

`1` to `255` = Failure (error).

You can view the exit code of the last run command by typing `echo $?`.

We use these exit codes inside `if` statements to make scripts intelligent. For example, why launch an aggressive 15-minute Nmap scan if the host is offline?

