#!/usr/bin/env python3
import sys
import csv
import pprint
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt
import operator 

print(sys.argv[1])
file = sys.argv[2]
with open(file,'r') as f:
    reader = csv.DictReader(file)
    artist = set()
    songs = []
    NumOfWords = []
    ArtistAndWords = {}
    ArtistAndSongs = {}
    pairsOfArtistAvgNumOfWords = {}
    
    reg = RegexpTokenizer(r'\w+')
    
    for row in reader:
        if row['artist'] not in artist:
            artist.add(row['artist'])
            ArtistAndWords[row['artist']] = 0
            ArtistAndSongs[row['artist']] = 0
            

        songs.append(row['song'])
        ArtistAndSongs[row['artist']] = ArtistAndSongs[row['artist']] + 1
            
        words = reg.tokenize(row['text'].lower())
        stops = set(stopwords.words('english'))
        
        unique_words = set()
        for word in words:
            if word not in stops:
                unique_words.add(word)

        NumOfWords.append(unique_words.__len__())
        ArtistAndWords[row['artist']] = ArtistAndWords[row['artist']] + unique_words.__len__()
    
        
    numOfArtists = artist.__len__()        
    numOfSongs = songs.__len__()
    avgNumOfSongs = numOfSongs / numOfArtists
    avgNumOfWords = sum(NumOfWords) / NumOfWords.__len__()
    
    
    for artist in sorted(ArtistAndSongs.keys()):
        # print("artist:",artist, "Words", ArtistAndWords[artist], "Songs", ArtistAndSongs[artist])
        pairsOfArtistAvgNumOfWords[artist] = ArtistAndWords[artist] / ArtistAndSongs[artist]


    sorted_pairsOfArtistAvgNumOfWords =  dict(sorted(pairsOfArtistAvgNumOfWords.items(),key = operator.itemgetter(0),reverse = False)[:10])

    
    
    print("numOfArtists",numOfArtists)
    print("numOfSongs",numOfSongs)
    print("avgNumOfSongs", avgNumOfSongs)
    print("avgNumOfWords", avgNumOfWords)
    print("pairsOfArtistAvgNumOfWords:")
    pprint.pprint(pairsOfArtistAvgNumOfWords)
    plt.bar(range(len(sorted_pairsOfArtistAvgNumOfWords)), list(sorted_pairsOfArtistAvgNumOfWords.values()), align='center')
    plt.xticks(range(len(sorted_pairsOfArtistAvgNumOfWords)), list(sorted_pairsOfArtistAvgNumOfWords.keys()))
    plt.show()
    
    
    