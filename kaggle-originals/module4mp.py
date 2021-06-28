#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import helppd2sql


# In[2]:


sentiment_values = pd.read_csv('../data/chelseapower/fixed_sentiment_values.csv')


# In[3]:


proj_sent = sentiment_values[['hashtag', 'ol_score', 'ol_avg']]


# In[4]:


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


user_track = pd.read_csv('../data/chelseapower/user_track_hashtag_timestamp.csv')


# In[10]:


# explorative analysis - comment out for benchmark
# df2.apply(lambda x: x.isnull().sum())


# In[11]:


dropna_user = user_track.dropna(subset=['hashtag'])


# In[12]:


counts = dropna_user['track_id'].value_counts() # no CTE
popular = counts[counts >= 50] # no CTE
pop_user_list = popular.index


# In[13]:


pop_user = dropna_user[dropna_user['track_id'].
                                       isin(pop_user_list)]


# In[14]:


context_content_features = pd.read_csv(
    '../data/chelseapower/fixed_context_content_features.csv')


# In[15]:


counts3 = context_content_features['track_id'].value_counts() # no CTE
popular3 = counts3[counts3 >= 50] # no CTE
pop_context_list = popular3.index


# In[16]:


pop_context = context_content_features[context_content_features['track_id'].
                                       isin(pop_context_list)]


# In[17]:


# set(pop_context.columns) - {'coordinates','id',
#    'place','geo', 'created_at','artist_id','tweet_lang'}


# In[18]:


proj_context = pop_context.drop(
    columns=['coordinates','id','place','geo','artist_id','tweet_lang'])
helppd2sql.drop2select(proj_context)


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
helppd2sql.drop2select(english_context)


# In[23]:


usa_context = english_context[english_context['time_zone'].isin(
    ['Eastern Time', 'Central Time', 'Pacific Time',
     'Mountain Time', 'Alaska Time', 'Hawaii Time'])]


# In[24]:


df23 = usa_context.merge(
    pop_user, on=['track_id','created_at','user_id'], how='inner')


# In[25]:


df23_drop = df23.drop(columns=['created_at'])
helppd2sql.drop2select(df23_drop)


# In[ ]:


# Unsupported because df1 is in Python
df123 = dropna_sentiments.merge(df23, on=['hashtag'], how='inner')


# In[ ]:


# Unsupported because df123 is in Python
df123 = df123.drop(columns=['hashtag'])


# In[75]:


# Unsupported
df123['mode'] = df123['mode'].astype('Int64')
df123['user_id'] = df123['user_id'].astype(str)


# In[76]:


#Create new column sentiment that will be the predictor based on the sentiment_score values
df123['sentiment'] = np.where(df123['sentiment_score']>= 0.01, 1, 0)


# In[ ]:


# Reorder columns
df_mvp = df123[['sentiment','sentiment_score','user_id','track_id','time_zone','instrumentalness',
              'liveness','speechiness','danceability','valence','loudness','tempo','acousticness','energy','mode','key']]
df_mvp.info()


# In[ ]:


report = helppd2sql.global_report()
report_df = pandas.DataFrame(report)
report_df('pandas_report.csv', index=False)
exit()


# In[ ]:


# Create new dataset with only user_id, track_id and time_zone and the category variables
df_timezone = df_mvp.drop(['user_id','track_id','sentiment','sentiment_score','instrumentalness','liveness','speechiness',
                             'danceability','valence','loudness','tempo','acousticness','energy','mode','key'], axis=1)
df_timezone.head()


# In[ ]:


from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# One Hot Encode the category data set
one_hot_df = pd.get_dummies(df_timezone)
one_hot_df.head()


# In[ ]:


# Rename the columns
one_hot_df.columns = ['tz_Alaska_Time','tz_Central_Time','tz_Eastern_Time','tz_Hawaii_Time','tz_Mountain_Time','tz_Pacific_Time']
one_hot_df.head()


# In[ ]:


#Drop time_zone from MVP dataset
df_mvp = df_mvp.drop(["time_zone"], axis=1)


# In[ ]:


#Concatenate one hot encoded dataframe
df_mvp = pd.concat([df_mvp,one_hot_df], axis=1)
df_mvp.head()


# In[ ]:


df_mvp.to_csv('module4_cleaned.csv',index=False)


# ## Explore the data
# 
# * Look at the distribution for the data
# * Look for Multicollinearity
# * Remove unnecessary features
# * Balace and scale data

