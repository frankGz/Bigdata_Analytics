
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
sentimentTags = ['positive','neutral','negative']

result = open('auto-analyze.csv','w')
result.write('ID,class\n')

csvfile = open('train.csv','r')
reader = csv.DictReader(csvfile)

for row in reader:
    compound = sid.polarity_scores(row['text'])["compound"]
    if compound >= 0.25:
        sentiment =  sentimentTags[0] # positive
    elif compound <= -0.25:
        sentiment = sentimentTags[2] # negative
    else:
        sentiment = sentimentTags[1] # neutral

    result.write(row['ID'] + ',' + sentiment + '\n')

result.close()
csvfile.close()