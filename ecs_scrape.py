from functions import login, totals, get_picture_links, scrape_page
import pandas as pd 
import time
import csv 

u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
my_username = u.read().strip('\n')
my_password = p.read().strip('\n')
u.close()
p.close()

users = ['adizz82', 'sirlawrencecharles', 'phensworld', 'fresco5280', 'jarronpaul', 'caseybarnold']

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