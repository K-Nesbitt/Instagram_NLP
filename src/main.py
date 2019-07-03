#%% 
from src.scraping import login, totals, get_picture_links, scrape_page, users_scrape_save
from src.transforming import  csvs_to_df, clean_text, create_corpus, tokenize_corpus

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, punkt

import pandas as pd 
import numpy as np
import time
import emoji
import re
import pprint

import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')
#%%
#Open files with my username and password stored
u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
my_username = u.read().strip('\n')
my_password = p.read().strip('\n')
u.close()
p.close()

#%%
#Get information from my own profile page
IGdriver = login(my_username, my_password)
time.sleep(5)
my_posts , my_followers = totals(IGdriver)
time.sleep(5)
p_links = get_picture_links(IGdriver, my_posts)
time.sleep(3)
p_info = scrape_page(IGdriver, p_links, my_username)


#%%
#Get information from other users page's
users=['caseybarnold', 'adizz82', 'sirlawrencecharles', 'fresco5280', 'phensworld']
users_scrape_save(my_username, my_password, users)

#%%
#combine csvs to a dataframe
data_path = '/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data'
df_raw = csvs_to_df(data_path)
df_raw.head()
#%%
#This function will lowercase, remove special characters, stem,
# remove stopwords, and tokenize the words
likes_caption_df  = clean_text(df_raw)
likes_caption_df.head()

#%%
#Plot the number of likes on a histogram
fig, ax3 = plt.subplots()
likes_caption_df.hist(column = 'number_of_likes', ax = ax3, figsize = (8,8), bins = 40, color = 'orange')
plt.savefig('images/number_of_likes.png', facecolor = 'white')

#%%
#Collect data on each person's total posts and followers. 
# Create dataframe with information for user by row
names = ['adizz82', 'blake.kelch', 'briannanmoore13', 'caseybarnold', 'cclay2', 'copperhead_etx', 'faithandfuel',
'fitness_with_mercy', 'fresco5280', 'happy_hollydays_', 'jhousesrt8', '_knesbitt', 'mckensiejoo', 'oletheamclachlan',
'phensworld', 'richardrobinsonmusic', 'sirlawrencecharles']
totals_dict = {} 
driver = login(my_username, my_password)
for name in names:
    driver.get('https://www.instagram.com/{}/'.format(name))
    time.sleep(5)
    total_posts , total_followers  = totals(driver)
    totals_dict[name] = [total_posts.split(' ')[0].replace(',', ''), total_followers.split(' ')[0].replace(',', '')]
driver.close()

df_totals  = pd.DataFrame.from_dict(totals_dict, orient='index', dtype = int, columns = ['number_of_posts', 'number_of_followers'])
df_totals = df_totals.astype(int)

#%%
#Plot histograms for the number of posts and number of followers
fig, ax1 = plt.subplots()
df_totals.hist(column = 'number_of_posts', ax = ax1, figsize = (8,8), bins = 20, color = 'green')
plt.savefig('images/number_of_posts.png', facecolor = 'white')

fig, ax2 = plt.subplots()
df_totals.hist(column = 'number_of_followers', ax = ax2, figsize = (8,8), bins = 20, color= 'purple')
plt.savefig('images/number_of_followers.png', facecolor = 'white')

#%%
corpus = create_corpus(likes_caption_df)
word_corpus = tokenize_corpus(corpus)

#%%
#Create a frequency distribution for the words in the corpus_two
fdist = FreqDist(word for word in word_corpus)    
fdist.pprint(maxlen=15)

#image shows best in jupyter notebook
fdist.plot(30, title='Frequency of Top 30 Words')
#%%
#create a train and test set of data
X = np.array(corpus)
y = likes_caption_df['number_of_likes'].values
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)
#%%
#Create Tf-idf vectorizer and save feature names, vocabulary set, and ignored words
vector_train = TfidfVectorizer(min_df= 0.0025)
X_vector = vector_train.fit_transform(Xtrain)
X_train = X_vector.todense()

popular_words = vector_train.get_feature_names()

vocab = vector_train.vocabulary_
ignored_words = vector_train.stop_words_

#%%
#Create Xtest vector from Xtrain vocabulary
vector_test = TfidfVectorizer(vocabulary=vocab)
X_vect = vector_test.fit_transform(Xtest)
X_test = X_vect.todense().astype(int)

#%%
#Random Forest Regression Model
rf = RandomForestRegressor(n_estimators = 100, n_jobs=-1)
rf.fit(X_train, ytrain)
print("Random Forest score:", rf.score(X_test, ytest))

#Record best score: minimum df of 0.003, and 100 trees, rf score: -0.04968729153554263

#%%
#Linear Regression Model
lmodel = LinearRegression()
lmodel.fit(X_train, ytrain)
print('Linear Regression score:', lmodel.score(X_test, ytest))


#%%
len(vocab)

#%%