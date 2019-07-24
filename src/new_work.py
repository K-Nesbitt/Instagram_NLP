#%%
from src.transforming import  csvs_to_df, clean_text, create_corpus, tokenize_corpus

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, punkt

import pandas as pd 
import numpy as np

import holoviews as hv 

hv.extension('bokeh')

#%%
#%%
#combine csvs to a dataframe
data_path = '/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data_2'
df_raw = csvs_to_df(data_path)
df_raw.head()

#%%
#Plot the number of likes on a histogram
hv.Histogram(np.histogram(df_raw['number_of_likes'], 20)).opts(xlabel='Number of Likes per photo')


#%%
