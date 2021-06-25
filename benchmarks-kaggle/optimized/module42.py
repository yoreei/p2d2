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

query = """
WITH projected_sentiments AS (
    SELECT hashtag, COALESCE(ol_score, ol_avg) AS ol_score
    FROM sentiment_values
), dropna_sentiments AS (
    SELECT hashtag, ol_score FROM projected_sentiments
    WHERE hashtag IS NOT NULL AND ol_score IS NOT NULL
), renamed_sentiments AS(
    SELECT hashtag, ol_score AS sentiment_score
    FROM dropna_sentiments
--), nlargest_sentiments AS (
--    SELECT * FROM renamed_sentiments
--    ORDER BY sentiment_score DESC
--    LIMIT 10


), dropna_user_track AS (
    SELECT * FROM user_track
    WHERE hashtag IS NOT NULL
), listof_popular_tracks_user_tracks AS (
    SELECT track_id FROM dropna_user_track
    GROUP BY track_id
    HAVING COUNT(track_id) > 50
),  popular_user_track AS (
    SELECT * FROM user_track
    WHERE track_id IN (SELECT * FROM listof_popular_tracks_user_tracks)
), sentiment_tracks AS (
    SELECT * FROM popular_user_track
    INNER JOIN renamed_sentiments 
    ON popular_user_track.hashtag = renamed_sentiments.hashtag


), 
listof_popular_tracks_content_features AS (
    SELECT track_id FROM context_content_features
    GROUP BY track_id
    HAVING COUNT(track_id) > 50
),  popular_content_features AS (
    SELECT * FROM context_content_features
    WHERE track_id IN (SELECT * FROM listof_popular_tracks_content_features)
), projected_content_features AS (
    SELECT instrumentalness, liveness, speechiness, danceability, valence, loudness, tempo, acousticness, energy, "mode", "key", artist_id, tweet_lang, track_id, created_at, lang, time_zone, user_id
    FROM popular_content_features
), dropna_content_features AS (
    SELECT * FROM projected_content_features
    WHERE instrumentalness IS NOT NULL AND
          liveness IS NOT NULL AND
          speechiness IS NOT NULL AND
          danceability IS NOT NULL AND
          valence IS NOT NULL AND
          loudness IS NOT NULL AND
          tempo IS NOT NULL AND
          acousticness IS NOT NULL AND
          energy IS NOT NULL AND
          "mode" IS NOT NULL AND
          "key" IS NOT NULL AND
          artist_id IS NOT NULL AND
          tweet_lang IS NOT NULL AND
          track_id IS NOT NULL AND
          created_at IS NOT NULL AND
          lang IS NOT NULL AND
          time_zone IS NOT NULL AND
          user_id IS NOT NULL
), rename_content_features AS (
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
english_content_features AS (
    SELECT * from rename_content_features
    WHERE time_zone IN ('Eastern Time', 'Central Time', 'Pacific Time', 'Mountain Time', 'Alaska Time', 'Hawaii Time')
    AND lang = 'en'

), joined AS (
    SELECT * FROM english_content_features
    INNER JOIN sentiment_tracks
    USING (track_id, created_at, user_id)
),
 df_mvp AS ( 
-- creating sentiment column while dropping:
-- hashtag, created_at, artist_id, tweet_lang, lang
    SELECT CASE
        WHEN sentiment_score >= 0.01 THEN 1
        ELSE 0
    END AS sentiment,
    sentiment_score, user_id, track_id, instrumentalness, liveness, speechiness, danceability, valence, loudness, tempo, acousticness, energy, "mode", "key", time_zone
    FROM joined
)


SELECT * FROM df_mvp;
"""

df_mvp = pd.read_sql_query(query, con=conn)
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock
df_mvp.to_csv('df_mvp_sql.csv', index=False)
# ML

