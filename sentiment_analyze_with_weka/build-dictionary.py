#!/usr/bin/env python3
import csv
import re

from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


# get given stop words
lines = []
with open('stop_words.lst') as f:
    lines = f.readlines()
stops = [line.strip() for line in lines]


# initialize helper tools
tf = TfidfVectorizer(stop_words = stops, token_pattern=(r'[0-9]+[.]{1}[0-9]+|[0-9]+[/]{1}[0-9]+|\w+'), lowercase=True ) # regex: words + decimal + x/y
reg = RegexpTokenizer(r'[0-9]+[.]{1}[0-9]+|[0-9]+[/]{1}[0-9]+|\w+')
ps = PorterStemmer()

# porter stemmer for string
def stem_string(string):
    words = [ps.stem(w) for w in reg.tokenize(string)]
    str = ''
    for stemmed in words:
        str += stemmed + ' '
    return str

# regex rule for splitting, note: , \n . - are replaced by \s from previous script
#reg = '[;:\'\"\r\n\t\s\*]+'
#s = '5 star cut and color from cat...i love the feel of the shop. chitowns finest are definitely representing. when i came in i felt at home. everyone spoke even the clients. the service i received was great. cat was sure to check the length with me as she cut making sure it wasnt too short for me. the color i got was nice and i left the shop feeling like a new me! will definitely be back.'
#print(stem_string(s))

# for store the combined text
reviews = {'positive':'','negative':'','neutral':''}

# read csv 
file = open('quoted-train.csv','r')
csvfile = csv.DictReader(file)
for row in csvfile:
    stemmed = stem_string(row['text'])
    reviews[row['class']] += stemmed + ' '
    #print(row['class'] + '.....' + stemmed)
    
file.close()

X =  tf.fit_transform(reviews.values())

# Array mapping from feature integer indices to feature name, here are the words
feature_names = tf.get_feature_names() 

test = open('check-text.txt','w')
for wo in feature_names:
    test.write(wo + '\n')
test.close()
