#include <stdio.h>
#include <math.h>
#define  PI 3.14159
	int main(){
		double userInput;
		double hcosValue;
		printf("Please input an integer:\n");
		scanf("%lf",&userInput);
		userInput = ((userInput * PI)/180); //Converts Input into degrees
		hcosValue = cosh(userInput);    //Gets the Hyperbolic Cos Value
		printf("%0.3lf\n",hcosValue);
	}
