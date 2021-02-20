# CS 320 Assignment #1

## General Description

This is a collection of basic C programs, the first three use standard in/out and the last utilizes command line arguments for input.  
~~All programs will output my title string~~

## Descriptions of Programs

### `prog1_1.c`

This program takes no input and should always output `Hello! my name is William Fox`.

### `prog1_2.c`

This program will ask you politely for your name and then respond with `Hello [your name]. Nice to meet you!`.

### `prog1_3.c`

This program will ask you for an integer and then return the Hyperbolic Cosine value for that value.  
**This program expects the input to be in degrees**

### `prog1_4.c`

This program requires two command  line arguments to run. It will output the value of Cosine at multiples of the second argument with the frequency of the first argument.  
**This program expects the input to be in degrees**

Example:

`./a.out 5 15` will output

Degrees Evaluated at:....`0.0 15.0 30.0 45.0 60.0`

Value of Cosine:..............`1.0 0.97 0.87 0.71 0.50`


## How to Compile and Run the Programs

### How to compile and run the two programs in Linux terminal
1. Have source file in active directory
2. type `gcc prog1_1.c` and hit enter (For program 2 replace prog1_1.c with prog1_2.c)
3. type `./a.out` and hit enter
4. enter any information if prompted

### How to compile and run the third program in Linux terminal
1. Have source file in active directory
2. type `gcc prog1_3.c -lm` and hit enter (-lm is needed for math.h)
3. type `./a.out` and hit enter
4. enter any information if prompted

### How to compile and run the fourth program in Linux terminal
1. Have source file in active directory
2. type `gcc prog1_3.c -lm`
3. type `./a.out <number of elements> <step size in degrees>` and hit enter
  * An Example of running `prog1_4.c` can be found in the prog1_4.c description
