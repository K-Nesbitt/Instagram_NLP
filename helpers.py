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
    webdriver.find_element_by_css_selector("a[href*='/_knesbitt/']").click()

    #get total number of post and total number of followers


    #scrape page for photos, datetime stamp, and caption

    #end session
    #webdriver.close()