# In[ ]:


#Look at value counts of the predictor variable sentiment
df_mvp.sentiment.value_counts()


# In[ ]:


# Visualize the predictor variable
import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(x='sentiment', data=df_mvp, palette='hls')
plt.show()


# **Observation**: The data is very imbalanced and will need to be balanced.

# In[ ]:


# Create continuous dataset and look at distributions of data
df_mvp_lin = df_mvp.drop(['user_id','track_id','sentiment','mode','tz_Alaska_Time','tz_Central_Time','tz_Eastern_Time',
                          'tz_Hawaii_Time','tz_Mountain_Time','tz_Pacific_Time'], axis=1)
df_mvp_lin.hist(figsize = [30, 20]);


# In[ ]:


#Create coorelation heatmap and check for multicolinarity
from matplotlib import pyplot as plt
import seaborn as sns

correlation = df_mvp_lin.corr()
plt.figure(figsize=(14, 12))
heatmap = sns.heatmap(correlation, annot=True, linewidths=0, vmin=-1, cmap="RdBu_r")


# **Observation**: Loudness and Energy seem to be highly coorelated.
# 
# ## Logistic Regression
# * Normalize the data prior to fitting the model
# * Train-Test Split
# * Fit the model
# * Predict
# * Evaluate

# In[ ]:


# Define X and y
y = df_mvp['sentiment']
X = df_mvp.drop('sentiment', axis = 1)


# In[ ]:


# Normalizing the data prior to fitting the model.
x_feats = ['sentiment_score','instrumentalness','liveness','speechiness','danceability',
           'loudness','tempo','acousticness','energy','mode','key','valence','tz_Alaska_Time',
           'tz_Central_Time','tz_Eastern_Time','tz_Hawaii_Time','tz_Mountain_Time','tz_Pacific_Time']

X = pd.get_dummies(df_mvp[x_feats], drop_first=False)
y = df_mvp.sentiment
X.head()


# In[ ]:


from sklearn.model_selection import train_test_split

# Splitting the data into train and test sets (automatically uses stratified sampling by labels)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=42)


# In[ ]:


from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression(fit_intercept = True, C=1e12)
model_log = logreg.fit(X_train, y_train)
model_log


# In[ ]:


print(y_train.value_counts())
print(y_test.value_counts())


# In[ ]:


#Predict against test set using Sigmoid function
import time
start = time.time()

y_hat_test = logreg.predict(X_test)
y_hat_train = logreg.predict(X_train)

end = time.time()
print("Execution time:", end - start)


# In[ ]:


y_hat_test = logreg.predict_proba(X_test)
y_hat_test[0]


# In[ ]:


import time
start = time.time()

logreg.predict_proba(X_train)

end = time.time()
print("Execution time:", end - start)


# In[ ]:


# How may times was the classifier correct for the training set?
logreg.score(X_train, y_train)


# In[ ]:


# How may times was the classifier correct for the test set?
logreg.score(X_test, y_test)


# ### Classification Model Performance
# Check the precision, recall, and accuracy of the model.

# In[ ]:


# Function to calculate the precision
def precision(y_hat, y):
    y_y_hat = list(zip(y, y_hat))
    tp = sum([1 for i in y_y_hat if i[0]==1 and i[1]==1])
    fp = sum([1 for i in y_y_hat if i[0]==0 and i[1]==1])
    return tp/float(tp+fp)


# In[ ]:


# Function to calculate the recall
def recall(y_hat, y):
    y_y_hat = list(zip(y, y_hat))
    tp = sum([1 for i in y_y_hat if i[0]==1 and i[1]==1])
    fn = sum([1 for i in y_y_hat if i[0]==1 and i[1]==0])
    return tp/float(tp+fn)


# In[ ]:


# Function to calculate the accuracy
def accuracy(y_hat, y):
    y_y_hat = list(zip(y, y_hat))
    tp = sum([1 for i in y_y_hat if i[0]==1 and i[1]==1])
    tn = sum([1 for i in y_y_hat if i[0]==0 and i[1]==0])
    return (tp+tn)/float(len(y_hat))


# In[ ]:


# Calculate the precision, recall and accuracy of the classifier.
y_hat_test = logreg.predict(X_test)
y_hat_train = logreg.predict(X_train)

print('Training Precision: ', precision(y_hat_train, y_train))
print('Testing Precision: ', precision(y_hat_test, y_test))
print('\n')

