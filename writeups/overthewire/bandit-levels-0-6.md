**Over The Wire (level 0-6)**



**-Level 0**

&#x20;

\- using ssh to log into the over the wire game

\- cmd {ssh bandit0@bandit.labs.overthewire.org -p 2220}

**-Level 1** 



\- the instructions is that the password is located in a file in the home directory. Commands used :{ls - list the files in the current directory, cat - read the contents in the file}

**-Level 1-2** 



\- opening a (-)file

\- logic Linux treats - as a standard input meaning cat - will just freeze the terminal waiting for an input

\- solution give the file a relative path with ./ thus cat ./- reveals the contents

**-Level 2-3** 



\- reading the contents of a file with {spaces} and {dashed file}

\- the command cat "--spaces in this filename--" does not work because of the dashes however from previous flags of using {./} together with {""} we are able to read the file contents

**-Level 3-4** 



\- the file is located in the inhere directory meaning we have to change directories from our home directory using the command {cd inhere}

\- the file is hidden meaning the standard ls command won't reveal it we use the command {ls -al} to reveal hidden files

\- standard cat command will not work because the file is a dot file so the solution is {cat ...Hiding-From-You}

**-Level 4-5** 



\- the file we are looking for is a human readable file among other files in the inhere directory

* human readable files are commonly referred to as ASCII text

&#x20;     - method 1 cat all the files one by one until you find a human readable   

&#x20;       file works but in a scenario with hundreds of files it is slow i used 

&#x20;       the command {file ./-\*} the command looks at all the dashed files in 

&#x20;       the current directory and lists the type of content in the file with 6 

&#x20;       coming in as data and one coming in as ASCII text

**-Level 5-6** 



\- finding a file with the properties { human readable, 1033 bytes in size and not executable}

* there are multiple directories in the inhere directory with multiple files in each directory meaning searching one by one is redundant i used the command { find . -type f -size 1033c} meaning find . (in this directory) a file (-type f) with the size 1033 bytes (-size 1033c) and we find the file in directory 7 being a dot file and using the {ls -al} command we find that the file is non executable meaning no (x) on the permissions and the file is

&#x20;  exactly 1033 bytes in size

