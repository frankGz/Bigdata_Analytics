import csv

csvfile = open('train.csv','r')
reader = csv.DictReader(csvfile)

# Add arff header
result = open('quoted-train.arff','w')
result.write('@RELATION train\n\n') 
result.write('@ATTRIBUTE text STRING\n') 
result.write('@ATTRIBUTE CLASS {negative,positive,neutral}\n') 
result.write('@ATTRIBUTE ID real\n\n')
result.write('@DATA\n')

for row in reader:
    # Take the original text, remove the apostrophe so that the short cut like 'don't' be 'dont'
    # Otherwise after the tokenlize the 'n' will be removed
    # Replace the line terminate to a space so that all text in a single review become one line.
    # Replace \ to \+space to make sure the emoj doesn't effect the line delima
    # Lower all text
    text = row['text'].replace('\'','').replace('\n',' ').replace('\\','\\ ').lower()
    
    # Add quote to each end
    result.write('\'' + text + '\',' + row['class'] + ',' + row['ID'] + '\n')
   
result.close()
csvfile.close()

