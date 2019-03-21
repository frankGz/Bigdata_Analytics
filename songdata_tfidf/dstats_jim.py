import csv

import sys

import numpy

import matplotlib.pyplot as pyplot



from nltk.corpus import stopwords

from nltk.tokenize import RegexpTokenizer

from collections import Counter



#global variable

tokenizer = RegexpTokenizer(r'\w+') # tokenizer used to get all words

stopWords = set(stopwords.words('english')) # use set to increase performance



class Artist:

    def __init__(self, name):

        self.song = []

        self.name = name

        self.wd_tot = 0

        

    def addSong(self, songObj):

        self.song.append(songObj)

        self.wd_tot = self.wd_tot + songObj.wd_count 



    def avgNumOfWords(self):

        return self.wd_tot / len(self.song)

    

class Song:

    def __init__(self, name, link, disc):

        self.name = name

        self.link = link

        wd_tokens = tokenizer.tokenize(e[descInd].lower()) #get all words

        filtered = [] # place non stopword

        #filter out all stopword

        for w in wd_tokens:

            if w not in stopWords:

                filtered.append(w)

        self.disc_dict = Counter(filtered)

        self.wd_count = len(self.disc_dict)



csvfile = open("songdata.csv", 'r')
row = csv.reader(csvfile)

count = -1 # count of songs

wd_count = 0 # count of words

# --------- index --------------

artistInd = 0 # index of artist

nameInd = 1 # index of song name

linkInd = 2 # index of link of song

descInd = 3 # index of song description

# --------- array --------------

artists = {} # use dictionary to increase performance

for e in row:

    count = count + 1

    if count == 0:

        continue # skip the header



    curr_song = Song(e[nameInd],e[linkInd],e[descInd])

    wd_count = wd_count + curr_song.wd_count

    add_art = True

        

    if e[artistInd] in artists:

        add_art = False

        artists[e[artistInd]].addSong(curr_song)

        

    if add_art:

        curr_artist = Artist(e[artistInd])

        curr_artist.addSong(curr_song)

        artists[e[artistInd]] = curr_artist



print("number of artists/bands in the collection:", len(artists))

print("number of songs in the collection:", count)

print("average number of songs per artist/band:", count/len(artists))

print("average number of unique words per song in the collection:", wd_count/count)

print("average number of unique words per song of an artist/band:")

    

art_wdct_list = []

for art in artists.values():

    art_wdct_list.append((art.name, art.avgNumOfWords()));

        

art_wdct_list.sort(key=lambda tup: tup[0], reverse=False)

for art_pair in art_wdct_list:

    print(art_pair)

    

# plot image

art_wdct_list.sort(key=lambda tup: tup[1], reverse=True)

    

top_ten_art = art_wdct_list[:10]

artNames = []

artAvgWd = []

for art_pair in top_ten_art:

    artNames.append(art_pair[0])

    artAvgWd.append(art_pair[1])

pyplot.bar(artNames, artAvgWd, width = 0.5)

pyplot.show()