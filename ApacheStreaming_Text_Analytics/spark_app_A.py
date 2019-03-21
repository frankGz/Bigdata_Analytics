# this code execute the actual function


from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests


# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from spark context, interval size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter",9009)

# reminder - lambda functions are just anonymous functions in one line:
#
#   words.flatMap(lambda line: line.split(" "))
#
# is exactly equivalent to
#
#    def space_split(line):
#        return line.split(" ")
#
#    words.filter(space_split)

# split each tweet into words
words = dataStream.flatMap(lambda line: line.lower().split(" "))

# set csv header and hashtag list
mytags = ['#job','#traffic','#happythanksgiving','#hawks','#blackfriday']

f = open('partA.csv','w+')
s = "timestamp"
for tag in mytags:
    s = s + ',' + tag

f.write(s + '\n')
f.close()


# filter the words to get only hashtags
hashtags = words.filter(lambda w: w in mytags)


# map each hashtag to be a pair of (hashtag,1)
hashtag_counts = hashtags.map(lambda x: (x, 1))


# adding the count of each hashtag to its last count
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)


# do the aggregation, note that now this is a sequence of RDDs
hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)



def send_tagCount_to_dashboard(tagCount):
    # extract the hashtags from dataframe and convert them into array
    top_tags = mytags
    # extract the counts from dataframe and convert them into array
    tags_count = tagCount
    # initialize and send the data through REST API
    url = 'http://dockerhost:5001/updateData'
    request_data = {'label': str(top_tags), 'data': str(tags_count)}
    response = requests.post(url, data=request_data)

# process a single time interval
def process_interval(time, rdd):

    # print a separator
    print("----------- %s -----------" % str(time))
    try:#
        #write into the end of the file
        csv = open('partA.csv','a')
        #string for a row of csv
        row = str(time)
    
        tagCount = []
        
        #get dict from rdd
        m = rdd.collectAsMap()
        
        #constuct csv
        for tag in mytags:
            if tag in m.keys():
                row = row + ',' +  str(m[tag])
                tagCount.append(m[tag])
            else:
                row = row + ',' + '0'
                tagCount.append('0')
        csv.write(row + '\n')
        csv.close()
        # sort counts (desc) in this time instance and take top 10
        # sorted_rdd = rdd.sortBy(lambda x:x[1], False)
        sorted_rdd = rdd.sortBy(lambda x:x[1], False)
        top10 = sorted_rdd.take(5)
        

        # print it nicely
        for tag in top10:
            print('{:<40} {}'.format(tag[0], tag[1]))
        
        send_tagCount_to_dashboard(tagCount)
            
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)
    
    
    
    
    
    

# do this for every single interval
hashtag_totals.foreachRDD(process_interval)



# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()

