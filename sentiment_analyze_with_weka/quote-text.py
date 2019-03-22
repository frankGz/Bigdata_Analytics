# add quote to each text so that weka can recognize string
import csv

csvfile = open('train.csv','r')
reader = csv.DictReader(csvfile)

result = open('quoted-train.csv','w')
result.write('text,class,ID\n')

for row in reader:
    result.write('\'' + row['text'].replace('\'','').replace('\n',' ').replace('\\','\\ ') + '\',' + row['class'] + ',' + row['ID'] + '\n')
   
result.close()
csvfile.close()

