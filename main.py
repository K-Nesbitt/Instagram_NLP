#%% 
from functions import login, totals, get_picture_links, scrape_page, users_scrape_save, csvs_to_df, clean_text
import pandas as pd 
import time
import csv 
import glob
import re

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
#Get information from other users page's
users=['jhousesrt8','cclay2', 'copperhead_etx', 'faithandfuel', 
'mckensiejoo','oletheamclachlan', 'happy_hollydays', 'fitness_with_mercy',
'briannanmoore13']



#%%


    

#%%


#%%
concatenated_df.iloc[:, 1] = concatenated_df.iloc[:, 1].map(lambda row: 
        row.lower().replace('#', '').replace('@', ''), 
        na_action = 'ignore')

#%%


#%%



#%%


#%%


#%%
