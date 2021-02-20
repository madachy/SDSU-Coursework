#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char *argv[]){

	int offset;
	char cipherText[256];
	char letter;
	int i;
	int length;

	offset = atoi(argv[1]);
	// Pulls In cipherText also changes the delimiter to newline
	scanf("%[^\n]s", cipherText);
	//Gets the length of the string
	length = strlen(cipherText);
	for( i = 0; i < length; i++){
	if( cipherText[i] == ' '){
		//Does Nothing to pereserve spaces
	}else if( cipherText[i] < (65+offset)){
		//To close to start of alphabet
		cipherText[i] += (26-offset);
	}else if( cipherText[i] > 96 && cipherText[i] < (97+offset)){
		//To close to start of lower alphabet and don't want to ruin caps
		cipherText[i] += (26-offset);
	}else{
		//I'm still afraid I'm going to break this so I'm leaving this in
		//letter = cipherText[i];
		//letter -= offset;
		cipherText[i] -= offset; //used to be = letter
	}
}
	printf("%s\n", cipherText);

}
