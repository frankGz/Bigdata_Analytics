#!/usr/bin/python
import sys

#global variable
isFirst = True
termCt = 0
thisTerm = ""
lastTerm = ""

#reducer function for this treducer
file = open('trigrams.txt', 'w')
for line in sys.stdin:
	#get key and value part
	terms = line.replace('\n','').rsplit('\t', 1)
	thisTerm = terms[0]
	if isFirst:
		isFirst = False
		lastTerm = thisTerm
	if thisTerm != lastTerm:
		print(lastTerm + '\t' + str(termCt))
		termCt = 0
		
	lastTerm = thisTerm
	termCt = termCt + int(terms[1])

#print the last key and value
print(lastTerm + '\t' + str(termCt))
file.close()