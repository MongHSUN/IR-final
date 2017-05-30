import os
import sys
import time

dataPath='../data/lrcc'
vocab='../data/vocab'
invIndex='../data/invIndex'
fileListPath='../data/file_list'
term_dict=dict()
termOccur_dict=dict()
totalTermCount=0
bitermOccur_dict=dict()
totalBitermCount=0
invInd_dict=dict()
biInvInd_dict=dict()
term_list=[]
file_dict=dict()
file_list=[]


def read_filelist():

	global fileListPath,file_dict

	count=0
	with open(fileListPath,'r',encoding='utf8') as fp:
		for line in fp:
			line=line.strip()
			file_dict[line]=count
			file_list.append(line)
			count=count+1

	return


def check_term(f,lastWord,s,termCount):

	global term_dict,term_list,invInd_dict,biInvInd_dict,termOccur_dict,totalTermCount,bitermOccur_dict,totalBitermCount

	if s not in term_dict:
		term_dict[s]=termCount
		term_list.append(s)
		termOccur_dict[s]=1
		termCount += 1
		invInd_dict[s]=dict()
		invInd_dict[s][f]=1
	else:
		termOccur_dict[s] += 1
		if f not in invInd_dict[s]:
			invInd_dict[s][f]=1
		else:
			invInd_dict[s][f] += 1
	if not lastWord=='':
		hashBigramId=str(term_dict[lastWord]).zfill(6)+str(term_dict[s]).zfill(6)
		if hashBigramId not in bitermOccur_dict:
			bitermOccur_dict[hashBigramId]=1
		else:
			bitermOccur_dict[hashBigramId] += 1
		if hashBigramId not in biInvInd_dict:
			biInvInd_dict[hashBigramId]=dict()
		if f not in biInvInd_dict[hashBigramId]:
			biInvInd_dict[hashBigramId][f]=1
		else:
			biInvInd_dict[hashBigramId][f] += 1
	totalTermCount += 1
	totalBitermCount += 1

	return termCount


def isChinese(c):
	return (c >= u'\u4e00' and c <= u'\u9fff')


def isEnglish(c):
	return ((c >= u'\u0041' and c <= u'\u005a') or (c >= u'\u0061' and c <= u'\u007a'))


def build():

	global dataPath,file_list

	termCount=0

	for f in file_list:
		path = dataPath+f
		path=path.strip()
		with open(path,'r',encoding='big5',errors='ignore') as fp:
			firstFlag=0
			for line in fp:
				line=line.split(']')
				line=line[-1]
				if line in ['\n','\r\n']:
					continue
				line=line.strip()
				if firstFlag==0 and ('詞' in line  and '曲' in line):
					firstFlag=1
					continue
				if 'http' in line:
					continue
				elif '精品網頁' in line:
					continue
				elif 'www' in line:
					continue
				line=line.split(' ')
				lastWord=''
				for i in range(len(line)):
					s,flag='',0
					for c in line[i]:
						if str(c).isalpha() or str(c).isdigit():
							if isChinese(c):
								if flag==0:
									termCount=check_term(f,lastWord,str(c),termCount)
									lastWord=str(c)
								else:
									termCount=check_term(f,lastWord,s,termCount)
									lastWord=s
									termCount=check_term(f,lastWord,str(c),termCount)
									lastWord=str(c)
									s,flag='',0
							elif isEnglish(c):
								s += str(c)
								flag=1
							else:
								if not s=='':
									termCount=check_term(f,lastWord,s,termCount)
									lastWord=s
									flag,s=0,''
						else:
							if not s=='':
								termCount=check_term(f,lastWord,s,termCount)
								lastWord=s
								flag,s=0,''
					if not s=='':
						termCount=check_term(f,lastWord,s,termCount)
						lastWord=s

	return


def write_file():

	global dataPath,vocab,invIndex,term_dict,invInd_dict,biInvInd_dict,term_list,file_dict,file_list,termOccur_dict,bitermOccur_dict
	global totalTermCount,totalBitermCount

	totalFileNum=len(file_list)
	with open(vocab,'w',encoding='utf8') as fp:
		for x in term_list:
			fp.write('%s\n' % (x))

	with open(invIndex,'w',encoding='utf8') as fp:
		for term in term_list:
			if len(invInd_dict[term]) > int(0.4*float(len(file_list))) or termOccur_dict[term] < 10:
				continue
			fp.write('%d -1 %d\n' % (term_dict[term],len(invInd_dict[term])))
			for key in invInd_dict[term]:
				fp.write('%d %d\n' % (file_dict[key],invInd_dict[term][key]))
		for key in biInvInd_dict:
			if len(biInvInd_dict[key]) > int(0.4*float(len(file_list))) or bitermOccur_dict[key] < 10:
				continue
			fp.write('%d %d %d\n' % (term_dict[term_list[int(key[0:6])]],term_dict[term_list[int(key[6:12])]],len(biInvInd_dict[key])))
			for f in biInvInd_dict[key]:
				fp.write('%d %d\n' % (file_dict[f],biInvInd_dict[key][f]))

	return


def main():

	print('Start processing...')
	startTime=time.time()
	print('Start reading file list...')
	read_filelist()
	print('Finish reading in %s seconds' % (time.time()-startTime))
	build()
	print('Finish building in %s seconds' % (time.time()-startTime))
	write_file()
	print('Finish processing in %s seconds' % (time.time()-startTime))

	return

if __name__=='__main__':
	main()
