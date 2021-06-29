echo "run as root"

for DBNAME in tpch1 tpch10 tpch100
do
    psql<<EOF
\c "${DBNAME}"
-----
-- Primary keys
ALTER TABLE region ADD PRIMARY KEY (r_regionkey);
ALTER TABLE nation ADD PRIMARY KEY (n_nationkey);
ALTER TABLE part ADD PRIMARY KEY (p_partkey);
ALTER TABLE supplier ADD PRIMARY KEY (s_suppkey);
ALTER TABLE partsupp ADD PRIMARY KEY (ps_partkey, ps_suppkey);
ALTER TABLE customer ADD PRIMARY KEY (c_custkey);
ALTER TABLE orders ADD PRIMARY KEY (o_orderkey);
ALTER TABLE lineitem ADD PRIMARY KEY (l_orderkey, l_linenumber);

------
-- microbenchmarks
CREATE UNIQUE INDEX IDX_ORDERS_ORDERKEY ON ORDERS (O_ORDERKEY);

CREATE INDEX IDX_LINEITEM_ORDERKEY ON LINEITEM (L_ORDERKEY);
CREATE INDEX IDX_LINEITEM_LINENUMBER ON LINEITEM (L_LINENUMBER);


-------
-- tpch
-- indexes on the foreign keys

CREATE INDEX IDX_SUPPLIER_NATION_KEY ON SUPPLIER (S_NATIONKEY);

CREATE INDEX IDX_PARTSUPP_PARTKEY ON PARTSUPP (PS_PARTKEY);
CREATE INDEX IDX_PARTSUPP_SUPPKEY ON PARTSUPP (PS_SUPPKEY);

CREATE INDEX IDX_CUSTOMER_NATIONKEY ON CUSTOMER (C_NATIONKEY);

CREATE INDEX IDX_ORDERS_CUSTKEY ON ORDERS (O_CUSTKEY);

CREATE INDEX IDX_LINEITEM_PART_SUPP ON LINEITEM (L_PARTKEY,L_SUPPKEY);

CREATE INDEX IDX_NATION_REGIONKEY ON NATION (N_REGIONKEY);

-- aditional indexes
CREATE INDEX IDX_LINEITEM_SHIPDATE ON LINEITEM (L_SHIPDATE, L_DISCOUNT, L_QUANTITY);

CREATE INDEX IDX_ORDERS_ORDERDATE ON ORDERS (O_ORDERDATE);

EOF
done


psql<<EOF
\c module4
-------
-- module4
CREATE UNIQUE INDEX IDX_SENTIMENT_HASHTAG ON sentiment_values(hashtag);

CREATE INDEX IDX_USER_HASHTAG ON user_track(hashtag);
CREATE INDEX IDX_USER_ID ON user_track(track_id);
	
CREATE INDEX IDX_CONTENT_TRACK_ID ON context_content_features(track_id);
CREATE INDEX IDX_CONTENT_LIVENESS ON context_content_features(liveness);
CREATE INDEX IDX_CONTENT_SPEECHINESS ON context_content_features(speechiness); 
CREATE INDEX IDX_CONTENT_DANCEABILITY ON context_content_features(danceability);
CREATE INDEX IDX_CONTENT_VALENCE ON context_content_features(valence);     
CREATE INDEX IDX_CONTENT_LOUDNESS ON context_content_features(loudness);    
CREATE INDEX IDX_CONTENT_TEMPO ON context_content_features(tempo);       
CREATE INDEX IDX_CONTENT_ACOUSTICNESS ON context_content_features(acousticness);
CREATE INDEX IDX_CONTENT_ENERGY ON context_content_features(energy);      
CREATE INDEX IDX_CONTENT_MODE ON context_content_features("mode");      
CREATE INDEX IDX_CONTENT_KEY ON context_content_features("key");       
CREATE INDEX IDX_CONTENT_ARTIST_ID ON context_content_features(artist_id);   
CREATE INDEX IDX_CONTENT_TWEET_LANG ON context_content_features(tweet_lang);  
CREATE INDEX IDX_CONTENT_CREATED_AT ON context_content_features(created_at);  
CREATE INDEX IDX_CONTENT_LANG ON context_content_features(lang);        
CREATE INDEX IDX_CONTENT_TIME_ZONE ON context_content_features(time_zone);   
CREATE INDEX IDX_CONTENT_USER_ID ON context_content_features(user_id);    

EOF
