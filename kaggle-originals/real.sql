WITH 
dropna_user AS (
    SELECT * FROM user_track
    WHERE hashtag IS NOT NULL
), 
counts AS (
    SELECT track_id, count(*) AS count_col FROM dropna_user
    GROUP BY track_id
),
popular AS (
    SELECT track_id, count_col FROM counts
    WHERE count_col >= 50
),
pop_user_list AS (
    SELECT track_id FROM popular
),
pop_user AS (
    SELECT * FROM dropna_user
    WHERE track_id IN (SELECT * FROM pop_user_list)
),


counts3 AS (
    SELECT track_id, count(*) AS count_col FROM context_content_features
    GROUP BY context_content_features
),
popular3 AS (
    SELECT track_id, count_col FROM counts3
    WHERE count_col >= 50
),
pop_context_list AS (
    SELECT track_id FROM popular3
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
