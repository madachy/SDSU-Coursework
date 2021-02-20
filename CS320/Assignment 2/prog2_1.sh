#!/bin/bash

# Finds and saves the student that got all perfects
student=`grep 100,100,100 Grades`

#Removes the scores and commas from the name
name=${student//,/ }
name=${name% 100 100 100}
echo ${name}


#Finds Login Information and saves it
login=`grep -i -s ${name} Logins`


#Grabs the masc id from the login information
masc=${login%,*}
masc=${masc##*,}

echo ${masc}
password=${login##*,}

echo ${password}
