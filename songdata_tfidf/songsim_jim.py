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

allSongs = [] # list<Song>

#get command line argument

file = sys.argv[1]

song1_id = int(sys.argv[2])

song2_id = int(sys.argv[3])



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

        self.tfidf = tf * (math.log( (1 + doc_ct) / (1 + df)) + 1)



# Structure {name: string, link: string, disc: string, word_freq: list<WordTF>, word_profiled: set<string>}

class Song: 

    def __init__(self, name, link, disc):

        self.name = name

        self.link = link

        self.disc = disc #lyrics of this song

        self.word_freq = [] #word frequency for this song

        self.profile_max = 50

        self.word_profiled = set() #hold the top self.profile_max important word base on tfidf score

        

    def processFreq(self):

        self.word_freq.clear() #clear the content

        wd_tokens = tokenizer.tokenize(self.disc.lower()) #get all words

        filtered = [] # place non stopword

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

    def getProfile(self, song_ct):

        self.word_profiled.clear()

        tfidfs = []

        for term in self.word_freq:

            tfidfs.append(WordTFIDF(term.word.name, term.freq, term.word.freq, song_ct))

        tfidfs.sort(key=lambda wdtfidf: wdtfidf.tfidf, reverse=True)

        wd_count = 0

        for term in tfidfs:

            if wd_count >= self.profile_max:

                break

            self.word_profiled.add(term.name)

            wd_count = wd_count + 1

        

with open(file, 'r') as csvfile:

    row = csv.reader(csvfile)

    count = -1 # count of songs

    # --------- index --------------

    nameInd = 1 # index of song name

    linkInd = 2 # index of link of song

    descInd = 3 # index of song description



    for e in row:

        count = count + 1

        if count == 0:

            continue # skip the header

        curr_song = Song(e[nameInd],e[linkInd],e[descInd])

        allSongs.append(curr_song)

    

    if song1_id > count:

        print("song1_id is invalid !")

        exit(0)

    if song2_id > count:

        print("song2_id is invalid !")

        exit(0)

    if song1_id == song2_id:

        print("song1_id and song2_id can't be the same !")

        exit(0)

    

    #pre processing all term frequency and document frequency (must be done before calculate tfidf)

    for song in allSongs:

        song.processFreq()

    

    song_ct = len(allSongs)

    # calculate song1 word tfidf and get first 50 word with highest tfidf

    song1 = allSongs[song1_id]

    song1.getProfile(song_ct)

    # calculate song2 word tfidf and get first 50 word with highest tfidf

    song2 = allSongs[song2_id]

    song2.getProfile(song_ct)

    # calculate Jaccard index 

    intersect = song1.word_profiled.intersection(song2.word_profiled)

    union = song1.word_profiled.union(song2.word_profiled)

    JacIndex = len(intersect) / len(union)

    print('The similarity between song "' + song1.name + '" and "' + song2.name + '" is', JacIndex)

                

                