print('Training Recall: ', recall(y_hat_train, y_train))
print('Testing Recall: ', recall(y_hat_test, y_test))
print('\n')

print('Training Accuracy: ', accuracy(y_hat_train, y_train))
print('Testing Accuracy: ', accuracy(y_hat_test, y_test))


# ### Resample data since it's imbalanced and all scores are very high.

# In[ ]:


# concatenate our training data back together
training_data = pd.concat([X_train, y_train], axis=1)


# In[ ]:


# separate minority and majority classes
not_safe = training_data[training_data.sentiment==0]
safe = training_data[training_data.sentiment==1]


# In[ ]:


from sklearn.utils import resample
# upsample minority
not_safe_upsampled = resample(not_safe, 
                              replace=True, # sample with replacement
                              n_samples=len(safe), # match number in majority class
                              random_state=42) # reproducible results


# In[ ]:


# combine majority and upsampled minority
upsampled = pd.concat([safe, not_safe_upsampled])


# In[ ]:


# check new class counts
print(upsampled.sentiment.value_counts())


# In[ ]:


sns.countplot(x='sentiment', data=upsampled, palette='hls')
plt.show()


# In[ ]:


X_train = upsampled.drop('sentiment', axis=1)
y_train = upsampled.sentiment


# In[ ]:


# Scaling X using StandardScaler
from sklearn.preprocessing import StandardScaler

# Only fit training data to avoid data leakage
scaler = StandardScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=list(X.columns))
X_test = pd.DataFrame(scaler.transform(X_test), columns=list(X.columns))
X_train.head()


# ### Run another Logistic Regression Model with resampled data

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

logreg2 = LogisticRegression(fit_intercept = True, C=1e12)
model_log = logreg2.fit(X_train, y_train)
model_log


# In[ ]:


print(y_train.value_counts())
print(y_test.value_counts())


# In[ ]:


# Predict against test set using Sigmoid function
import time
start = time.time()

y_hat_test = logreg2.predict(X_test)
y_hat_train = logreg2.predict(X_train)

end = time.time()
print("Execution time:", end - start)


# In[ ]:


y_hat_test = logreg2.predict_proba(X_test)
y_hat_test[0]


# In[ ]:


import time
start = time.time()

logreg2.predict_proba(X_train)

end = time.time()
print("Execution time:", end - start)


# In[ ]:


#Train score
logreg2.score(X_train, y_train)


# In[ ]:


#Test score
logreg2.score(X_test, y_test)


# In[ ]:


logreg2.coef_[0]


# In[ ]:


for feature, weight in zip(X.columns, logreg2.coef_[0]):
    print("{} has a weight of : {}".format(feature, weight))


# ### Confusion Matrix
# 
# Show the performance of the classification model.

# In[ ]:


#Create a Confusion Matrix
from sklearn.metrics import confusion_matrix

cnf_matrix = confusion_matrix(y_train, y_hat_train)
print('Confusion Matrix:\n',cnf_matrix)


# In[ ]:


#Plot the Confusion Matrix
import itertools
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.imshow(cnf_matrix,  cmap=plt.cm.Blues) #Create the basic matrix

#Add title and axis labels
plt.title('Confusion Matrix')
plt.ylabel('True label')
plt.xlabel('Predicted label')

#Add appropriate axis scales
class_names = set(y) #Get class labels to add to matrix
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names, rotation=45)
plt.yticks(tick_marks, class_names)

#Add Labels to each cell
thresh = cnf_matrix.max() / 2. #Used for text coloring below
#Here we iterate through the confusion matrix and append labels to our visualization
for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
        plt.text(j, i, cnf_matrix[i, j],
                 horizontalalignment="center",
                 color="white" if cnf_matrix[i, j] > thresh else "black")

#Add a side bar legend showing colors
plt.colorbar()


# In[ ]:


#conf_matrix function
def conf_matrix(y_true, y_pred):
    cm = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
    
    for ind, label in enumerate(y_true):
        pred = y_pred[ind]
        if label == 1:
            # CASE: TP 
            if label == pred:
                cm['TP'] += 1
            # CASE: FN
            else:
                cm['FN'] += 1
        else:
            # CASE: TN
            if label == pred:
                cm['TN'] += 1
            # CASE: FP
            else:
                cm['FP'] += 1
    return cm


# In[ ]:


#Set variable
model_confusion_matrix = conf_matrix(y_train, y_hat_train)


# In[ ]:


