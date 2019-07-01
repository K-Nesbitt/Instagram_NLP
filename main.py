#%% 
from scraping import login, totals, get_picture_links, scrape_page, users_scrape_save
from transforming import  csvs_to_df, clean_text
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

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
my_posts , my_followers = totals(IGdriver)
p_links = get_picture_links(IGdriver, my_posts)
p_info = scrape_page(IGdriver, p_links, my_username)

#%%
data_path = '/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data'

#%%
#Get information from other users page's
users=[]
users_scrape_save(my_username, my_password, users, data_path)

#%%
#combine csvs to a dataframe
df = csvs_to_df(data_path)
clean_df  = clean_text(df)
clean_df
#%%
corpus = []
for row in clean_df['caption']:
    if row == []:
        corpus.append('None')
    else:
        corpus.append(str(' '.join(row)))
print(corpus)

#%%




#%%
