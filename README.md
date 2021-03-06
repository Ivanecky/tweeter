# tweeter
## What is it?
The `tweeter` repository is a small project that was set up as a data engineering example. This project uses the Twitter API to read 100 tweets at a time, store the data in a local postgres table, and then perform analysis of the tweets in R.

## How does it work?
There are two files that are used by Airflow to read and store tweets from the Twitter API. The `extract_tweets.py` file executes the actual Python code used to access the Twitter API and store the data. In that file, there is some basic natural language processing done prior to uploading to postgres in order to alleviate future required analysis. The polarity and subjectivity of the tweets in both a rank and in a score are stored as new colunms. There is also a column to identify what word or phrase was queried from Twitter to be used as a key in conjuction with the created date. 

This file is executed using the  `test_airflow.py` file which runs on a local installation of Airflow. I initially set this up as a way to introduce myself to Airflow and to test it's capabilities. 

The `Tweet Analyis.Rmd` file was some basic EDA done on the data being pulled into the postgres database. I set up basic connections to the database with my credentials housed in local `yaml` files. In the example code, I aggregated the data for a specific term, cleaned up the text data to drop punctuation, stop words and whitespace, and then created a world cloud plot based on the most common words in the tweets.
