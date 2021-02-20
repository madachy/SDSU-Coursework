# CS 320 Assignment #2
---
## General Description

This is a collection of bash shell scripts that will find a student who has received perfect grades, find their username and password, search through their repository for C files, copies the found files to the working directory, compiles the found programs, and outputs which program goes with which assignment.

---

## Descriptions of programs
~~All programs will output my ID String~~

### prog2_1.sh

This program searches a "Grades" file and finds a student with perfect assignment scores. The program then searches the "Logins" file to find the corresponding student's username and password.

** This program takes two arguments**
1. Grades file location
2. Logins file location

### prog2_2.sh

This program searches through the found students git repository for C program source files and copies them to the working directory. It will also echo the found program names to the screen.

**This program takes one argument**
1. The root directory of the repository

### prog2_3.sh

This program compiles four C programs, and figures out which C programs match with which assignments and echos the pair.

**This program takes four arguments**
1. First C file
2. Second C file
3. Third C file
4. Fourth C file

---

## How to run and Example Outputs
*All programs will output my ID String*

### prog2_1.sh

`./prog2_1.sh Grades Logins`

`[Student]`

`[masc457]`

`[PAS5w0rd]`

### prog2_2.sh

`./prog2_2.sh cs320assignment3`

`[fixed.c]`

`[fixedv2.c]`

`[test.c]`

`[ADFG.c]`

### prog2_3.sh

`./prog2_2.sh fixed.c fixedv2.c test.c ADFG.c`

`[fixed.c Assignment #3]`

`[fixedv2.c Assignment #2]`

`[test.c Assignment #1]`

`[ADFG.c Assignment #4]`

---
