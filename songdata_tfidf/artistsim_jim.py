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



#get command line argument

file = sys.argv[1]

artist1_id = int(sys.argv[2])

artist2_id = int(sys.argv[3])



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



# Structure {name: string, lyrics: string, word_freq: dict<string, WordTF>}

class Artist:

    def __init__(self, name, id):

        self.id = id

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

        wd_tuples = Counter(filtered) # variable for Term(word) Frequency

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

        self.word_profiled.clear()

        tfidfs = []

        for term in self.word_freq:

            tfidfs.append(WordTFIDF(term.word.name, term.freq, term.word.freq, art_ct))

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

    wd_count = 0 # count of words

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

        add_art = True

        if art_name in artists: #if artist inside artists dictionary

            artists[art_name].addSong(lyrics)

        else: # if not

            artist_id = len(artists)

            curr_artist = Artist(art_name, artist_id)

            curr_artist.addSong(lyrics)

            artists[art_name] = curr_artist



    if artist1_id > count:

        print("artist1_id is invalid !")

        exit(0)

    if artist2_id > count:

        print("artist2_id is invalid !")

        exit(0)

    if artist1_id == artist2_id:

        print("artist1_id and artist2_id can't be the same !")

        exit(0)

    

    artist1 = Artist('', -1) #dummy artist

    artist2 = artist1 #dummy artist

    

    #post processing of each artist to get term frequency and document frequency

    for artist_name in artists:

        artist = artists[artist_name]

        artist.processFreq()

        if artist.id == artist1_id:

            artist1 = artist

        if artist.id == artist2_id:

            artist2 = artist



    art_ct = len(artists)

    # calculate artist1 word tfidf and get first 100 word with highest tfidf

    artist1.getProfile(art_ct)

    # calculate artist2 word tfidf and get first 100 word with highest tfidf

    artist2.getProfile(art_ct)

    # calculate Jaccard index 

    intersect = artist1.word_profiled.intersection(artist2.word_profiled)

    union = artist1.word_profiled.union(artist2.word_profiled)

    JacIndex = len(intersect) / len(union)

    print('The similarity between artist "' + artist1.name + '" and "' + artist2.name + '" is', JacIndex)

    

    