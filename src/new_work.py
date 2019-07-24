#%%
from src.transforming import  csvs_to_df, clean_text, create_corpus, tokenize_corpus
from src.scraping import user_totals
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
num_likes = hv.Histogram(np.histogram(df_raw['number_of_likes'], 250))
num_likes.opts(xlabel='Number of Likes per photo', xticks=10)
num_likes.redim(x=hv.Dimension('x', range=(0, 200)))


#%%
users= [ 'adizz82', 'blake.kelch', 'briannanmoore13', 'caseybarnold', 'cclay2', 'copperhead_etx', 'faithandfuel',
                'fitness_with_mercy', 'fresco5280', 'happy_hollydays_', 'jhousesrt8','_knesbitt', 'mckensiejoo', 
                'oletheamclachlan', 'phensworld', 'richardrobinsonmusic', 'sirlawrencecharles', 'keilam7', 'dr_kerrie', 
                'pina.risa', 'presmith', 'giftedhands_crochet_and_crafts','jeffersonmason4', 'dmdanamitchell', 
                'suntanned_superman_', 'laceycooley', 'goulding_jr']
user_totals = user_totals(users)
