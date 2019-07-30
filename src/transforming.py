import pandas as pd 
import glob
import re

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer


def csvs_to_df(path):
        '''This function will convert all csv'slocated in the same folder
        to one big dataframe with two named columns. 

        Parameters: the path of the data folder with csv's

        Returns: the combined dataframe '''

        concat_df = pd.DataFrame()

        all_files = glob.glob(path + '/*.csv')
        for f in all_files:
            df = pd.read_csv(f, usecols=[1,2])
            df['user'] = f.replace(path, '').strip('/')[:-4]
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
                                " ".join([port.stem(word) for word in row.split() if word not in s_stop]))


        return df

def add_word_count(df):
        '''This function will count the length of the caption once split. 
        This will count words, emojis, and characters separated by a space.

        Parameters: the dataframe with the caption column.

        Returns: new dataframe with a 'number of words column'. 
        '''

        df['number_of_words'] = df['caption'].apply(lambda x: len(x.split()))
        return df

def add_user_totals(current_df, file_path_totals = './user_totals.csv'):
        '''This function will add the columns for user total posts and user total followers 
        by row. 
        Parameters: dataframe, and file path with user total posts and followers information.
        
        Returns: new dataframe with information on user post and followers.
        '''

        totals_df = pd.read_csv('./data/user_totals.csv', header=0, names = ['user', 'user_posts', 'user_followers'])
        new_df = current_df.merge(totals_df, how = 'left', on='user')
        return new_df

def add_user_avg_likes(df):
        '''This function will calculate and add the average number of likes by user
        to each row by the user. 

        Parameters: dataframe

        Returns: new dataframe with additional column of user average likes. 
        '''
        
        users = df.user.unique()
        likes_avg = {}
        for u in users:
                mean = df[df.user == u]['number_of_likes'].mean()
                likes_avg[u]=round(mean, 0)
        df['user_avg_likes'] = df['user'].map(likes_avg)
        return df

def make_user_dummies(df, column_name = 'user'):
        '''This function will turn the 'user' column into  multiple columns
        by the username with 0 or 1 if the row is the user. 

        Parameters: dataframe and column name of the users

        Returns: dataframe with multiple columns for each username'''

        user_dummies = pd.get_dummies(df[column_name])
        new_df = pd.concat((df, user_dummies), axis=1).drop(columns=column_name)
        return new_df

def create_full_df(path):
        '''This function is the pipeline for the data 
        that combines the previous functions.
        
        Parameter: the path to the folder with all stored csv's 
        of user photo information (likes and caption)

        Returns: dataframe ready for train and test'''

        df = csvs_to_df(path)
        df = clean_text(df)
        df = add_word_count(df)
        df = add_user_totals(df)
        df = add_user_avg_likes(df)
        df = make_user_dummies(df)
        
        return df


def get_top_n_words(corpus, n=None):
        '''
        This fucntion will list the top n words in a vocabulary according 
        to occurrence in a text corpus.

        Parameters: corpus (list of strings), n (the number of words)

        Returns: a list of the top n words in descending order. 
        '''

        vec = CountVectorizer().fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
        return words_freq[:n]