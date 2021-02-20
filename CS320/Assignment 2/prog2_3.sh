#!/bin/bash
	#Compiles all files matching command line arguments
	for var in "$@"
	do
		#Figures out which assingment it is due to the rounding
		#Echos that + assignment number
		gcc $var -o ${var::-3}.x -lm -w
		if grep -q ".3f" $var; then
			echo $var Assignment "#1"
		elif grep -q ".4f" $var; then
			echo $var Assignment "#2"
		elif grep -q ".5f" $var; then
			echo $var Assignment "#3"
		else
			echo $var Assignment "#4"
		fi

	done
