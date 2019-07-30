#%%
from src.transforming import create_full_df

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

import pandas as pd 
import numpy as np


#%%
#Create dataframe from files in folder. 
data_path = '/Users/keatra/Galvanize/Projects/Instagram_NLP/users'
data = create_full_df(data_path)
data.head()

#%%
#Create a target label for above or below average number of likes. 
target = data['number_of_likes'].apply(lambda x: 1 if x > data.user_avg_likes[x] else 0)

X = data.iloc[:, 1:]
y = target.values
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)

#%%
#Create Tf-idf vectorizer, transform data, 
# combine tf-idf vector and other features to feed into model 
vector_train = TfidfVectorizer(min_df= 0.0025)
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
#Feed in tf-idf and other features to Random Forest Model to make predictions. 
rfc = RandomForestClassifier(n_estimators=25, n_jobs=-1)
rfc.fit(train_x, ytrain)

print("Random Forest Classifier score:", rfc.score(test_x, ytest))

#%%
#Get confusion matrix results 
ypred = rfc.predict(test_x)
confusion_matrix(ytest, ypred).ravel()



#%%
