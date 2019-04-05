Hadoop MapReduce HDFS
-----------

## running in docker environment docker pull eecsyorku/eecs4415:latest(python3 and HDFS installed)	 	 
-----------

## Distributed Text Analytics using Python
* Distributed Computation of n-grams
	*  compute the number of occurrences of each unigram in the song collection (umapper.py, ureducer.py) and output the results in a file called unigrams.txt
	*  compute the number of occurrences of each bigram in the song collection (bmapper.py, breducer.py) and output the results in a file called bigrams.txt
	*  compute the number of occurrences of each trigram in the song collection (tmapper.py, treducer.py) and output the results in a file called trigrams.txt
	*  how would you modify these scripts in order to compute the frequency of each of the quantities
	*  (instead of the number of occurrences)? Provide a short answer in plain text (up to half a page) with the name frequency-computation.txt
* Distributed Computation of k-skip-n-gram
	*  compute the number of occurrences of each 1-skip-2-gram in the song collection (skipgrammapper.py, skipgramreducer.py) and output the results in a file called skipgrams.txt
* Distributed Construction of an Inverted Index
	*  compute the inverted index of the song collection (iimaper.py, iireducer.py) and output the results in a file called inverted-index.txt
