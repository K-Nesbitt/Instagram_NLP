import numpy as np 
import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

        num_posts = int(total_posts.split(' ')[0])   
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
                likes_list = webdriver.find_elements_by_class_name('zV_Nj')
                if len(likes_list) != 0:
                        if len(likes_list) == 1:
                                num_likes = int(likes_list[0].text.split(' ')[0])
                        
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

                webdriver.close()
                
                # Switch focus back to main tab
                webdriver.switch_to.window(webdriver.window_handles[0])    
                time.sleep(5)        
       
        return picture_info
 

def save_csv(lst_of_lst, filename):
        '''converts list of lists into a dataframe
        and then saves the df as a csv file'''
        columns = ['number_of_likes', 'caption']
        df = pd.DataFrame(lst_of_lst, columns =columns)
        df.to_csv(path_or_buf='/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data/{}'.format(filename))
        return None


'''if __name__ == "__main__":
        u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
        p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
        my_username = u.read().strip('\n')
        my_password = p.read().strip('\n')
        u.close()
        p.close()
        IGdriver = login(my_username, my_password)
        time.sleep(10)
        user = 'dj_bangs'
        IGdriver.get('https://www.instagram.com/{}/'.format(user))
        user_posts, user_followers = totals(IGdriver)
        time.sleep(3)
        user_links = get_picture_links(IGdriver, user_posts)
        time.sleep(5)
        user_info = scrape_page(IGdriver, user_links, user)'''

       

