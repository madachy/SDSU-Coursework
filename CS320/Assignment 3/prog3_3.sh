#!/bin/bash


offset=$1

gcc prog3_3.c -o prog3_3
# Searches for each .enc file and just echos the name for now
# $matchENC is the matching filename(w/.enc)
find *.enc | while read -r matchENC; do
	#Grabs Cipher Text from .enc file
	cipherText=`cat $matchENC`
	#Makes the new .dec name
	matchDEC=${matchENC//enc/}dec
	#Creates the .dec files
	touch ${matchDEC}
	#Echos new file names
	echo $matchDEC
	#Decrypts
	plainText=`echo $cipherText | ./prog3_3 $offset`
	#Overwrites matching plaintext to new .dec file
	echo $plainText > $matchDEC

done
