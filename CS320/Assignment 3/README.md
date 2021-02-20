# CS 320 Assignment #3
---
## General Description

This is a collection of bash scripts and a few C programs that will find a user's password, log in as them into a target server, copy all .enc files and the encryptor into the working directory, finds the offset of the encryptor, decrypts the files, and saves them with a new .dec extension.

---

## Descriptions of programs
~~All scripts will output my ID String~~

### prog3_1.sh

This script finds the user's password in the Logins folder, logs into the target server as them, and copies all .enc files and the encryptor to the working directory.

**This program takes three arguments**
1. Logins file location
2. Target server
3. Employee Name

### prog3_2.sh

This script figures out the offset from the encryptor, by running prog3_2.c.

**This program takes no arguments**

### prog3_2.c

This program figures out the difference of two ascii characters. One from stdin and the other from cmd line args.

*Intended use is stdin for cipherText and cmd line arg for plainText*

**This program takes one argument**
1. Plaintext

### prog3_3.sh

This script finds all the .enc files, makes a new .dec file sharing the same root name, echos the new file.dec, then decrypts the .enc file into the matching .dec file using prog3_3.c

**This program takes one argument**
1. Offset printed when prog3_2.sh was run

### prog3_3.c

This program is a dumb decryptor for a Caeser cipher, it hardly does any error checking. But it works for all alphabet characters(upper & lower) so  ¯\\_(ツ)_/¯. It expects one cmd line arg, the offset of which to work. It will then decrypt until a new line is entered or break if characters exceeds 256, don't do that.(It could possibly also encrypt, but would most likely not work properly so don't try it).

**This program takes one argument**
1. Offset printed when prog3_2.sh was run

---
