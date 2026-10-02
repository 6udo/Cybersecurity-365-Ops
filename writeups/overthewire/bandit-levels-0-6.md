**Over The Wire (level 0-6)**

**-Level 0** - using ssh to log into the over the wire game

&#x20;        - cmd {ssh bandit0@bandit.labs.overthewire.org -p 2220}

**-Level 1** - the instructions is that the password is located in a file in the home

&#x20;          directory. Commands used :{ls - list the files in the current

&#x20;          directory, cat - read the contents in the file}

**-Level 1-2** - opening a (-)file

&#x20;          - logic Linux treats - as a standard input meaning cat - will just

&#x20;            freeze the terminal waiting for an input

&#x20;          - solution give the file a relative path with ./ thus cat ./-

&#x20;            reveals the contents

**-Level 2-3** - reading the contents of a file with {spaces} and {dashed file}

&#x20;          - the command cat "--spaces in this filename--" does not work

&#x20;            because of the dashes however from previous flags of using {./}

&#x20;            together with {""} we are able to read the file contents

**-Level 3-4** - the file is located in the inhere directory meaning we have to

&#x20;            change directories from our home directory using the command {cd

&#x20;            inhere}

&#x20;          - the file is hidden meaning the standard ls command won't reveal it

&#x20;            we use the command {ls -al} to reveal hidden files

&#x20;          - standard cat command will not work because the file is a dot file

&#x20;            so the solution is {cat ...Hiding-From-You}

**-Level 4-5** - the file we are looking for is a human readable file among other

&#x20;            files in the inhere directory
- human readable files are commonly referred to as ASCII text

&#x20;          - method 1 cat all the files one by one until you find a human

&#x20;            readable file works but in a scenario with hundreds of files it is

&#x20;            slow i used the command {file ./-*} the command looks at all the

&#x20;            dashed files in the current directory and lists the type of

&#x20;            content in the file with 6 coming in as data and one coming in as

&#x20;            ASCII text

**-Level 5-6** - finding a file with the properties { human readable, 1033 bytes in

&#x20;            size and not executable}
- there are multiple directories in the inhere directory with

&#x20;            multiple files in each directory meaning searching one by one is

&#x20;            redundant i used the command { find . -type f -size 1033c} meaning

&#x20;            find . (in this directory) a file (-type f) with the size 1033

&#x20;            bytes (-size 1033c) and we find the file in directory 7 being a

&#x20;            dot file and using the {ls -al} command we find that the file is

&#x20;            non executable meaning no (x) on the permissions and the file is

&#x20;            exactly 1033 bytes in size



