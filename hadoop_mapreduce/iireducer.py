#!/usr/bin/python
import sys

#global variable
isFirst = True
thisTerm = ""
lastTerm = ""
thisID = -1
lastID = -1
docIDs = []

#reducer function for this treducer
for line in sys.stdin:
	terms = line.replace('\n','').rsplit('\t', 1)
	thisTerm = terms[0] #key
	thisID = terms[1] #value
	if isFirst:
		isFirst = False
		lastTerm = thisTerm
		lastID = thisID
	if lastID not in docIDs:
		docIDs.append(lastID)
	if thisTerm != lastTerm:
		print(lastTerm + '\t' + str(docIDs))
		docIDs.clear()
	
	lastTerm = thisTerm
	lastID = thisID

#print the last key and value
if lastID not in docIDs:
	docIDs.append(lastID)
print(lastTerm + '\t' + str(docIDs))
docIDs.clear()