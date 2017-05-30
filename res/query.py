import urllib.request
import operator
import unicodedata
import sys
from html.parser import HTMLParser

# Nick's Parser
class NParser(HTMLParser):
	_parsedData = ""
	_tagRemain = 0
	_tagWeWant = ["p", "title"]
	_title_done = False
	_titleWeight = 0
	def handle_starttag(self, tag, attrs):
		if (tag in self._tagWeWant):
			self._tagRemain = self._tagRemain + 1
	
	def handle_endtag(self, tag):
		if (tag in self._tagWeWant):
			self._tagRemain = self._tagRemain - 1
	
	def handle_data(self, data):
		if (self._tagRemain != 0):
			# return if data is javascript
			if ("script" in self.get_starttag_text()):
				return
			# replace special char
			replace = [b'\n', b'\r', b'\t', b'\xc2\xa0']
			byte = str.encode(data)
			for r in replace:
				byte = byte.replace(r, b' ')
			data = byte.decode("utf-8")
			# title can have a high weight
			if ("title" in self.get_starttag_text() and \
							not self._title_done):
				# do something
				self._parsedData = self._parsedData + data * self._titleWeight
				self._title_done = True
				return
			self._parsedData = self._parsedData + data

	def isChinese(self, word):
		return "CJK" in unicodedata.name(word)

	def isAlpha(self, word):
		return "LATIN" in unicodedata.name(word)

	def isDigit(self, word):
		return "DIGIT" in unicodedata.name(word)
	
	def getParsedData(self):
		parsedData = self._parsedData;
		# remove punc
		for word in parsedData:
			if (not (self.isChinese(word) or self.isAlpha(word))):
				parsedData = parsedData.replace(word, " ")
		return parsedData

MAXBYTE = 3000000
content = ""
index = 0
parser = NParser()

def getHTML(url):
	webPage = urllib.request.urlopen(url)
	return webPage.read(MAXBYTE).decode("utf-8")

def parseHTML(data):
	global parser
	parser.feed(data)
	return parser.getParsedData()

# get next word from content
def getWord():
	global parser, content, index
	if (index >= len(content)):
		return ""
	word = content[index]
	# ignore space
	while word == " ":
		index = index + 1
		if (index >= len(content)):
			return word
		word = content[index]
	# create word
	if (parser.isChinese(word)):
		index = index + 1
		return word
	else:	# English or Digit
		index = index + 1
		if index >= len(content):
			return word
		char = content[index]
		while (parser.isAlpha(char) or parser.isDigit(char)):
			word = word + char
			index = index + 1
			if index >= len(content):
				return word
			char = content[index]
		return word

def countWord(isUni):
	global content, index
	wordCount = {}
	last = len(content) if isUni else len(content) - 1
	while index < last:
		word = getWord()
		if not isUni:
			word2 = getWord()
			if len(word2) == 0:
				pass
			else:
				# add sapce between word and word2 if word2 is English or Digit
				word = word + word2 if (parser.isChinese(word2[0])) \
									else word + " " + word2
		# count word
		if (word in wordCount):
			wordCount[word] = wordCount[word] + 1
		else:
			wordCount[word] = 1
	return sorted(wordCount.items(), key = operator.itemgetter(1), reverse = True)

def getQuery(url, isUni, thres):
	global content
	data = getHTML(url)
	content = parseHTML(data)
	sortedWordCount = countWord(isUni)
	thres = len(sortedWordCount) if thres > len(sortedWordCount) else thres
	for i in range(0, thres):
		(word, count) = sortedWordCount[i]
		print(word)
	# list = makeQueryList()
	# return list

if __name__ == '__main__':
	'''
	Usage:
		getQuery(url, isUnigram, top)
	Parameters:
		url(string): url of the web page
		isUnigram(boolean): true returns unigram query, bigram otherwise
		top(int): number of key words to return
	Return:
		A list of key words in string
	'''
	arg = sys.argv
	getQuery(arg[1], False, int(arg[2]))
	# JP food
	#getQuery("http://hsing16.pixnet.net/blog/post/33292894", False, 20)
	# make notebook
	#getQuery("http://travelmous2013.pixnet.net/blog/post/411878827")
	# for testing other webpage
	#getQuery("https://www.dcard.tw/f")