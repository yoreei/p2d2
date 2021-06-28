#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import helppd2sql
import pandas
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=module4 user=disable_nestloop_user password=disable_nestloop_user")


proj_sent_query = """
    SELECT hashtag, ol_score, ol_avg
    FROM sentiment_values;
"""

cte_statements = """
WITH 
dropna_user AS (
    SELECT * FROM user_track
    WHERE hashtag IS NOT NULL
), 
pop_user_list AS (
    SELECT track_id FROM dropna_user
    GROUP BY track_id
    HAVING COUNT(track_id) >= 50
),  
pop_user AS (
    SELECT * FROM dropna_user
    WHERE track_id IN (SELECT * FROM pop_user_list)
),

 
pop_context_list AS (
    SELECT track_id FROM context_content_features
    GROUP BY track_id
    HAVING COUNT(track_id) >= 50
),  
pop_context AS (
    SELECT * FROM context_content_features
    WHERE track_id IN (SELECT * FROM pop_context_list)
), 
proj_context AS (
    SELECT -- drop 'coordinates','id','place','geo','artist_id','tweet_lang'
        "instrumentalness", "liveness", "speechiness", 
        "danceability", "valence", "loudness", 
        "tempo", "acousticness", "energy", 
        "mode", "key", "track_id", 
        "created_at", "lang", "time_zone", 
        "user_id"
    FROM pop_context
), 
dropna_context AS (
    SELECT * FROM proj_context
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
    SELECT * from dropna_context
    WHERE lang = 'en'
),
rename_content_features AS (
    SELECT -- drop "lang"
        "instrumentalness", "liveness", "speechiness",
        "danceability", "valence", "loudness",
        "tempo", "acousticness", "energy",
        "mode", "key", "track_id",
        "created_at", "user_id",
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
    FROM english_context
),
usa_context AS (
    SELECT * FROM rename_content_features
    WHERE time_zone IN ('Eastern Time', 'Central Time', 'Pacific Time', 'Mountain Time', 'Alaska Time', 'Hawaii Time')
), 
df23 AS (
    SELECT * FROM usa_context
    INNER JOIN pop_user
    USING (track_id, created_at, user_id)
),
df23_drop AS(
    SELECT -- drop created_at
        "instrumentalness", "liveness", "speechiness", 
        "danceability", "valence", "loudness", 
        "tempo", "acousticness", "energy", 
        "mode", "key", "track_id", 
        "time_zone", "user_id", "hashtag"
    FROM df23
)
"""
report = helppd2sql.new_report()
for cte in ['dropna_user', 'pop_user_list', 'pop_user', 'pop_context_list',
            'pop_context', 'proj_context', 'dropna_context', 'english_context',
            'rename_content_features', 'usa_context', 'df23', 'df23_drop']
    cte_query = cte_statements + "select * from " + cte + ";"
    start_clock = time.perf_counter()
    df = pd.read_sql_query(cte_query, con=conn)
    helppd2sql.report_add(report, cte, df)
    calc_time = time.perf_counter() - start_clock
    print(f"{cte} calc_time")
report_df = pandas.DataFrame(report)
report_df('sql_report.csv', index=False)

