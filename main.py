#%% 
from functions import login, totals, get_picture_links, scrape_page
import pandas as pd 
import time
import csv 
import glob
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
users=['jhousesrt8','cclay2', 'copperhead_etx', 'faithandfuel', 
'mckensiejoo','oletheamclachlan', 'happy_hollydays', 'fitness_with_mercy',
'briannanmoore13']

#%%
#Get information from other users page's
IGdriver = login(my_username, my_password)

for user in users:
    time.sleep(5)
    IGdriver.get('https://www.instagram.com/{}/'.format(user))
    time.sleep(5)
    user_posts, user_followers = totals(IGdriver)
    time.sleep(3)
    user_links = get_picture_links(IGdriver, user_posts)
    time.sleep(7)
    user_info = scrape_page(IGdriver, user_links, user)
    #users_dict[user] = [user_posts, user_followers, user_info]

    df = pd.DataFrame(user_info, columns=['number_of_likes', 'caption'])
    df.to_csv(path_or_buf='/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data/{}.csv'.format(user))
    

#%%
#open all csv's and save to pandas df
path = '/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data'
all_files = glob.glob(path + '/*.csv')
df_from_each_file = (pd.read_csv(f, usecols=[1,2]) for f in all_files)
concatenated_df  = pd.concat(df_from_each_file, ignore_index=False)
concatenated_df.head()

|#%%


#%%
