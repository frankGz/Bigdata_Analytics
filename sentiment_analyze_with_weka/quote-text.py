import csv

csvfile = open('train.csv','r')
reader = csv.DictReader(csvfile)

# Add arff header
arff_out = open('quoted-train.arff','w')
arff_out.write('@RELATION train\n\n')
arff_out.write('@ATTRIBUTE text STRING\n')
arff_out.write('@ATTRIBUTE CLASS {negative,positive,neutral}\n')
arff_out.write('@ATTRIBUTE ID real\n\n')
arff_out.write('@DATA\n')

# Add csv header
csv_out = open('quoted-train.csv','w')
csv_out.write('text,class,ID\n')


for row in reader:
    # Take the original text, remove the apostrophe so that the short cut like 'don't' be 'dont'
    # Otherwise after the tokenlize the 'n' will be removed
    # Replace the line terminate to a space so that all text in a single review become one line.
    # Replace \ to \+space to make sure the emoj doesn't effect the line delima
    # Replace comma to avoid splitting large number
    # Lower all text
    text = row['text'].replace('\'','').replace('\n',' ').replace('\\','\\ ').replace(',','').replace('-',' ').replace('_',' ').lower()

    # in case reviewer use word to give stars
    text.replace('one star', '1 star').replace('two starts', '2 stars').replace('three stars','3 stars').replace('four stars','4 stars').replace('five stars', '5 stars').replace('zero star','0 star')

    # Add quote to each end
    arff_out.write('\'' + text + '\',' + row['class'] + ',' + row['ID'] + '\n')
    csv_out.write('\'' + text + '\',' + row['class'] + ',' + row['ID'] + '\n')

arff_out.close()
csv_out.close()
csvfile.close()
