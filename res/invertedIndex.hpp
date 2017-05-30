
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <map>
#include <utility>

#define MAXFILENAME 1000
#define MAXWORDNUM 30000
#define MAXWORDLEN 20
#define MAXTERMLEN 2*MAXWORDLEN+1
#define MAXFILENUM 30000
#define MAXTERMNUM 80000

using namespace std;

char fileListFilename[MAXFILENAME];
char invFilename[MAXFILENAME];
char vocabFilename[MAXFILENAME];
// string compare for inverts
struct cmp_str{
	bool operator()(char* a, char* b){
		return strcmp(a, b) < 0;
	}
};
char words[MAXWORDNUM][MAXWORDLEN];			// wordID => word string
int maxFreq[MAXFILENUM];					// fileID => maxFreq
map<int, int> wordCounts[MAXTERMNUM];		// fileID => wordCount
char terms[MAXTERMNUM][MAXTERMLEN];			// termID => term string
map<char*, map<int, int>*, cmp_str> inverts;// term string => wordCounts map
char files[MAXFILENUM][MAXFILENAME]; 		// fileID => filename

void readVocab(){
	FILE* f = fopen(vocabFilename, "r");
	int wordNum = 0;
	while (fscanf(f, "%s", words[wordNum]) != EOF)
		wordNum++;
}

void createInverts(){
	FILE* f = fopen(invFilename, "r");
	int vID1, vID2, fileNum, fileID, count;
	pair<int, int> p;
	pair<char*, map<int, int>* > item;
	int termNum = 0;
	// init maxFreq
	for (int i = 0; i < MAXFILENUM; i++)
		maxFreq[i] = 0;
	// create inverted index
	int lineNum = 0;
	while (fscanf(f, "%d %d %d", &vID1, &vID2, &fileNum) != EOF){
		lineNum++;
		// create wordCounts
		for (int i = 0; i < fileNum; i++){
			fscanf(f, "%d %d", &fileID, &count);
			lineNum++;
			maxFreq[fileID] = count > maxFreq[fileID] ? count : maxFreq[fileID];
			p = make_pair(fileID, count);
			wordCounts[termNum].insert(p);
		}
		// create terms
		strncpy(terms[termNum], words[vID1], strlen(words[vID1]));
		if (vID2 != -1){
			// add space if word2 is English or Digit
			if (isalpha(words[vID2][0]) || isdigit(words[vID2][0]))
				strcat(terms[termNum], " ");
			strncat(terms[termNum], words[vID2], strlen(words[vID2]));
		}
		item = make_pair(terms[termNum], &wordCounts[termNum]);
		inverts.insert(item);
		termNum++;
	}
}

void createFileName(){
	FILE* f = fopen(fileListFilename, "r");
	int fileNum = 0;
	int len;
	while (fgets(files[fileNum], MAXFILENAME, f) != NULL)
		fileNum++;
	// remove '\n'
	for (int i = 0; i < fileNum - 1; i++) {
		len = strlen(files[i]);
		files[i][len - 1] = '\0';
	}
}

void createInvertedIndex(){
	readVocab();
	createInverts();
	createFileName();
}