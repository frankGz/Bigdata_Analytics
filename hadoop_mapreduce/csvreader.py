import sys

record = [] #hold record data
currCell = ""
inQuote = False; #if current scope is inside quote
songId = 0

file = open('songdata.txt', 'w')
for line in sys.stdin:
	index = 0 #index of character for current string
	length = len(line) #string length of current line
	#loop for processing data in current line
	while index < length: 
		# if current scope is inside quote, then comma will seperate field
		if inQuote:
			if line[index] == '"': # if discover another quote inside a quote
				if index + 1 < length and line[index + 1] != '"': # if next character still inside scope of current line and it is not quote
					inQuote = False 
				else: #if next character still inside scope of current line and it is quote, then append 2 quote and jump 2 index
					currCell = currCell + line[index] 
					index = index + 2
					continue
			elif line[index] != '\n':
				currCell = currCell + line[index]
				
		# if current scope is not inside quote, then comma will seperate field
		else:
			if line[index] == '\n': #if not in quote and new line character reached
				record.append(currCell)
				# operation with record, id and content are seperated by dot
				if songId > 0: #skip the header
					file.write(str(songId) + '.' + record[3] + '\n')
				songId = songId + 1
				# end with operation with record
				currCell = ""
				record = [] # reset list to empty list
			elif line[index] == '"': #if inside quote then inQuote is true
				inQuote = True
			elif line[index] == ',':
				record.append(currCell) # append information to current record
				currCell = "" # clear field data and ready to next field
			else:
				currCell = currCell + line[index] # append character to current field

		index = index + 1

if len(record) != 0:
	if currCell != 0:
		record.append(currCell)
	songId = songId + 1
	file.write(str(songId) + '.' + record[3] + '\n')

file.close()
