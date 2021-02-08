# Libraries for Airflow
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Libraries for Python script
import requests
import os
import pandas as pd
import numpy as np
import datetime
import json
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import psycopg2
from textblob import TextBlob
import yaml

import sys
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

# Define default args
default_args = {
    'owner': 'samivanecky',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes = 5)
}

# Define the DAG
dag = DAG(
    'tweet_airflow_test',
    default_args = default_args,
    max_active_runs = 1,
    schedule_interval = '*/2 * * * *',
    start_date = days_ago(1)
)

# Define Python Operator
BashOperator(
    task_id = 'test_airflow',
    bash_command = 'python /Users/samivanecky/airflow/pyfxns/extract_tweets.py',
    dag = dag
)
