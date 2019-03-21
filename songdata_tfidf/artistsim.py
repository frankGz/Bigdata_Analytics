#!/usr/bin/env python3

import csv

import pprint

from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords

from nltk.tokenize import RegexpTokenizer

from collections import Counter

import operator 

import sys



#global variable

tokenizer = RegexpTokenizer(r'\w+') # tokenizer used to get all words

stopWords = stopwords.words('english')



def jaccard_similarity(list1, list2):

    intersection = len(list(set(list1).intersection(list2)))

    print(list(set(list1).intersection(list2)))

    union = (len(list1) + len(list2)) - intersection

    return float(intersection / union)



f = sys.argv[1]



id1_str = sys.argv[2]

id2_str = sys.argv[3]



id1 = int(id1_str)

id2 = int(id2_str) 



csvfile = open(f, 'r')

row = csv.reader(csvfile)

count = -1 # count of songs

wd_count = 0 # count of words

# --------- index --------------

artistInd = 0 # index of artist

nameInd = 1 # index of song name

linkInd = 2 # index of link of song

descInd = 3 # index of song description

# --------- array --------------

artistsProf = {}

for e in row:

    count = count + 1

    if count == 0:

        continue # skip the header



    if e[artistInd] in artistsProf.keys():

        artistsProf[e[artistInd]] = artistsProf[e[artistInd]] + "\n" + e[descInd] # string append lyric

    else:

        artistsProf[e[artistInd]] = e[descInd] # create pair



artistList = list(artistsProf.keys()) 

lyricList = list(artistsProf.values())



# initialize the TfidfVectorizer, subtract stop words, replace tf with 1 + log(tf).

tf = TfidfVectorizer(stop_words = stopWords, token_pattern=r'\w+', lowercase=True )

'''

What it does is tokenize the strings and give you a vector for each string,

each dimension of which corresponds to the number of times a token is found in the corresponding string. 

Most of the entries in all of the vectors will be zero, 

since only the entries which correspond to tokens found in that specific string will have positive values, 

but the vector is as long as the total number of tokens for the whole corpus.

'''

X =  tf.fit_transform(lyricList)

# Array mapping from feature integer indices to feature name, here are the words

feature_names = tf.get_feature_names() 



top100Words_collection = []



for j in range(0, len(artistList)):

    #doc = 0

    # tuple the pairs

    raw_dict = {}

    feature_index = X[j,:].nonzero()[1] 

    #(0, n). nonzero and select the 2nd col

    tfidf_scores = zip(feature_index, [X[j, x] for x in feature_index])

    for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:

        raw_dict[w] = s

    

    sorted_dict = dict(sorted(raw_dict.items(),key = operator.itemgetter(1),reverse = True)[:100])  

    #print("Profile of artist:", artistList[j]) 

    '''

    for r in sorted_dict.keys():

        print(r, "\t\t", sorted_dict[r])  

    '''

    top100Words_collection.append(list(sorted_dict.keys()))

           

    

print(list(artistsProf.keys())[id1],"-------",list(artistsProf.keys())[id2])

print(top100Words_collection[id1])

print(top100Words_collection[id2])   

print(jaccard_similarity(top100Words_collection[id1], top100Words_collection[id2]))

    

csvfile.close()