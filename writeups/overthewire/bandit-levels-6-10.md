**-Level 6-7**

&#x20;

\- objective find a file in the server with the properties

\-owned by user bandit7

\-owned by group bandit6

\-33 bytes in size

&#x20; **executing command** { find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null}

&#x20; : {/}look from the root directory , {-type f} look only for files and not directories, {-user bandit7} user permissions for bandit7 , {-group bandit6} group permissions for bandit6, {-size 33c} size of the file is 33bytes, {2>/dev/null} looking through all the files the command might look into files which is not permitted to leading to a lot of error outputs the command outputs the standard errors (2) and throws it to (/dev/null) a file in Linux that acts as a blackhole and destroys whatever data is sent to it

&#x20; :file permissions ; x-ters 2-4 user permissions (rw-)

&#x20;                     x-ters 5-7 group permissions (r--)

&#x20;                     x-ters 8-10 others (---)

&#x20;           r(4) - read , w(2) - write , x(1) - execute



**-Level 7-8** 



\- find the pass in a txt file , the file is large thus cat is not useful the grep command is used as it prints the line with the word used with it and since the hint is the pass is next to the word millionth the cmd {grep "millionth" data.txt} outputs the password



**-level 8-9** 



\- objective find the pass in the txt file and the hint that it is the only line that occurs once cmd **\[sort data.txt | uniq -u]** , **sort** - sorts the data alphabetically **|** piping links the output of the first command to the second command , **uniq -u** outputs only the unique line.



**-Level 9-10** 



**-** objective was to find the password in the txt file with binary data and ascii texts cmd **\[strings data.txt | grep "="]** string command outputs only the printable characters which is ascii texts , the output is then piped to grep "=" to find the lines with the \[=] characters

