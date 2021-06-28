#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2
import time

start_clock = time.perf_counter()
conn = psycopg2.connect(f"host=localhost dbname=module4 user=root password=root")
# variable CONN should be provided by the overseeing script. See benchmarker/main.py

### Tables and their columns:

# # context_content_features
# coordinates     
# instrumentalness
# liveness        
# speechiness     
# danceability    
# valence         
# loudness        
# tempo           
# acousticness    
# energy          
# mode            
# key             
# artist_id       
# place           
# geo             
# tweet_lang      
# track_id        
# created_at      
# lang            
# time_zone       
# user_id         
# id

# # sentiment_values
# hashtag    
# vader_score
# afinn_score
# ol_score   
# ss_score   
# vader_min  
# vader_max  
# vader_sum  
# vader_avg  
# afinn_min  
# afinn_max  
# afinn_sum  
# afinn_avg  
# ol_min     
# ol_max     
# ol_sum     
# ol_avg     
# ss_min     
# ss_max     
# ss_sum     
# ss_avg

# # user_track
# user_id   
# track_id  
# hashtag   
# created_at
# CTEs

query1 = """
    SELECT hashtag, ol_score, ol_avg
    FROM sentiment_values;
"""

query2 = """
WITH 
dropna_user AS (
    SELECT * FROM user_track
    WHERE hashtag IS NOT NULL
), 
pop_user_list AS (
    SELECT track_id FROM dropna_user_track
    GROUP BY track_id
    HAVING COUNT(track_id) => 50
),  
pop_user AS (
    SELECT * FROM user_track
    WHERE track_id IN (SELECT * FROM listof_popular_tracks_user_tracks)
),

 
pop_context_list AS (
    SELECT track_id FROM context_content_features
    GROUP BY track_id
    HAVING COUNT(track_id) => 50
),  
pop_context AS (
    SELECT * FROM context_content_features
    WHERE track_id IN (SELECT * FROM pop_context_list)
), 
proj_context AS (
    SELECT 
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "key",
        "lang",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "time_zone",
        "track_id",
        "user_id",
        "valence"
), 
dropna_context AS (
    SELECT * FROM projected_content_features
    WHERE 
        "instrumentalness" IS NOT NULL AND
        "liveness" IS NOT NULL AND
        "speechiness" IS NOT NULL AND
        "danceability" IS NOT NULL AND
        "valence" IS NOT NULL AND
        "acousticness" IS NOT NULL AND
        "energy" IS NOT NULL AND
        "mode" IS NOT NULL AND
        "key" IS NOT NULL AND
        "time_zone" IS NOT NULL AND
        "user_id" IS NOT NULL
), 
english_context AS (
    SELECT * from rename_content_features
    AND lang = 'en'
),
rename_content_features AS (
    SELECT instrumentalness, liveness, speechiness, danceability, valence, loudness, tempo, acousticness, energy, "mode", "key", artist_id, tweet_lang, track_id, created_at, lang, user_id,
    CASE
        WHEN time_zone = 'Eastern Time (US & Canada)' THEN 'Eastern Time'
        WHEN time_zone = 'Eastern Time (US & Canada)' THEN 'Eastern Time'
        WHEN time_zone = 'Central Time (US & Canada)' THEN 'Central Time'
        WHEN time_zone = 'Pacific Time (US & Canada)' THEN 'Pacific Time'
        WHEN time_zone = 'Mountain Time (US & Canada)' THEN 'Mountain Time'
        WHEN time_zone = 'Alaska' THEN 'Alaska Time'
        WHEN time_zone = 'Hawaii' THEN 'Hawaii Time'
        WHEN time_zone = 'Arizona' THEN 'Mountain Time'
        WHEN time_zone = 'America/Chicago' THEN 'Central Time'
        WHEN time_zone = 'America/New_York' THEN 'Eastern Time'
        WHEN time_zone = 'America/Los_Angeles' THEN 'Pacific Time'
        WHEN time_zone = 'America/Denver' THEN 'Mountain Time'
        WHEN time_zone = 'America/Detroit' THEN 'Eastern Time'
    END AS time_zone
    FROM dropna_content_features
),
usa_context AS (
    SELECT * FROM rename_content_features
    WHERE time_zone IN ('Eastern Time', 'Central Time', 'Pacific Time', 'Mountain Time', 'Alaska Time', 'Hawaii Time')
), 
df23 AS (
    SELECT * FROM popular_user_track
    INNER JOIN sentiment_tracks
    USING (track_id, created_at, user_id)
)

SELECT * FROM df23;
"""

df_mvp = pd.read_sql_query(query, con=conn)
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock
df_mvp.to_csv('df_mvp_sql.csv', index=False)
# ML

