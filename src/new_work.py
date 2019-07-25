#%%
from src.transforming import csvs_to_df, clean_text, add_word_count, create_full_df, create_corpus, tokenize_corpus
from src.scraping import user_totals
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from nltk.tokenize import word_tokenize, punkt

import pandas as pd 
import numpy as np
from collections import Counter
import operator
import holoviews as hv 

hv.extension('bokeh')

#%%
#Combine all csvs to a dataframe with all features: likes, caption, user
data_path = '/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data_2'
test = csvs_to_df(data_path)
test = clean_text(test)

#%%
likes_caption_user = create_full_df(data_path)
likes_caption_user.head()


#%%
#Join datafrae with features and user totals
user_totals = pd.read_csv('./user_totals.csv', header=0, names = ['user', 'user_posts', 'user_followers'])
full_df = test.merge(user_totals, on='user')


#%%
#Graph a histogram of the  number of likes 
num_likes = hv.Histogram(np.histogram(df_raw['number_of_likes'], 250))
num_likes.opts(xlabel='Number of Likes', xticks=10)
num_likes.redim(x=hv.Dimension('x', range=(0, 200)))

#%%
#Graph relationship between number of likes and number of words
likes = full_df['number_of_likes'].values
words = full_df['number_of_words'].values

words_likes = hv.Scatter((words, likes)).opts(xlabel='Number of words in caption', ylabel='Number of likes',title='Words vs. Likes')
words_likes.redim(x=hv.Dimension('x', range=(0, 100)), y=hv.Dimension('y', range=(0,100)))

#%%
#Graph a histogram of the number of words per document
hv.Histogram(np.histogram(full_df['number_of_words'].values)).opts(xlabel='Number of Words in caption')


#%%
#Plot the number of posts
num_posts = hv.Histogram(np.histogram(user_totals['number_of_posts'], 50))
num_posts.opts(xlabel='Number of Posts per User', xticks=10)
num_posts.redim(x=hv.Dimension('x', range=(0, 800)))
num_posts.redim(y=hv.Dimension('y', range=(0, 4)))


#%%
#Plot the number of followers
num_followers = hv.Histogram(np.histogram(drop_high_users['number_of_followers'], 50))
num_followers.opts(xlabel='Number of Followers per User', xticks=5)
num_followers.redim(x=hv.Dimension('x', range=(0, 1200)))

#%%
#Create a corpus from the rows in a dataframe
full_df = pd.read_csv('./all_info.csv', index_col=0)

#%%
corpus = create_corpus(full_df)
word_corpus = tokenize_corpus(corpus)
print('There are a total of {} words in the corpus'.format(len(word_corpus)))

#%%
#Create a frequency distribution for word_corpus
words = Counter(word_corpus)
sorted_words = sorted(words.items(), key=operator.itemgetter(1))

#%%
#Graph the frequency of the top ten words
frequency = hv.Scatter(sorted_words[-10:])
frequency.opts(size=7, title='Word Frequency', xlabel='Word', ylabel='Number of Times in Corpus')
#%%
#create a train and test set of data
#combine = np.concatenate((np.array(corpus).reshape(-1,1), full_df.iloc[:, 2:].values), axis=1) 
X = full_df.iloc[:,1:]
y = full_df['number_of_likes'].values
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)

#%%
#Create Tf-idf vectorizer, transform data, 
# combine tf-idf vector and number of words to feed into model 
vector_train = TfidfVectorizer(min_df= 0.00017)
X_vector = vector_train.fit_transform(Xtrain['caption'])
X_train = np.array(X_vector.todense())
#x_full_train = np.concatenate((X_train, Xtrain['num_words'].values.reshape(-1,1)), axis=1)

vocab = vector_train.vocabulary_
ignored_words = vector_train.stop_words_

#%%
#Create Xtest vector from Xtrain vocabulary
vector_test = TfidfVectorizer(vocabulary=vocab)
X_vect = vector_test.fit_transform(Xtest['caption'])
X_test = X_vect.todense().astype(int)
x_full_test = np.concatenate((X_test, Xtest['num_words'].values.reshape(-1,1)), axis=1)

#%%
#Random Forest Regression Model
rf = RandomForestRegressor(n_estimators = 10, max_features=0.33, n_jobs=-1)
rf.fit(x_full_train, ytrain)
print("Random Forest score:", rf.score(x_full_test, ytest))

#n_estimators = 10, max_features=0.33 = score -0.48

#%%
