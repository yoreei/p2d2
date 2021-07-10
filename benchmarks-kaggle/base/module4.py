import time
start_clock = time.perf_counter()

import numpy as np # linear algebra
import pandas 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

sentiment_values = pandas.read_sql_query('select * from sentiment_values', con=CONNSTR)
user_track = pandas.read_sql_query('select * from user_track', con=CONNSTR)
context_content_features = pandas.read_sql_query('select * from context_content_features', con=CONNSTR)

SHARED_DB_TIME.value = time.perf_counter() - start_clock
print(f"db_time: {SHARED_DB_TIME}")

proj_sent = sentiment_values[['hashtag', 'ol_score', 'ol_avg']]


# proj_sent.apply(lambda x: x.isnull().sum())


# In[5]:


# COALESCE (ol_score, ol_avg) NOT SUPPORTED YET
proj_sent['ol_score'] = proj_sent['ol_score'].combine_first(
    proj_sent['ol_avg'])


# In[6]:


# proj_sent.apply(lambda x: x.isnull().sum())


# In[7]:


# UNREACHABLE
dropna_sentiments = proj_sent.dropna(axis = 0, how ='any')


# In[8]:


# UNREACHABLE
dropna_sentiments.rename(columns = {'ol_score':'sentiment_score'}, inplace = True)


# In[9]:




# In[10]:


# explorative analysis - comment out for benchmark
# df2.apply(lambda x: x.isnull().sum())


# In[11]:


dropna_user = user_track.dropna(subset=['hashtag'])


# In[12]:


counts = dropna_user['track_id'].value_counts()
popular = counts[counts >= 50]
pop_user_list = popular.index


# In[13]:


pop_user = dropna_user[dropna_user['track_id'].
                                       isin(pop_user_list)]


# In[36]:




# In[65]:


counts3 = context_content_features['track_id'].value_counts()
popular3 = counts3[counts3 >= 50]
pop_context_list = popular3.index


# In[66]:


print(len(context_content_features))
print(len(pop_context_list))
print(len(counts3))


# In[67]:


pop_context = context_content_features[context_content_features['track_id'].
                                       isin(pop_context_list)]


# In[68]:


len(pop_context)


# In[17]:


# set(pop_context.columns) - {'coordinates','id',
#    'place','geo', 'created_at','artist_id','tweet_lang'}


# In[18]:


proj_context = pop_context.drop(
    columns=['coordinates','id','place','geo','artist_id','tweet_lang'])
# helppd2sql.drop2select(proj_context)


# In[19]:


# proj_context.apply(lambda x: x.isnull().sum())


# In[20]:


dropna_context = proj_context.dropna(subset=
                 ['instrumentalness', 'liveness', 'speechiness',
                  'danceability', 'valence', 'acousticness',
                  'energy', 'mode', 'key', 'time_zone', 'user_id'])


# Reduced the dataset from 10,887,911 to **6,413,576** by dropping all null value rows.

# In[21]:


english_context = dropna_context[dropna_context['lang'] == 'en']


# In[22]:


# CTE rename_context
english_context = english_context.drop(columns=['lang'])
english_context['time_zone'].replace('Eastern Time (US & Canada)', 'Eastern Time', inplace=True)
english_context['time_zone'].replace('Central Time (US & Canada)', 'Central Time', inplace=True)
english_context['time_zone'].replace('Pacific Time (US & Canada)', 'Pacific Time', inplace=True)
english_context['time_zone'].replace('Mountain Time (US & Canada)', 'Mountain Time', inplace=True)
english_context['time_zone'].replace('Alaska', 'Alaska Time', inplace=True)
english_context['time_zone'].replace('Hawaii', 'Hawaii Time', inplace=True)
english_context['time_zone'].replace('Arizona', 'Mountain Time', inplace=True)
english_context['time_zone'].replace('America/Chicago', 'Central Time', inplace=True)
english_context['time_zone'].replace('America/New_York', 'Eastern Time', inplace=True)
english_context['time_zone'].replace('America/Los_Angeles', 'Pacific Time', inplace=True)
english_context['time_zone'].replace('America/Denver', 'Mountain Time', inplace=True)
english_context['time_zone'].replace('America/Detroit', 'Eastern Time', inplace=True)
# helppd2sql.drop2select(english_context)


# In[23]:


usa_context = english_context[english_context['time_zone'].isin(
    ['Eastern Time', 'Central Time', 'Pacific Time',
     'Mountain Time', 'Alaska Time', 'Hawaii Time'])]


# In[24]:


df23 = usa_context.merge(
    pop_user, on=['track_id','created_at','user_id'], how='inner')


# In[25]:


df23_drop = df23.drop(columns=['created_at'])
# helppd2sql.drop2select(df23_drop)


# In[ ]:

# print(f"python_time: {calc_time}")
# 
# env = globals().copy()
# report = helppd2sql.global_report(env)
# report_df = pandas.DataFrame(report)
# report_df.to_csv('pandas_report.csv', index=False)
# df23_drop.to_csv('df23_drop_p.csv', index=False)

SHARED_WALL_TIME.value = time.perf_counter() - start_clock
