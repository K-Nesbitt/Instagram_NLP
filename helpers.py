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
    time.sleep(5)

    #get total number of post and total number of followers
    header_classes = webdriver.find_elements_by_class_name('_3dEHb')
    info_list = []
    for header in header_classes:
        header_info = header.find_elements_by_class_name('LH36I')
        for info in header_info:
            text = info.text.split('\n')
            info_list.append(text)       
    print(info_list)
    '''total_posts = info_list[0]
    total_followers = info_list[1]
    total_following = info_list[2]'''

    #scrape page for photos, datetime stamp, and caption

    #end session
    #webdriver.close()
    return None #total_posts, total_followers
