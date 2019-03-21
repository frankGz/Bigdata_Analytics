Part A:
1. Run docker for twitter app: docker run -it -v <PATH>:/app --name twitter -p 9009:9009 -w /app python bash
2. Install tweepy package: pip install -U git+https://github.com/tweepy/tweepy.git@2efe385fc69385b57733f747ee62e6be12a1338b
3. Run application: python twitter_app.py
4. Change the last line in app.py (not submitted), host to current ip addr and run dashboard web application: python <PATH>\TwitterStreaming-master\HashtagsDashboard\app.py
5. Run docker for spark app: docker run -it -v <PATH>:/app --link twitter:twitter --add-host="dockerhost:<YOUR IP ADDR>" -w /app eecsyorku/eecs4415
6. Run spark app: spark-submit spark_app_A.py

Note: Result will render on web page '<YOUR IP ADDR>:5001' in real time, use a broswer to see it. Also, a csv file 'partA.csv' will be created for batch process (haven't done the script for that since I finilly make the dashboard web app works). The submmitted 'partA.txt' contains exactly the same thing as 'partA.csv'.


Part B:
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

