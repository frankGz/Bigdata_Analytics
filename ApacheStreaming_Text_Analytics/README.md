Hadoop MapReduce HDFS
-----------
#### running in docker environment (python3, HDFS, and Apache Spark installed)
	 docker pull eecsyorku/eecs4415:latest
-----------
## Streaming Text Analytics using Python
*  Identifying Trends in Twitter (Part A)
	A Twitter streaming application that tracks specific hashtags and reports their popularity (# occurrences) in real-time. I
	*  Identify 5 related #hashtags
	*  Collect tweets mentioning any of the 5 #hashtags in real-time
	*  Compute the number of occurrences of each of the mentioned hashtags
	*  Plot the results of your analysis in real-time. Alternatively, you can decide to store the results in a file, post-process them as a batch (offline) and create a plot based on the post-process analysis. The results are based on the time window that your application is running (from the time it begins, until it is killed or interrupted/stopped).
* Real-time Sentiment Analysis of Twitter Topics (Part B)
	a Twitter streaming application that performs sentiment analysis of tweets related to competitive topics and provides a real-time monitoring of the polarity.
	*  Identify 5 competitive topics
	*  Manually select a set of 10 hashtags that better describe each of the topic identified above
	*  Collect tweets related to the 5 topics in real-time and perform sentiment analysis for each topic
	*  Plot the results of your analysis in real-time. Alternatively, you can decide to store results in afile, post-process them and create a plot based on the post-process analysis

## How to use (with docker):
### Part A
	1. Run docker for twitter app: docker run -it -v <PATH>:/app --name twitter -p 9009:9009 -w /app python bash
	2. Install tweepy package: pip install -U git+https://github.com/tweepy/tweepy.git@2efe385fc69385b57733f747ee62e6be12a1338b
	3. Run application: python twitter_app.py
	4. Change the last line in app.py (not submitted), host to current ip addr and run dashboard web application: python <PATH>\TwitterStreaming-master\HashtagsDashboard\app.py
	5. Run docker for spark app: docker run -it -v <PATH>:/app --link twitter:twitter --add-host="dockerhost:<YOUR IP ADDR>" -w /app eecsyorku/eecs4415
	6. Run spark app: spark-submit spark_app_A.py
###Part B
	1. Run docker for twitter app: docker run -it -v <PATH>:/app --name twitter -p 9009:9009 -w /app python bash (stop and delete the previous container if you have went through Part A to avoid port binding errors)
	2. Install tweepy package: pip install -U git+https://github.com/tweepy/tweepy.git@2efe385fc69385b57733f747ee62e6be12a1338b
	3. Run application: python twitter_app.py
	4. Change the last line in app.py (not submitted), host to current ip addr and run dashboard web application: python <PATH>\TwitterStreaming-master\HashtagsDashboard\app.py
	5. Run docker for spark app: docker run -it -v <PATH>:/app --link twitter:twitter --add-host="dockerhost:<YOUR IP ADDR>" -w /app eecsyorku/eecs4415
	6. Install nltk package and download data: pip install nltk
	6.1 Run python: python
	6.2 :>> import nltk
	6.3 :>> nltk.download('vader_lexicon')
	6.4 :>> exit()
	7. Run spark app: spark-submit spark_app_B.py

Note: Result will render on web page '<YOUR IP ADDR>:5001' in real time, use a broswer to see it. To see every bar in different color, add 5 extra colors in chart.html, or the last 5 bars will be displayed in gray. Also, a csv file 'partB.csv' will be created for batch process (haven't done the script for that since I finilly make the dashboard web app works). The submmitted 'partA.txt' contains exactly the same thing as 'partB.csv'.
	