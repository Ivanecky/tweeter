# Import libraries
# import requests
# import os
# import pandas as pd
# import numpy as np
# import datetime
# import json
# import matplotlib.pyplot as plt
# import seaborn as sns
# import nltk
# from nltk.tokenize import word_tokenize, RegexpTokenizer
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# import psycopg2
# from textblob import TextBlob
# import yaml
# from sqlalchemy import create_engine

# One big wrapper function
def tweetsToDB():
    # Read data via yaml files
    with open(r'postgres.yaml') as file:
        psql = yaml.full_load(file)
    with open(r'api.yaml') as file:
        api_yaml = yaml.full_load(file)

    tokenizer = RegexpTokenizer(r'\w+')

    # Connect to postgres
    conn = psycopg2.connect(
        host=psql['host'],
        database=psql['database'],
        user=psql['user'],
        port=psql['port'])

    # Keys & creds
    api_key = api_yaml['api_key']
    api_secret = api_yaml['api_secret']
    bearer_token = api_yaml['bearer_token']

    # Create requests headers
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    # Functions to get sentiment and subjectivity
    def getSentiment(polarity):
        if polarity > 0.2:
            return("Positive")
        elif polarity < -0.2:
            return("Negative")
        else:
            return("Neutral")
        
    def getSubjectivity(subjectivity):
        if subjectivity > 0.5:
            return("Subjective")
        else:
            return("Objective")

    # Setup connection to tweeter DB
    # Create engine string
    connect_str = 'postgresql+psycopg2://' + psql['user'] + '@' + psql['host'] + '/' + psql['database'] 

    # Create engine connection
    engine = create_engine(connect_str)

    c = engine.connect()
    conn = c.connection

    # Function to send request, get data, create df, and append
    def getNewTweets(searchTxt, searchDropWords):
        # Define text to search for
        searchTxt = searchTxt

        # Define query
        query = "{} -is:retweet".format(searchTxt)

        # Define tweet fields
        tweet_fields = "tweet.fields=text,author_id,geo,created_at,public_metrics"

        # Define max results
        max_results = 100
        mrf = "max_results={}".format(max_results)

        # Define URL
        url = "https://api.twitter.com/2/tweets/search/recent?{}&query={}&{}".format(mrf, query, tweet_fields)

        # Submit request
        resp = requests.request("GET", url, headers=headers)
        
        # Convert data to dataframe
        respJSON = resp.json()
        temp_df = pd.json_normalize(respJSON['data'])
        
        # Define token list
        words = []

        # Iterate through dataframe and tokenize each tweet. Append to one long token.
        for index, row in temp_df.iterrows():
            try:
                token = tokenizer.tokenize(row.text.lower()) # Use lowercase for future analysis. Using this tokenize method to drop punctuation
                words = words + token
            except:
                print("Something went wrong trying to tokenize...")
        
        # Iterate over sentences and get polarity and sensitivity, as well as rating
        # Define vectors to hold values
        polar_vals = []
        subject_vals = []
        polar_ratings = []
        subject_ratings = []

        # Loop
        for index, row in temp_df.iterrows():
            blob = TextBlob(row.text)
            polar_vals.append(blob.sentiment.polarity)
            subject_vals.append(blob.sentiment.subjectivity)
            polar_ratings.append(getSentiment(blob.sentiment.polarity))
            subject_ratings.append(getSubjectivity(blob.sentiment.subjectivity))

        # Assign values to df cols
        temp_df['polarity'] = polar_vals
        temp_df['subjectivity'] = subject_vals
        temp_df['polarity_rank'] = polar_ratings
        temp_df['subjectivity_rank'] = subject_ratings

        # Add a column to call out what word was searched for
        temp_df['search_word'] = searchTxt

        # Write temp data to database
        temp_df.to_sql('tweets', engine, if_exists='append')
        
        # if df.empty:
        #     return temp_df
        # else:
        #     dfs = [df, temp_df]
        #     df = pd.concat(dfs, ignore_index=True)
        #     # Drop duplicates
        #     df = df.drop_duplicates(subset=['id'], keep='first')
        #     return(df)
        
    # Test run to get tweets
    searchTxt = 'cross country'
    searchDropWords = ['cross country', 'xc']
    getNewTweets(searchTxt, searchDropWords)

