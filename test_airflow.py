# Libraries for Airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from extract_tweets import tweetsToDB

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

# Define default args
default_args = {
    'owner': 'samivanecky',
    'depends_on_past': False,
    'email': 'sam.ivanecky3@gmail.com',
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes = 5)
}

# Define the DAG
dag = {
    'tutorial',
    default_args = default_args,
    max_active_runs = 1,
    schedule_interval = '*/10 * * * *'
}

# Define Python Operator
PythonOperator(
    dag = dag,
    task_id = 'test_python_run',
    provide_context = False,
    python_callable = tweetsToDB,
    op_args = ['arguments_passed_to_callable']
)
