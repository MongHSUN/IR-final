#include <vector>
#include <set>
#include <math.h>
vector<int> candidates;
int candidateNum;
int top;
double weights[MAXFILENUM][MAXQUERYTERMNUM]; // fileID => weight

void printCandidates(){
	printf("candidates: ");
	for (int i = 0; i < candidates.size(); i++)
		printf("%d ", candidates[i]);
}

void printWeight(double* w){
	printf("weight: ");
	for (int i = 0; i < queryTermNum; i++)
		printf("%f ", w[i]);
	puts("");
}

void candidatesOr(map<int, int>* wordCount){
	map<int, int>::iterator mit;
	vector<int>::iterator vit, tit;
	vector<int> temp;
	vit = candidates.begin();
	mit = wordCount->begin();
	while (vit != candidates.end() && mit != wordCount->end()){
		if (mit->first > *vit){
			temp.push_back(*vit);
			vit++;
		}
		else if (*vit > mit->first){
			temp.push_back(mit->first);
			mit++;
		}
		else {
			temp.push_back(*vit);
			vit++;
			mit++;
		}
	}
	for (; mit != wordCount->end(); mit++)
		temp.push_back(mit->first);
	for (; vit != candidates.end(); vit++)
		temp.push_back(*vit);
	candidates = temp;
}

void findCandidate(){
	map<char*, map<int, int>*, cmp_str>::iterator it;
	candidates.clear();
	for (int i = 0; i < queryTermNum; i++){
		it = inverts.find(queryTerms[i]);
		if (it == inverts.end())
			continue;
		candidatesOr(it->second);
	}
}

double TF(map<int, int>* wordCount, int fileID){
	map<int, int>::iterator mit = wordCount->find(fileID);
	if (mit == wordCount->end())
		return 0;
	// TF exists in wordCount (fileID => count)
	double tf = mit->second;
	return 0.5 + 0.5 * tf / maxFreq[fileID];
}

double IDF(map<int, int>* wordCount){
	// candidateNum or total fileNum? log or log10?
	return log(MAXFILENUM * 1.0 / wordCount->size());	
}

void findWeight(int fileID){
	map<char*, map<int, int>*, cmp_str>::iterator mit;
	for (int i = 0; i < queryTermNum; i++){
		mit = inverts.find(queryTerms[i]);
		// no data in inverts
		if (mit == inverts.end()){	
			weights[fileID][i] = 0;
			continue;
		}
		weights[fileID][i] = (TF(mit->second, fileID) * IDF(mit->second));
	}
}

double crossSim(int fileID, double* b){
	double sum = 0;
	for (int i = 0; i < queryTermNum; i++)
		sum += weights[fileID][i] * b[i];
	return sum;
}

double distSim(double* a, double* b){
	double sum = 0;
	for (int i = 0; i < queryTermNum; i++)
		sum += (a[i] - b[i]) * (a[i] - b[i]);
	return sqrt(sum);
}

double cosSim(double* a, double* b){
	double up = 0, downL = 0, downR = 0;
	for (int i = 0; i < queryTermNum; i++){
		up += a[i] * b[i];
		downR += a[i] * a[i];
		downL += b[i] * b[i];
	}
	return up / sqrt(downL * downR);
}

void makeQueryW(double* w){
	map<char*, map<int, int>*, cmp_str>::iterator mit;
	for (int i = 0; i < queryTermNum; i++){
		mit = inverts.find(queryTerms[i]);
		// no data in inverts
		if (mit == inverts.end()){
			w[i] = 0;
			continue;
		}
		w[i] = 1 * IDF(mit->second) * (queryTermNum - i) / queryTermNum * 1.0;
	}
}

void printResult(set<pair<double, int> >& r){
	set<pair<double, int> >::reverse_iterator rsit;
	for (rsit = r.rbegin(); rsit != r.rend(); rsit++){
		if (top == 0)
			break;
		//printf("sim: %f, fileName: %s\n", rsit->first, files[rsit->second]);
		//printWeight(weights[rsit->second]);
		printf("%s\n", files[rsit->second]);
		top--;
	}
}

void search(){
	findCandidate();
	candidateNum = candidates.size();
	double queryW[queryTermNum]; // how to calc this??
	double sim;
	set<pair<double, int> > result;	// (sim, fileID)
	pair<double, int> p;
	makeQueryW(queryW);
	for (int j = 0; j < candidateNum; j++){
		findWeight(candidates[j]);
		sim = crossSim(candidates[j], queryW);
		p = make_pair(sim, candidates[j]);
		result.insert(p);
	}
	printResult(result);
}