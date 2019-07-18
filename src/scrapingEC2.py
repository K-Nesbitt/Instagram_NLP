import numpy as np 
import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login(my_username, my_password):
        '''This function will initiate a webdriver, log into Instagram,
        and go to the user's profile page. 

        Parameters: Instagram username and password 
        
        Returns:
        The driver object'''

        url = 'https://www.instagram.com/accounts/login'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        '''chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("start-maximized")'''
        driver = webdriver.Chrome(executable_path='/home/ubuntu/chromedriver_unix', options=chrome_options)
        
        #go to instagram login page 
        driver.get(url)
        time.sleep(10)

        #enter username and passwords
        driver.find_element_by_name('username').send_keys(my_username)
        driver.find_element_by_name('password').send_keys(my_password)
        time.sleep(20)

        #Login
        driver.find_element_by_xpath("//*[contains(text(), 'Log In')]").click()
        time.sleep(15)
        
        return driver

def totals(webdriver):
        '''This function will get the total number of posts, followers, 
        and following for what ever page the webdriver is on. 

        Parameters: the webdrive that is active

        Returns: tuple of the total posts and total followers.'''

        list_elements = webdriver.find_elements_by_tag_name('li')

        post_element = [x for x in list_elements if x.text.find('posts') != -1] 
        total_posts = post_element[0].text

        followers_element = [x for x in list_elements if x.text.find('followers') != -1]
        total_followers = followers_element[0].text

        #I commented this code out because it was not useful in my data but I still
        # wanted to keep the code if I ever decided to use it. 
        #following_element = [x for x in list_elements if x.text.find('following') != -1]
        #total_following = following_element[0].text   

        return total_posts, total_followers


def get_picture_links(webdriver, total_posts):
        '''This function will find all links that have
        pictures on the page

        Parameters: the active webdriver, the total posts on that page

        Returns: a set of links to pictures and videos
        '''
        posts = total_posts.split(' ')[0].replace(',', '')
        num_posts = int(posts)   
        pages = (num_posts//12) #we divide by 12 because that is the average number of displayed
                                #photos by page
        
        link_set = set()
        html = webdriver.find_element_by_tag_name('html')

        for _ in range(pages):
                all_links = webdriver.find_elements_by_tag_name('a')
                
                for link in all_links:
                        picture_link = link.get_attribute('href') 
                        if picture_link.find('/p/') != -1:
                                link_set.add(picture_link)
                        
                html.send_keys(Keys.END)
                time.sleep(7)
        
        return link_set

def scrape_page(webdriver, links, username):
        '''This function will go to all links provided
        and scrape each picture for the number of likes
        and the caption. It will only provide the caption if the 
        identified user is the title
        
        Parameters: the active webdriver, a set of picture links, 
        the username of the page your are scraping

        Returns: a list of list with the number of likes and caption
        '''
        picture_info = []

        for link in links:
                # Open new tab
                webdriver.execute_script("window.open('');")
                time.sleep(9)

                # Switch to the new window
                webdriver.switch_to.window(webdriver.window_handles[1])
                
                webdriver.get(link)
                time.sleep(14)
                try:
                        likes_list = webdriver.find_elements_by_class_name('zV_Nj')

                        if len(likes_list) != 0: #If the length is 0, then it is a video
                                
                                if len(likes_list) == 1:
                                        num_likes = webdriver.find_elements_by_class_name('Nm9Fw')[0].text.split(' ')[0]
                                
                                else:
                                        num_likes = int(likes_list[1].text.split(' ')[0]) + 1

                                try:
                                        title = webdriver.find_element_by_class_name('_6lAjh').text
                                        if title == username:
                                                caption_list = webdriver.find_elements_by_xpath("//div[@class='C4VMK']//span")
                                                #This code works but not active since I did not use the information
                                                # num_of_comments = len(caption_list)
                                                caption = caption_list[0].text
                                        else:
                                                caption = None
                                except:
                                        caption = None
                                        

                                picture_info.append([num_likes, caption])
                except:
                
                    pass

                webdriver.close()
                
                # Switch focus back to main tab
                webdriver.switch_to.window(webdriver.window_handles[0])    
                time.sleep(7)        
       
        return picture_info
 
def users_scrape_save(my_username, my_password, users):
        '''This function will scrape a given set of users pages and 
        save the information by page into a csv in the data folder of the directory. 

        Parameters: Instagram username and password, list of usernames for other people,
        
        Returns: None. Files are saved as the program is running. '''

        #Assumes original driver was closed and will log in to Instagram
        IGdriver = login(my_username, my_password)

        for user in users:
                time.sleep(14)
                IGdriver.get('https://www.instagram.com/{}/'.format(user))
                print('On user page: {}'.format(user))
                time.sleep(9)
                user_posts, user_followers = totals(IGdriver)
                print('User: {}, has {}'.format(user, user_posts))
                time.sleep(12)
                user_links = get_picture_links(IGdriver, user_posts)
                print('The user has {} picture links'.format(len(user_links)))
                time.sleep(17)
                user_info = scrape_page(IGdriver, user_links, user)

                df = pd.DataFrame(user_info, columns=['number_of_likes', 'caption'])
                df.to_csv(path_or_buf= '/home/ubuntu/insta/data/{}.csv'.format(user))
        return None


if __name__ == "__main__":
        
        u = open('/home/ubuntu/.ssh/IG_username.txt', 'r')
        p = open('/home/ubuntu/.ssh/IG_password.txt', 'r')
        my_username = u.read().strip('\n')
        my_password = p.read().strip('\n')
        u.close()
        p.close()

        users= ['briannanmoore13', 'caseybarnold', 'cclay2', 'copperhead_etx', 'faithandfuel',
'fitness_with_mercy', 'fresco5280', 'happy_hollydays_', 'jhousesrt8', '_knesbitt', 'mckensiejoo', 'oletheamclachlan',
'phensworld', 'richardrobinsonmusic', 'sirlawrencecharles', 'keilam7', 'dr_kerrie', 'pina.risa', 'presmith', 'giftedhands_crochet_and_crafts', 
'jeffersonmason4/', 'dmdanamitchell', 'suntanned_superman_', 'laceycooley', 'goulding_jr']

        users_scrape_save(my_username, my_password, users)

        

        


       

       
