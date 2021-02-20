#!/bin/bash

#I needed to add this to run the encrpytor
chmod +x encryptor

plainText="a"
#Gets the cipher text from the encryptor
cipherText=`echo $plainText | ./encryptor`

gcc prog3_2.c -o "prog3_2"
#Runs prog3_2(the C program) with the cipher text through stdin and plaintext
#through cmd line args
echo $cipherText | ./prog3_2 $plainText
