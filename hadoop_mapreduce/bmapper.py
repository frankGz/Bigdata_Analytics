#!/usr/bin/python
import sys

#all stopwords list
stopWords = {'a', 'b', 'c', 'f', 'g', 'h', 'l', 'n', 'p', 'q', 'r', 'u', 'v', 'w', 'x', 'z', 'until', 'be', 'weren', 't', "she's", 'or', 'all', "you'd", 'ourselves', 'their', 'were', 're', "it's", 'his', 'into', 'hasn', 'where', "doesn't", "mightn't", 'above', 'doesn', 'her', 'should', 'a', "you're", 'as', 'no', 'not', 'ours', 'each', 'but', 'you', 'do', 'out', "you'll", 'm', 'while', 'again', 'so', 'which', 'll', "shouldn't", 'theirs', 'when', "wouldn't", 'isn', 'from', 'shouldn', 'down', 'doing', 'those', 'yours', 'there', 'its', "needn't", 'if', 'any', 'same', 'off', "hasn't", 'once', 'over', 'had', 'about', 'by', 'further', 'and', 'who', 'won', 'some', 'against', "mustn't", 'himself', 'ma', 'ain', 'then', 'being', 'how', 'why', "shan't", 'myself', 'for', 'during', 'nor', 'we', 'whom', 'herself', 'own', 'such', 'very', "should've", 'shan', 'they', 'wasn', 'the', "you've", 'yourself', 'just', 'most', 'other', "wasn't", 'needn', 'than', 'now', 'me', "didn't", 'our', 'have', 'is', 'my', 'at', 'because', 'through', "won't", 'can', 'yourselves', 'has', 'am', 'in', 'too', 'she', 'are', 'few', 'didn', 's', 'them', 'y', 'does', 'been', "don't", 'themselves', 'will', "couldn't", 'was', 'hers', 'what', 'up', 'here', 'that', 'of', 'having', 'with', 'more', 'aren', "hadn't", 'this', 'these', 'hadn', 'o', 'itself', 'did', "aren't", 'd', 'e', 'it', 'your', 'after', "weren't", 'don', 'before', 'he', 'him', 've', 'under', "isn't", 'wouldn', 'an', 'mustn', "that'll", 'only', 'on', 'haven', 'couldn', "haven't", 'mightn', 'between', 'both', 'to', 'i', 'j', 'below','chorus'}
#regex of [a-z0-9'], since it will convert to lowercase so only lowercase is ok
wdletter = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "'"}
#for numbers
num = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

#adjust start index and end index of the word (used by tokenize function)		
def getWd(stInd, fnInd, line):
	while line[fnInd] == "'":
		fnInd = fnInd - 1
	return line[stInd:fnInd+1]

#function for tokenize string (will remove all single letter word because it is stopword)
def tokenize(line):
	line = line.lower() # remove all new line character and to lowercase
	splited = []
	stInd = 0 #start index of word (inclusive)
	fnInd = 0 #end index of word (inclusive)
	inWord = False #flag for whether current index inside word
	i = 0 #index of character for current string
	length = len(line) #string length of current line
	while i < length:
		if inWord: #if current index is inside a word
			if line[i] not in wdletter: #if character is not valid english word letter (include number)
				inWord = False
				fnInd = i - 1
				if fnInd == stInd and line[stInd] not in num: #if it is only one letter word (which is stop word)
					pass
				else:
					splited.append(getWd(stInd, fnInd, line))
		else: #if current index is not inside a word
			if line[i] != "'": #first letter can't be single quote
				if line[i] in wdletter: #if character is valid english word letter (include number)
					inWord = True
					stInd = i
			#else skip to next character
		i = i + 1
	return splited

class RingArray:
	def __init__(self, capacity):
		self.capacity = capacity #maximum capacity
		self.value = []
		self.cursor = 0
	
	def push(self, element):
		if len(self.value) < self.capacity:
			self.value.append(element)
		else:
			self.value[self.cursor] = element
		self.cursor = (self.cursor + 1) % self.capacity
			
	def size(self):
		return len(self.value)
	
	def toString(self):
		result = ""
		if len(self.value) < self.capacity:
			for e in self.value:
				result = result + e + " "
			
		else:
			i = self.cursor
			j = 0
			while j < self.capacity:
				if j == self.capacity - 1:
					result = result + self.value[i]
				else:
					result = result + self.value[i] + " "
				i = (i + 1) % self.capacity
				j = j + 1
		return result

#mapper function for this umapper
for line in sys.stdin:
	brigram = RingArray(2)
	term = line.split('.', 1)
	lyric = term[1]
	wd_tokens = tokenize(lyric)
	for w in wd_tokens:
		if w not in stopWords:
			brigram.push(w)
			if brigram.size() == 2:
				print(brigram.toString() + '\t' + '1')