Pavlov has released 7-Zip for Linux in AMD64, ARM64, x86, and armhf versions, which users can download at the following links:

7-Zip for 64-bit Linux x86-64 (AMD64)
7-Zip for 64-bit Linux ARM64
7-Zip for 32-bit Linux x86
7-Zip for 32-bit Linux armhf

This first version of 7-Zip for Linux is released as a console application and has similar, but not identical, command-line arguments as p7zip.

While Pavlov has not released the source yet, he shared some information on how it has been compiled. As he self-admittedly does not work with Linux, he has requested other developers' advice on the best way to compile the program.

"These new 7-Zip binaries for Linux were linked (compiled) by GCC without -static switch. And compiled 32-bit executables (x86 and armhf) didn't work on some arm64 and amd64 systems, probably because of missing of some required .so files."

"Please write here, if you have some advices how to compile and link binaries that will work in most Linux systems," Pavlov stated on his release page.

Pavlov is also asking users to benchmark the 7-Zip for Linux's performance on various systems using the following command:

./7zz b "-mm=*" "-mmt=*" -bt > bench.txt
Users can then upload their bench.txt report as a comment on 7-Zip for Linux's release page to be reviewed for bugs and potential performance enhancements.

While this is great news for Linux users who prefer to use 7-Zip, a recent tweet by Google software engineer Christian Blichmann raises mysterious concerns about 7-zip's source code.
