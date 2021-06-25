#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2
import time

start_clock = time.perf_counter()
conn = psycopg2.connect(CONNSTR)
# variable CONN should be provided by the overseeing script. See benchmarker/main.py
sentiment_values_df = pd.read_sql_query("SELECT * FROM sentiment_values", conn)
user_track_df = pd.read_sql_query("SELECT * FROM user_track", conn)
content_features_df = pd.read_sql_query("SELECT * FROM content_features", conn)

#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock

sentiment_values_df = sentiment_values_df.drop(columns=['vader_min','vader_max','vader_sum','afinn_min','afinn_max','afinn_sum','ol_min','ol_max','ol_sum','ss_min','ss_max','ss_sum', 'vader_score','afinn_score','ss_score','vader_avg','afinn_avg','ol_avg','ss_avg'])

#Fill in missing ol_score with ol_avg score, if available
sentiment_values_df['ol_score'] = sentiment_values_df.apply(
    lambda row: row['ol_avg'] if np.isnan(row['ol_score']) else row['ol_score'],
    axis=1
)

sentiment_values_df = sentiment_values_df.dropna()

print (sentiment_values_df.nlargest(10, 'ol_score'))

user_track_df = user_track_df.dropna()

# Select the items where the track_id count is less than 50 and remove them
counts = user_track['track_id'].value_counts()
user_track = user_track[~user_track['track_id'].isin(counts[counts < 50].index)]

sentiment_df = sentiment_values.merge(user_track, on='hashtag')

# Select the items where the track_id count is less than 50 and remove them
counts = content_features['track_id'].value_counts()
content_features_df = content_features_df[~content_features_df['track_id'].isin(counts[counts < 50].index)]

content_features_df = content_features.drop(columns=['coordinates','id','place','geo'])
content_features_df = content_features_df.dropna()
content_features_df = content_features_df[content_features_df['lang'] == 'en']
joined = sentiment_df.merge(content_features_df, on=['track_id','created_at','user_id'])
joined['sentiment'] = np.where(df4['sentiment_score']>= 0.01, 1, 0)
joined = df4.dropna()

joined = joined.drop(columns=['hashtag','created_at','artist_id','tweet_lang','lang'])
joined['time_zone'].replace('Eastern Time (US & Canada)', 'Eastern Time',inplace=True)
joined['time_zone'].replace('Central Time (US & Canada)', 'Central Time',inplace=True)
joined['time_zone'].replace('Pacific Time (US & Canada)', 'Pacific Time',inplace=True)
joined['time_zone'].replace('Mountain Time (US & Canada)', 'Mountain Time',inplace=True)
joined['time_zone'].replace('Alaska', 'Alaska Time',inplace=True)
joined['time_zone'].replace('Hawaii', 'Hawaii Time',inplace=True)
joined['time_zone'].replace('Arizona', 'Mountain Time',inplace=True)
joined['time_zone'].replace('America/Chicago', 'Central Time',inplace=True)
joined['time_zone'].replace('America/New_York', 'Eastern Time',inplace=True)
joined['time_zone'].replace('America/Los_Angeles', 'Pacific Time',inplace=True)
joined['time_zone'].replace('America/Denver', 'Mountain Time',inplace=True)
joined['time_zone'].replace('America/Detroit', 'Eastern Time',inplace=True)

joined = joined[joined['time_zone'].isin(['Eastern Time','Central Time','Pacific Time','Mountain Time','Alaska Time','Hawaii Time']

# ML

action(joined)
