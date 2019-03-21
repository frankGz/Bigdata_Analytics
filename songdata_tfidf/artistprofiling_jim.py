import csv

import sys

import numpy

import math



from nltk.corpus import stopwords

from nltk.tokenize import RegexpTokenizer

from collections import Counter



#global variable

tokenizer = RegexpTokenizer(r'\w+') # tokenizer used to get all words

stopWords = set(stopwords.words('english'))

allWords = {} # dictionary<string, WordDF>

artists = {} # dictionary<string, Artist>



# for document frequency of word, putted inside a list containing word for all document

# Structure {name: string, freq: number}

class WordDF: 

	def __init__(self, name):

		self.name = name

		self.freq = 1



# for term frequency of word, putted inside a list for song discription word list

# Structure {word: string, freq: number}

class WordTF:

	def __init__(self, word, freq):

		self.word = word # type of WordDF

		self.freq = freq # term frequency



class WordTFIDF:

	def __init__(self, name, tf, df, doc_ct):

		self.name = name # name of word

		#this method is followed on the tutorial provided

		#self.tfidf = (1 + math.log(tf, 10)) * (math.log( (1 + doc_ct) / (1 + df), 10) + 1)

		#this method is method implemented on TfidfVectorizer(stop_words = stopWords, token_pattern=r'\w+', lowercase=True), but the base may be different

		#difference is tf will be tf(from tutorial provided) / unique word count for this document

		self.tfidf = tf * (math.log( (1 + doc_ct) / (1 + df) ) + 1)



# Structure {name: string, lyrics: string, word_freq: list<WordTF>, word_profiled: list<WordTF>}

class Artist:

	def __init__(self, name):

		self.name = name

		self.lyrics = '' #all lyrics of song this artist sing (originally it is an empty string)

		self.word_freq = [] #word frequency for this artist (should be processed after add all songs)

		self.profile_max = 100

		self.word_profiled = set() #hold the top self.profile_max important word base on tfidf score

	

	# append lyrics to this artist lyrics

	def addSong(self, lyrics): 

		self.lyrics = self.lyrics + ' ' + lyrics.lower()

	

	# processing this song to get term frequency and document frequency (should be processed after add all songs)

	def processFreq(self):

		self.word_freq.clear() #clear the content

		wd_tokens = tokenizer.tokenize(self.lyrics) #get all words

		filtered = []

		#filter out all stopword

		for w in wd_tokens:

			if w not in stopWords:

				filtered.append(w)

		wd_tuples = Counter(filtered) #get raw count of word frequency

		tot_word = len(filtered)



		for tup in wd_tuples: #for all word token in current song 

			if tup in allWords:  #if word inside allWords dictionary

				wddf = allWords[tup] #get WordDF object coresspond to this word from allWords

				wddf.freq = wddf.freq + 1 #update document frequency for this word

				self.word_freq.append(WordTF(wddf, wd_tuples[tup] / tot_word))

			else:

				wddf = WordDF(tup) #create a new WordDF object for this word

				allWords[tup] = wddf #insert this word into allWords dictionary

				self.word_freq.append(WordTF(wddf, wd_tuples[tup] / tot_word))

	

	# get tfidf for this artist and return top self.profile_max important word base on tfidf score

	def getProfile(self, art_ct):

		tfidfs = []

		for term in self.word_freq:

			tfidfs.append(WordTFIDF(term.word.name, term.freq, term.word.freq, art_ct))

		tfidfs.sort(key=lambda wdtfidf: wdtfidf.tfidf, reverse=True)

		self.word_profiled = tfidfs[:self.profile_max]

	

csvfile = open("songdata.csv", 'r')

row = csv.reader(csvfile)



count = -1 # count of songs

# --------- index --------------

artistInd = 0 # index of artist

nameInd = 1 # index of song name

linkInd = 2 # index of link of song

descInd = 3 # index of song description



for e in row:

	count = count + 1

	if count == 0:

		continue # skip the header

	art_name = e[artistInd]

	lyrics = e[descInd]

	if art_name in artists: #if artist inside artists dictionary

		artists[art_name].addSong(lyrics)

	else: # if not

		curr_artist = Artist(art_name)

		curr_artist.addSong(lyrics)

		artists[art_name] = curr_artist

			

#process each artist to get term frequency and document frequency

for artist in artists:

	artists[artist].processFreq()



# print the profile of all artist

art_ct = len(artists)

for artist in artists:

	attist_obj = artists["Ariana Grande"]

	attist_obj.getProfile(art_ct) #get tfidf for this artist

	print("----------------------------------------------------------")

	print("Profiles of artist:" , attist_obj.name)

	for term in attist_obj.word_profiled:

		print(term.name,'\t\t',str(term.tfidf))