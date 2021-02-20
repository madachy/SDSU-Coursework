#!/bin/bash


# These just rename the cmd line args
passwordFile=$1
targetServer=$2
employeeName=$3
# This was so I didn't have to type the expected cmd args every time,
# they're left incase I break something before turn in
#passwordFile="Logins"
#targetServer="sd.lindeneau.com"
#employeeName="Yoko Jamika"
# Gets the username from her name
username=`echo $employeeName | tr '[:upper:]' '[:lower:]'`
username=${username%% *}

#Finds the employees pasword from the file
password=`grep -i "$employeeName" $passwordFile`
password=${password##*,}

#Grabs encrptor and all .enc files from the target server
expect -c "
		log_user 0
		set timeout 1
		spawn scp ${username}@${targetServer}:encryptor .
		expect yes/no { send yes\r ; exp_continue }
		expect password: { send ${password}\r }
		sleep 1
		spawn scp ${username}@${targetServer}:"*.enc" .
		expect yes/no { send yes\r ; exp_continue }
		expect password: { send ${password}\r }
		sleep 1
		exit
"
#Echos found files
echo encryptor
echo *.enc | tr [:space:] "\n"
