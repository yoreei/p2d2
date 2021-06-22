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

# Subqueries
# joined_df = pd.read_sql_query("""
# SELECT FROM 
#     (SELECT * FROM user_track) as user_track_p2d2
# 
# 
# """

# CTEs
joined_df = pd.read_sql_query("""
WITH projected_sentiments AS (
    SELECT hashtag, COALESCE(ol_score, ol_avg) AS ol_score
    FROM sentiment_values
), dropna_sentiments AS (
    SELECT * FROM projected_sentiments
    WHERE hashtag IS NOT NULL AND ol_score IS NOT NULL
), nlargest_sentiments AS (
    SELECT * FROM dropna_sentiments
    ORDER BY ol_score
    LIMIT 10


), dropna_user_track AS (
    SELECT * FROM user_track
    WHERE hashtag IS NOT NULL
), listof_popular_tracks_user_tracks AS (
    SELECT track_id FROM dropna_user_track
    GROUP BY track_id
    HAVING COUNT(track_id) > 50
),  popular_user_track AS (
    SELECT * FROM user_track
    WHERE track_id IN (SELECT * FROM listof_popular_tracks)
), sentiment_tracks AS (
    SELECT * FROM popular_user_track
    INNER JOIN dropna_sentiments
    ON hashtag


), listof_popular_tracks_content_features AS (
    SELECT track_id FROM content_features
    GROUP BY track_id
    HAVING COUNT(track_id) > 50
),  popular_content_features AS (
    SELECT * FROM content_features
    WHERE track_id IN (SELECT * FROM listof_popular_tracks_content_features)
), projected_content_features AS (
    SELECT instrumentalness, liveness, speechiness, danceability, valence, loudness, tempo, acousticness, energy, "mode", "key", artist_id, tweet_lang, track_id, created_at, lang, time_zone, user_id
    FROM popular_content_features
), dropna_content_features AS (
    SELECT * FROM projected_content_features
   -- WHERE #TODO SEE WHERE NULLS
), english_content_features AS (
    SELECT * FROM dropna_content_features
    WHERE lang = 'en'
), joined AS (
    SELECT * FROM english_content_features AS c
    INNER JOIN sentiment_tracks AS s
    ON c.track_id = s.track_id AND
       c.created_at = s.created_at AND
       c.user_id = s.user_id
), case_joined AS ( -- creating sentiment column while dropping hashtag, created_at, artist_id, tweet_lang, lang
    SELECT CASE
        WHEN sentiment_score >= 0.01 THEN 1
        ELSE 0
    END AS sentiment,
    sentiment_score, user_id, track_id, instrumentalness, liveness, speechiness, danceability, valence, loudness, tempo, acousticness, energy, "mode", "key", time_zone, sentiment
    FROM joined
), dropna_joined AS (
    SELECT * FROM case_joined
   -- WHERE # TODO see which ones have nulls
), timezone_fixed_join AS (
    SELECT CASE
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
    END AS time_zone,
    sentiment, sentiment_score, user_id, track_id, instrumentalness, liveness, speechiness, danceability, valence, loudness, tempo, acousticness, energy, "mode", "key", sentiment
    WHERE time_zone IN ('Eastern Time', 'Central Time', 'Pacific Time', 'Mountain Time', 'Alaska Time', 'Hawaii Time')
  )

-- We could also fork timezone_fixes_join and drop 
--['user_id','track_id','sentiment','sentiment_score','instrumentalness','liveness','speechiness', 'danceability','valence','loudness','tempo','acousticness','energy','mode','key']
-- but that would increase network cost


SELECT * FROM timezone_fixed_join;

"""

#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock
# ML

action(joined)
