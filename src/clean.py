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
complete_df = df.merge(totals, on='user')


#%%


#%%
