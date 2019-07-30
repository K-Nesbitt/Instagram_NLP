#%%
from src.transforming import create_full_df, get_top_n_words

import pandas as pd 
import numpy as np
import holoviews as hv 

hv.extension('bokeh')

#%%
#Create dataframe from files in folder. 
data_path = '/Users/keatra/Galvanize/Projects/Instagram_NLP/users'
data = create_full_df(data_path)
data.head()

#%%
#Graph a histogram of the  number of likes 
num_likes = hv.Histogram(np.histogram(data['number_of_likes'], 250))
num_likes.opts(xlabel='Number of Likes', xticks=10)
num_likes.redim(x=hv.Dimension('x', range=(0, 200)))

#%%
#Graph relationship between number of likes and number of words
likes = data['number_of_likes'].values
words = data['number_of_words'].values

words_likes = hv.Scatter((words, likes)).opts(xlabel='Number of words in caption', ylabel='Number of likes',title='Words vs. Likes')
words_likes.redim(x=hv.Dimension('x', range=(0, 100)), y=hv.Dimension('y', range=(0,100)))

#%%
#Graph a histogram of the number of words per document
hv.Histogram(np.histogram(data['number_of_words'].values)).opts(xlabel='Number of Words in caption')

#%%
#Calculate and graph the frequency of the top 10 words

top_words = get_top_n_words(data.caption.values, n=10)
frequency = hv.Scatter(top_words)
frequency.opts(size=7, title='Word Frequency', xlabel='Word', ylabel='Number of Times in Corpus')


#%%
#Calculate and graph the average number of likes by user
avg_likes = [(i, avg) for i, avg in enumerate(data.user_avg_likes.unique())]
hv.Scatter(avg_likes).opts(size=7, title='Average Likes by User', xlabel='User ID', ylabel='Averge Number of Likes')


#%%
#!!! fix
# Plot the number of posts
num_posts = hv.Histogram(np.histogram(user_totals['number_of_posts'], 50))
num_posts.opts(xlabel='Number of Posts per User', xticks=10)
num_posts.redim(x=hv.Dimension('x', range=(0, 800)))
num_posts.redim(y=hv.Dimension('y', range=(0, 4)))


#%%
#!!!fix 
#Plot the number of followers
num_followers = hv.Histogram(np.histogram(drop_high_users['number_of_followers'], 50))
num_followers.opts(xlabel='Number of Followers per User', xticks=5)
num_followers.redim(x=hv.Dimension('x', range=(0, 1200)))






