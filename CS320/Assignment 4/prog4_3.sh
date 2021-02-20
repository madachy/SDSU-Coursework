#!/bin/bash
gcc prog4_1.c -o prog4_1 -l lua -l m -l dl -L lua-5.3.3/src/ -I lua-5.3.3/src/

correct=`cat $2`

./prog4_1 $1 > luaTestTemp

if cmp -s "$2" "luaTestTemp"
then
	echo "Passed Test"
else
	echo "Failed Test"
fi
rm luaTestTemp
