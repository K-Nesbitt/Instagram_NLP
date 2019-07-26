#%%
from src.transforming import create_full_df

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import confusion_matrix

import pandas as pd 
import numpy as np


#%%
data_path = '/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data_2'
data = create_full_df(data_path)
data.head()

#%%

target = data['number_of_likes'].apply(lambda x: 0 if x <= data.user_avg_likes[x] else 1)

X = data.iloc[:, 1:]
y = target.values
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)

#%%
#Create Tf-idf vectorizer, transform data, 
# combine tf-idf vector and number of words to feed into model 
vector_train = TfidfVectorizer(min_df= 0.0010)
caption_vector = vector_train.fit_transform(Xtrain['caption'])
vocab = vector_train.vocabulary_

vec_df = pd.DataFrame(caption_vector.todense(), index=Xtrain['caption'].index)
no_caption = Xtrain.iloc[:,1:]
train_x = vec_df.join(no_caption)


#%%
#Create Xtest vector from Xtrain vocabulary
vector_test = TfidfVectorizer(vocabulary=vocab)
caption_test_vector = vector_test.fit_transform(Xtest['caption'])
vec_test_df = pd.DataFrame(caption_test_vector.todense(), index=Xtest['caption'].index)
no_caption_test = Xtest.iloc[:,1:]
test_x = vec_test_df.join(no_caption_test)

#%%
#Random Forest Regression Model
rf = RandomForestRegressor(n_estimators = 25, max_features=0.33, n_jobs=-1)
rf.fit(train_x, ytrain)
print("Random Forest score:", rf.score(test_x, ytest))


#%%
'''Score of .61 with min_df=0.005, 10 trees, no user information
    Score of .535 with min_df=0.005, 10 trees and user information
    Score of .545 with min_df=0.005, 50 trees and user information 
    
    Score of .606 with min_df = 0.0025, 50 trees, user information
    Score of .601 with min_df=0.0025, 25 trees, user information '''

#%%

rfc = RandomForestClassifier(n_estimators=25, n_jobs=-1)
rfc.fit(train_x, ytrain)

print("Random Forest Classifier score:", rfc.score(test_x, ytest))

'''Classifier score of .891 with 25 trees
    only 25% of the data is over the mean therefore it is easier
    to predict
    
    Classifer score of .901 with 25 trees and min_df .0025, 
    score of .908 with min_df = 0.005
    score of .907 with min_df = 0.0010'''
#%%
ytrue = rfc.predict(test_x)
confusion_matrix(ytest, ytrue).ravel()

#%%
