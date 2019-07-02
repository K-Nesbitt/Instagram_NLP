import pandas as pd 
import glob
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, punkt
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')

def csvs_to_df(path):
        #open all csv's in folder path and save to one pandas df
        all_files = glob.glob(path + '/*.csv')
        df_from_each_file = (pd.read_csv(f, usecols=[1,2]) for f in all_files)
        concatenated_df  = pd.concat(df_from_each_file, ignore_index=False)
        concatenated_df['number_of_likes'] = concatenated_df['number_of_likes'].astype(int)
        concatenated_df['caption'] = concatenated_df['caption'].astype(str)
        return concatenated_df

'''emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)'''

def clean_text(df):
    '''This function will clean the caption column of the dataframe
    and return a transformed df'''

    #lowercase all words
    df['caption'] = df['caption'].str.lower()
    
    '''#remove all emojis
    df['caption'] = df['caption'].map(lambda row: 
                            emoji_pattern.sub('', row), na_action = 'ignore')'''
    
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
