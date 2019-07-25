#%%
from src.transforming import create_full_df, create_corpus, tokenize_corpus

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from nltk.tokenize import word_tokenize, punkt

import pandas as pd 
import numpy as np
from collections import Counter
import operator

#%%
data_path = '/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data_2'
df = create_full_df(data_path)
df.head()

#%%
#Join dataframe with features and user totals
totals = pd.read_csv('./user_totals.csv', header=0, names = ['user', 'user_posts', 'user_followers'])
complete_df = df.merge(totals, how = 'left', on='user')

#%%
X = complete_df.iloc[:,1:]
y = complete_df.iloc[:,0].values
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)

#%%
#Create Tf-idf vectorizer, transform data, 
# combine tf-idf vector and number of words to feed into model 
vector_train = TfidfVectorizer(min_df= 0.005)
caption_vector = vector_train.fit_transform(Xtrain['caption'])
vocab = vector_train.vocabulary_

vec_df = pd.DataFrame(caption_vector.todense(), index=Xtrain['caption'].index)
no_caption = Xtrain.iloc[:,2:]
train_x = vec_df.join(no_caption)


#%%
#Create Xtest vector from Xtrain vocabulary
vector_test = TfidfVectorizer(vocabulary=vocab)
caption_test_vector = vector_test.fit_transform(Xtest['caption'])
vec_test_df = pd.DataFrame(caption_test_vector.todense(), index=Xtest['caption'].index)
no_caption_test = Xtest.iloc[:,2:]
test_x = vec_test_df.join(no_caption_test)

#%%
#Random Forest Regression Model
rf = RandomForestRegressor(n_estimators = 50, max_features=0.33, n_jobs=-1)
rf.fit(train_x, ytrain)
print("Random Forest score:", rf.score(test_x, ytest))

'''Score of .61!!!!'''