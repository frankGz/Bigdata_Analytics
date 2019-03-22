#for weka to convert arff
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
sentimentTags = ['positive','neutral','negative']

result = open('auto-analyze-full.csv','w')
result.write('ID,neg,neu,pos,compound,class\n')

csvfile = open('train.csv','r')
reader = csv.DictReader(csvfile)

for row in reader:
    value = sid.polarity_scores(row['text'])
    result.write(row['ID'] + ',' + str(value['neg']) + ',' + str(value['neu']) + ',' + str(value['pos']) + ',' + str(value['compound']) + ',' + row['class']+ '\n')
    
result.close()
csvfile.close()
'''
j48 68.5
bayesNet 68.6
nue 68.3

问题是暂时分别不出neutral
'''