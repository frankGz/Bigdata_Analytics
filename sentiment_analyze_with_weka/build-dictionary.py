#!/usr/bin/env python3
import csv
import re
import operator

from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet as wn
'''
unigram - 1000:    70
unigram - 1500:    69
bigram - 1000:    70
'''

# porter stemmer for string
def stem_string(string):
    # words = [ps.stem(w) for w in reg.tokenize(string)]
    words = [w for w in reg.tokenize(string)]
    words_cleanned = []
    for word in words:
        if word not in stop_words:
            words_cleanned.append(ps.stem(word))
    ori_text.append(set(words_cleanned))
    str = ''
    for stemmed in words_cleanned:
        if len(stemmed) > 1:
            str += stemmed + ' '
            unique_words.add(stemmed)
    return str

# get given stop words
lines = []
with open('stop_words.lst') as f:
    lines = f.readlines()
stops = [line.strip() for line in lines]
# add common food words to stops
food = wn.synset('food.n.02')
foods = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
stop_words = [s.lower() for s in stops] + [f.lower() for f in foods]


# initialize helper tools
tf = TfidfVectorizer(token_pattern=(r'[0-9]?[.]?[0-9]?\sstar|[0-9]+[/]{1}[0-9]+|\w+'), ngram_range=(1, 1), lowercase=True, sublinear_tf=True) # regex: words + decimal + x/y
reg = RegexpTokenizer(r'[0-9]?[.]?[0-9]?\sstar|[0-9]+[/]{1}[0-9]+|\w+')
ps = PorterStemmer()

# for store the combined text
reviews = {'positive':'','negative':'','neutral':''}
# store the result from tfidf transform
keywords = {'positive':list(),'negative':list(),'neutral':list()}
# dictionary words set
words_set = set()
# unique_words
unique_words = set()
# save quoted-train.csv in memory
ori_text = []
ori_class = []
ori_ID = []

# read csv 
print('read from quoted-train.csv')
file = open('quoted-train.csv','r')
csvfile = csv.DictReader(file)
print('do porter stemming...')
for row in csvfile:
    #ori_text.append(row['text'])
    ori_class.append(row['class'])
    ori_ID.append(row['ID'])
    stemmed = stem_string(row['text'])
    reviews[row['class']] += stemmed + ' '
    #print(row['class'] + '.....' + stemmed)
    
file.close()
print('porter stemming done. Unique words: ',len(unique_words))

# do tfidf transform
print('do tfidf analyze...')
X =  tf.fit_transform(reviews.values())
feature_names = tf.get_feature_names() 
for j in range(0, 3):
    #doc = 0
    # tuple the pairs
    raw_dict = {}
    feature_index = X[j,:].nonzero()[1] 
    #(0, n). nonzero and select the 2nd col
    tfidf_scores = zip(feature_index, [X[j, x] for x in feature_index])
    for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
        raw_dict[w] = s
    
    sorted_dict = dict(sorted(raw_dict.items(),key = operator.itemgetter(1),reverse = True)[:1500])  
    print("working on: ", list(reviews.keys())[j]) 
    for r in sorted_dict.keys():
        #test.write(str(r) + "\t\t" + str(sorted_dict[r]) + '\n')  
        keywords[str(list(reviews.keys())[j])].append(str(r))
print('tfidf analyze done.')

# build the dictionary, remove common element
print('building dictionary...')
sentiment = list(reviews.keys())
for m in range(0,3):
    for word in keywords[str(sentiment[m])]:
        if not (word in keywords[str(sentiment[(m+1)%3])] and word in keywords[str(sentiment[(m+2)%3])]):
            words_set.add(word)
print('unique key words: ', len(words_set))
dictionary = open('words_dictionary.txt','w')
for words in words_set:
    dictionary.write(words + '\n')
print('dictionary saved -- words_dictionary.txt')

# build mapping csv based on dictionary
print('constructing mapping csv...')
vectorlized_train = open('vectorlized_train.csv','w')
header = 'ID,CLASS,'
for keys in  words_set:
    header += keys + ','
vectorlized_train.write(header[:-1] + '\n')
for i in range(0,len(ori_ID)):
    #print('working on line ',i)
    # construct single line binary
    line = ori_ID[i] + ',' + ori_class[i] + ','
    for word in words_set:
        if word in ori_text[i]:
            line += 'yes,'
        else:
            line += 'no,'
    vectorlized_train.write(line[:-1] + '\n')
print('saved mapping csv -- vectorlized_train.csv')
print('Finished')