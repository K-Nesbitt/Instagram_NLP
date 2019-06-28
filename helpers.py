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


def main(webdriver, url, my_username, my_password):
    #go to instagram login page 
    webdriver.get(url)
    time.sleep(3)

    #enter username and passwords
    webdriver.find_element_by_name('username').send_keys(my_username)
    webdriver.find_element_by_name('password').send_keys(my_password)
    time.sleep(3)

    #Login
    webdriver.find_element_by_xpath("//*[contains(text(), 'Log In')]").click()
    time.sleep(5)
    webdriver.find_element_by_xpath("//*[contains(text(), 'Not Now')]").click()
    time.sleep(3)
    #go to profile page
    webdriver.find_element_by_css_selector("a[href*='/"+my_username+"/']").click()
    time.sleep(10)

    #get total number of post and total number of followers
    list_elements = webdriver.find_elements_by_tag_name('li')

    post_element = [x for x in list_elements if x.text.find('posts') != -1] 
    total_posts = post_element[0].text
    print(total_posts)    

    followers_element = [x for x in list_elements if x.text.find('followers') != -1]
    total_followers = followers_element[0].text
    print(total_followers)
    
    following_element = [x for x in list_elements if x.text.find('following') != -1]
    total_following = following_element[0].text    

    #scrape page for photos, datetime stamp, and caption

    #end session
    #webdriver.close()
    return None

if __name__ == "__main__":
        u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
        p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
        my_username = u.read().strip('\n')
        my_password = p.read().strip('\n')
        u.close()
        p.close()
        url = 'https://www.instagram.com/accounts/login'
        driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')
        main(driver,url, my_username, my_password)