#Precision function
def precision(confusion_matrix):
    return confusion_matrix['TP'] / (confusion_matrix['TP'] + confusion_matrix['FP'])


# In[ ]:


#Recall function
def recall(confusion_matrix):
    return confusion_matrix['TP'] / (confusion_matrix['TP'] + confusion_matrix['FN'])


# In[ ]:


#Accuracy function
def accuracy(confusion_matrix):
    return (confusion_matrix['TP'] + confusion_matrix['TN']) / sum(confusion_matrix.values())


# In[ ]:


#f1 score
def f1(confusion_matrix):
    precision_score = precision(confusion_matrix)
    recall_score = recall(confusion_matrix)
    numerator = precision_score * recall_score
    denominator = precision_score + recall_score
    return 2 * (numerator / denominator)


# In[ ]:


from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

preds = [y_hat_train]

for ind, i in enumerate(preds):
    print('-'*40)
    print('Model Metrics:'.format(ind + 1))
    print('Precision: {}'.format(precision_score(y_train, i)))
    print('Recall: {}'.format(recall_score(y_train, i)))
    print('Accuracy: {}'.format(accuracy_score(y_train, i)))
    print('F1-Score: {}'.format(f1_score(y_train, i)))


# In[ ]:


from sklearn.metrics import classification_report

for ind, i in enumerate(preds):
    print('-'*40)
    print("Model Classification Report:".format(ind + 1))
    print(classification_report(y_train, i))


# ## Cross Validation
# Repeat a train-test-split creation 20 times, using a test_size of 0.05.

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
linreg = LinearRegression()
import matplotlib.pyplot as plt

num = 20
train_err = []
test_err = []
for i in range(num):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
    logreg2.fit(X_train, y_train)
    y_hat_train = logreg2.predict(X_train)
    y_hat_test = logreg2.predict(X_test)
    train_err.append(mean_squared_error(y_train, y_hat_train))
    test_err.append(mean_squared_error(y_test, y_hat_test))
plt.scatter(list(range(num)), train_err, label='Training Error')
plt.scatter(list(range(num)), test_err, label='Testing Error')
plt.legend();


# In[ ]:


#K-Fold Cross Validation
from sklearn.model_selection import cross_val_score

cv_5_results = np.mean(cross_val_score(logreg2, X, y, cv=5, scoring="accuracy"))
cv_10_results = np.mean(cross_val_score(logreg2, X, y, cv=10, scoring="accuracy"))
cv_20_results = np.mean(cross_val_score(logreg2, X, y, cv=20, scoring="accuracy"))

print(cv_5_results)
print(cv_10_results)
print(cv_20_results)


# ## Create a Sequential Neural Network
# - ReLU activation function
# - Sigmoid function on the output layer 

# In[ ]:


# Load libraries
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint

# split into input (X) and output (y) variables
X = pd.get_dummies(df_mvp[x_feats], drop_first=False)
y = df_mvp.sentiment


# In[ ]:


# define the keras model
model = Sequential()
model.add(Dense(12, input_dim=18, activation='relu'))
model.add(Dense(19, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


# In[ ]:


# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[ ]:


# Set callback functions to early stop training and save the best model so far
checkpoint = [ModelCheckpoint(filepath='models.hdf5', save_best_only=True, monitor='val_loss')]


# In[ ]:


# fit the keras model on the dataset
model.fit(X, y, epochs=10, callbacks=checkpoint, batch_size=100)


# In[ ]:


# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))


# ## Create a Sequential Neural Network with the scaled data
# - ReLU activation function
# - Sigmoid function on the output layer 

# In[ ]:


# split into input (X) and output (y) variables
X = pd.get_dummies(X_train, drop_first=False) #X_train = upsampled.drop('sentiment', axis=1)
y = y_train #y_train = upsampled.sentiment


# In[ ]:


# define the keras model
model2 = Sequential()
model2.add(Dense(12, input_dim=18, activation='relu'))
model2.add(Dense(8, activation='relu'))
model2.add(Dense(1, activation='sigmoid'))


# In[ ]:


# compile the keras model
model2.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[ ]:


# Set callback functions to early stop training and save the best model so far
checkpoint = [ModelCheckpoint(filepath='models.hdf5', save_best_only=True, monitor='val_loss')]


# In[ ]:


# fit the keras model on the dataset
model2.fit(X, y, epochs=10, callbacks=checkpoint, batch_size=100)


# In[ ]:


# evaluate the keras model
_, accuracy = model2.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

