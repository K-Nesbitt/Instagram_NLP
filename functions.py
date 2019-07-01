import numpy as np 
import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import glob
import re

def expo_wait():
    '''
    expo wait - create an exponential random sleep time
    '''
    time.sleep(210*np.random.exponential())


def login(my_username, my_password):
        '''This function will initiate a webdriver and
         log in into Instagram 
        with the given username and password and 
        direct you to the profile page. '''

        url = 'https://www.instagram.com/accounts/login'
        driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')
        
        #go to instagram login page 
        driver.get(url)
        time.sleep(3)

        #enter username and passwords
        driver.find_element_by_name('username').send_keys(my_username)
        driver.find_element_by_name('password').send_keys(my_password)
        time.sleep(3)

        #Login
        driver.find_element_by_xpath("//*[contains(text(), 'Log In')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//*[contains(text(), 'Not Now')]").click()
        time.sleep(3)
        #go to profile page
        driver.find_element_by_css_selector("a[href*='/"+my_username+"/']").click()
        
        return driver

def totals(webdriver):
        '''This function will find and return the total 
        number of posts and followers on a page'''

        list_elements = webdriver.find_elements_by_tag_name('li')

        post_element = [x for x in list_elements if x.text.find('posts') != -1] 
        total_posts = post_element[0].text

        followers_element = [x for x in list_elements if x.text.find('followers') != -1]
        total_followers = followers_element[0].text

        '''following_element = [x for x in list_elements if x.text.find('following') != -1]
        total_following = following_element[0].text  '''  

        return total_posts, total_followers


def get_picture_links(webdriver, total_posts):
        '''This function will find all links that have
        pictures on the page'''
        posts = total_posts.split(' ')[0].replace(',', '')
        num_posts = int(posts)   
        pages = (num_posts//12)
        link_set = set()
        html = webdriver.find_element_by_tag_name('html')

        for _ in range(pages):
                all_links = webdriver.find_elements_by_tag_name('a')   
                for link in all_links:
                        picture_link = link.get_attribute('href') 
                        if picture_link.find('/p/') != -1:
                                link_set.add(picture_link)
                        
                html.send_keys(Keys.END)
                time.sleep(3)

        return link_set

def scrape_page(webdriver, links, username):
        '''This function will go to all links provided
        and scrape each picture for the number of likes
        and the caption. It will only provide the caption if the 
        identified user is the title'''
        picture_info = []

        for link in links:
                # Open new tab
                webdriver.execute_script("window.open('');")
                time.sleep(3)

                # Switch to the new window
                webdriver.switch_to.window(webdriver.window_handles[1])
                webdriver.get(link)
                time.sleep(5)
                try:
                        likes_list = webdriver.find_elements_by_class_name('zV_Nj')
                        if len(likes_list) != 0:
                                if len(likes_list) == 1:
                                        num_likes = 5
                                
                                else:
                                        num_likes = int(likes_list[1].text.split(' ')[0]) + 1

                                try:
                                        title = webdriver.find_element_by_class_name('_6lAjh').text
                                        if title == username:
                                                caption_list = webdriver.find_elements_by_xpath("//div[@class='C4VMK']//span")
                                                '''num_of_comments = len(caption_list)'''
                                                caption = caption_list[0].text
                                        else:
                                                caption = None
                                except:
                                        caption = None
                                        

                                picture_info.append([num_likes, caption])
                except:
                        num_likes = None 
                webdriver.close()
                
                # Switch focus back to main tab
                webdriver.switch_to.window(webdriver.window_handles[0])    
                time.sleep(5)        
       
        return picture_info
 
def users_scrape_save(my_username, my_password, users, path, df_columns=['number_of_likes', 'caption']):
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

                df = pd.DataFrame(user_info, columns= df_columns)
                df.to_csv(path_or_buf= glob.glob(path + '/{}.csv'.format(user)))
        return None

def csvs_to_df(path):
        #open all csv's in folder path and save to one pandas df
        all_files = glob.glob(path + '/*.csv')
        df_from_each_file = (pd.read_csv(f, usecols=[1,2]) for f in all_files)
        concatenated_df  = pd.concat(df_from_each_file, ignore_index=False)
        return concatenated_df

emoji_pattern = re.compile("["
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
        "]+", flags=re.UNICODE)

def clean_text(df):
        #lowercase, strip hashtags and at symbols
        df.iloc[:, 1] = df.iloc[:, 1].map(lambda row: 
                            row.lower().replace('#', '').replace('@', ''),
                            na_action = 'ignore')
        #remove all emojis
        df.iloc[:, 1] = df.iloc[:, 1].map(lambda row: 
                             emoji_pattern.sub('', row), na_action = 'ignore')
        return df

'''if __name__ == "__main__":

'''
       

       

