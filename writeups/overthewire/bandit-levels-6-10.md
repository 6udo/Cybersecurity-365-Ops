\-Level 6-7 - objective find a file in the server with the properties

&#x20;           -owned by user bandit7

&#x20;           -owned by group bandit6

&#x20;           -33 bytes in size

&#x20;          executing command { find / -type f -user bandit7 -group bandit6 -

&#x20;            size 33c 2>/dev/null}

&#x20;           : {/}look from the root directory , {-type f} look only for files

&#x20;            and not directories, {-user bandit7} user permissions for

&#x20;            bandit7 , {-group bandit6} group permissions for bandit6, {-size

&#x20;            33c} size of the file is 33bytes, {2>/dev/null} looking through

&#x20;            all the files the command might look into files which is not

&#x20;            permitted to leading to a lot of error outputs the command outputs

&#x20;            the standard errors (2) and throws it to (/dev/null) a file in

&#x20;            Linux that acts as a blackhole and destroys whatever data is sent

&#x20;            to it

&#x20;           :file permissions ; x-ters 2-4 user permissions (rw-)

&#x20;                               x-ters 5-7 group permissions (r--)

&#x20;                               x-ters 8-10 others (---)

&#x20;           r(4) - read , w(2) - write , x(1) - execute

\-Level 7-8 - find the pass in a txt file , the file is large thus cat is not

&#x20;            useful the grep command is used as it prints the line with the

&#x20;            word used with it and since the hint is the pass is next to the

&#x20;            word millionth the cmd {grep "millionth" data.txt} outputs the

&#x20;            password

level 8-9 - objective find the pass in the txt file and the hint that it is the

&#x20;           only line that occurs once

&#x20;           cmd \[sort data.txt | uniq -u] , sort - sorts the data

&#x20;           alphabetically | piping links the output of the first command to

&#x20;           the second command , uniq -u outputs only the unique line.

**-Level 9-10 -** objective was to find the password in the txt file with binary

&#x20;             data and ascii texts cmd \[strings data.txt | grep "="] string

&#x20;             command outputs only the printable characters which is ascii

&#x20;             texts , the output is then piped to grep "=" to find the lines

&#x20;             with the \[=] characters

