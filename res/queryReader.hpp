#define MAXQUERYTERMNUM 100

char queryFilename[MAXFILENAME];
char queryTerms[MAXQUERYTERMNUM][MAXTERMLEN];
int queryTermNum;

void readQueryFile(void){
	FILE* q = fopen(queryFilename, "r");
	queryTermNum = 0;
	int len;
	while (fgets(queryTerms[queryTermNum], MAXTERMLEN, q) != NULL)
		queryTermNum++;
	// remove '\n'
	for (int i = 0; i < queryTermNum - 1; i++){
		len = strlen(queryTerms[i]);
		queryTerms[i][len - 1] = '\0';
	}
	return;
}