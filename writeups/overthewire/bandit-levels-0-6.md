Over The Wire (level 0-6)

\-Level 0 - using ssh to log into the over the wire game

&#x20;        - cmd {ssh bandit0@bandit.labs.overthewire.org -p 2220}

\-Level 1 - the instructions is that the password is located in a file in the home 

&#x20;          directory. Commands used :{ls - list the files in the current    directory, cat - read the contents in the file}

\-Level 1-2 - opening a (-)file 

&#x20;          - logic Linux treats - as a standard input meaning cat - will just freeze the terminal waiting for an input 

&#x20;          - solution give the file a relative path with ./ thus cat ./- reveals the contents

\-Level 2-3 -



