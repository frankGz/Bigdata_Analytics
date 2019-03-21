# this code execute the actual function


from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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

sid = SentimentIntensityAnalyzer()
sentimentTags = ['_pos','_neu','_neg']

mytags = {'nvidia':['#nvidia','#nvda','#nvidiageforce','#rtx','#rtx2080','#rtx2080ti','#geforcertx','#rtx2070','#geforce'], \
          'microsoft':['#microsoft','#msft','#windows10','#windows','#surfacepro6','#surface','#outlook','#azure','#microsoftazure','#microsoftteam'], \
          'logitech':['#playadvanced','#logitechg','#logitech','#g502','#g903','#g933','#g533','#g402','#g602','#g305'], \
          'leagueoflegends':['#leagueoflegends','#neeko','#riotgames','#kda','#kdapopstars','#teamwwe','#artoflegends','#nalcs','#sktt1','#lck'], \
           'apple':['#apple','#aapl','#iphone','#ios','#iphonexs','#iphonexsmax','#mac','#osx','#ipad','#ipadpro'] \
    }

hashtag_sentiments = [t + s for t in mytags.keys() for s in sentimentTags]

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




def myFlatMap(line):
    compound = sid.polarity_scores(line)["compound"]
    if compound >= 0.25:
        sentiment =  sentimentTags[0] # positive
    elif compound <= -0.25:
        sentiment = sentimentTags[2] # negative
    else:
        sentiment = sentimentTags[1] # neutral
    return [word + sentiment for word in line.lower().split(" ")]

def myFilter(w):
    find = False
    for taglist in mytags.values():
        if w[0:-4] in taglist:
            find = True
    return find

def myMap(x):
    for topic in mytags.keys():
        if x[0:-4] in mytags[topic]:
            return (topic+x[-4:],1)


def send_tagCount_to_dashboard(tagCount):
    # extract the hashtags from dataframe and convert them into array
    top_tags = hashtag_sentiments
    # extract the counts from dataframe and convert them into array
    tags_count = tagCount
    # initialize and send the data through REST API
    # note: have to add 5 more colors in chart.html since only 10 are defined.
    url = 'http://dockerhost:5001/updateData'
    request_data = {'label': str(top_tags), 'data': str(tags_count)}
    response = requests.post(url, data=request_data)

# create csv file for recording 
f = open('partB.csv','w+')
s = "timestamp"
for topic in mytags.keys():
    s = s + ',' + topic + sentimentTags[0] + ',' + topic + sentimentTags[1] + ',' + topic + sentimentTags[2]
f.write(s + '\n')
f.close()

# split each tweet into words and add sentiment analyze
words = dataStream.flatMap(myFlatMap)

# filter the words to get only hashtags
hashtags = words.filter(myFilter)

# map each hashtag to be a pair of (hashtag,1)
hashtag_counts = hashtags.map(myMap)


# adding the count of each hashtag to its last count
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

# do the aggregation, note that now this is a sequence of RDDs
hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)

# process a single time interval
def process_interval(time, rdd):
    # print a separator
    print("----------- %s -----------" % str(time))
    try:#
        #write into the end of the file
        csv = open('partB.csv','a')
        #string for a row of csv
        row = str(time)
        
        tagCount = [] # for send to dash board
        
        #get dict from rdd
        m = rdd.collectAsMap()
        
        #constuct csv
        for tag in hashtag_sentiments:
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
        sorted_rdd = rdd.sortBy(lambda x:x[0], False)
        top5 = sorted_rdd.take(5)

        # print it nicely
        for tag in top5:
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