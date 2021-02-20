#include <stdio.h>
#include <math.h>

#define PI  3.14159

	int main(int argc, char *argv[]){

		int i; //For for loop
		double size;
		double stepSize;
		double degrees = 0;
		double radians = 0;
		sscanf(argv[1], "%lf", &size);
		sscanf(argv[2], "%lf", &stepSize);
	    //Prints out the degrees that the program will evaluate at
		for( i = 0; i < size; i++){
			printf("%0.2lf ", degrees);
			degrees += stepSize;
		}
		printf("\n"); //New line that wont repeat in the for loops
		//Converts the step size into radians for Cos function
		stepSize *= (PI/180);
		//Prints out the value of cosine at the chosen intervals
		for( i = 1; i <= size; i++){
			printf("%0.2lf ", cos(radians));
			radians += stepSize;
		}
		printf("\n");
	}
