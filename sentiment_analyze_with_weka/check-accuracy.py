import csv
from nltk.chunk.util import accuracy

original = open('train.csv','r')
f1 = csv.DictReader(original)

senti_orig = []
senti_auto = []

for row in f1:
    senti_orig.append(row['class'])
    
original.close()

auto = open('auto-analyze.csv','r')
f2 = csv.DictReader(auto)

for row2 in f2:
    senti_auto.append(row['class'])

same = 0
for i in range(0,senti_auto.__len__()):
    if(senti_auto[i]==senti_orig[i]):
        same+=1
print(same)
print(senti_auto.__len__())
accu = float(same) / float(senti_auto.__len__())
print(accu)

'''
22341
40000
0.558525
'''