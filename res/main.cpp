#include <stdlib.h>
#include "invertedIndex.hpp"
#include "queryReader.hpp"
#include "ir.hpp"

void parseArg(int argc, char** argv){
	for (int i = 0; i < argc; i++)
		if (strcmp(argv[i], "-f") == 0){
			strncpy(fileListFilename, argv[i + 1], MAXFILENAME);
			i++;
		}
		else if (strcmp(argv[i], "-v") == 0){
			strncpy(vocabFilename, argv[i + 1], MAXFILENAME);
			i++;
		}
		else if (strcmp(argv[i], "-i") == 0){
			strncpy(invFilename, argv[i + 1], MAXFILENAME);
			i++;
		}
		else if (strcmp(argv[i], "-q") == 0){
			strncpy(queryFilename, argv[i + 1], MAXFILENAME);
			i++;
		}
		else if (strcmp(argv[i], "-t") == 0){
			top = atoi(argv[i + 1]);
			i++;
		}
}

int main(int argc, char** argv){
	parseArg(argc, argv);
	createInvertedIndex();
	readQueryFile();
	search();
	return 0;
}
