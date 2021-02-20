#include <stdio.h>

int main(int argc, char *argv[]){

	char cipherText;
	char plainText;
	int shift;
	scanf("%c", &cipherText);
	plainText = *argv[1];
	shift = cipherText - plainText;
	printf("%d\n", shift);
}
