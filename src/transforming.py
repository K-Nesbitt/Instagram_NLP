import pandas as pd 
import glob
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, punkt
from nltk.stem import PorterStemmer

import nltk
nltk.download('punkt')

def csvs_to_df(path):
        '''This function will convert all csv'slocated in the same folder
        to one big dataframe with two named columns. 

        Parameters: the path of the data folder with csv's

        Returns: the combined dataframe. '''

        concat_df = pd.DataFrame()

        all_files = glob.glob(path + '/*.csv')
        for f in all_files:
            df = pd.read_csv(f, usecols=[1,2])
            df['user'] = f.replace(path, '').strip('/').strip('.csv')
            concat_df  = pd.concat([concat_df,df], ignore_index=False)
       
        concat_df['number_of_likes'] = concat_df['number_of_likes'].apply(lambda x: x.replace(',', '') if type(x)==str else x)
        concat_df['number_of_likes'] = concat_df['number_of_likes'].astype(int)
        concat_df['caption'] = concat_df['caption'].astype(str)
        
        return concat_df

def clean_text(df):
        '''This function will transform the caption text to lowercase all words,
        remove special characters, use the Porter Stemmer to stem words down,
        remove stop words from each caption, and then tokenize the words

        Parameters: the dataframe to change

        Returns: changed dataframe
        '''

        #lowercase all words
        df['caption'] = df['caption'].str.lower()

        #remove special characters
        strip_chars = "@#.?,!;:/\/'()&<>"
        rgx = re.compile('[%s]' % strip_chars)
        df['caption'] = df['caption'].map(lambda row: 
                        rgx.sub('', row), na_action = 'ignore')

        #stem and remove stopwords
        port = PorterStemmer()
        s_stop = set(stopwords.words('english'))
        df['caption'] = df['caption'].apply(lambda row: 
                                [port.stem(word) for word in row.split() if word not in s_stop])

        #tokenize the words
        df['caption'] = df['caption'].apply(lambda row: word_tokenize(' '.join(row)))

        return df

def add_word_count(df):
	df['number_of_words'] = df['caption'].apply(lambda x: len(x))
	return df

def create_full_df(path):
        df = csvs_to_df(path)
        df = clean_text(df)
        df = add_word_count(df)
        return df

def create_corpus(df, column= 'caption'):
        '''Create a corpus from each row in the dataframe to use
        on train and test sets.

        Parameters: a dataframe and column to make a corpus

        Returns: a corpus (list of strings in same index order as dataframe)
        '''

        corpus = []
        for row in df[column]:
                r_string = str(' '.join(row))
                clean_string = re.sub('\W+',' ', r_string)
                corpus.append(clean_string)
        
        return corpus
def tokenize_corpus(corpus):
        '''Removes special characters and emojis and separate the corpus
        by individual words. 

        Parameters: the corpus (a list of strings)

        Returns: a list of words
        '''
        corpus_two = []
        for i in range(len(corpus)):
                words = word_tokenize(corpus[i])
                for j in range(len(words)):
                        corpus_two.append(words[j])
        
        return corpus_two

