import numpy as np 
import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')


def expo_wait():
    '''
    expo wait - create an exponential random sleep time
    '''
    time.sleep(210*np.random.exponential())


def main(url, my_username, my_password):
    #go to instagram login page 
    driver.get(url)
    time.sleep(3)

    #enter username and passwords
    driver.find_element_by_name('username').send_keys(my_username)
    driver.find_element_by_name('password').send_keys(my_password)
    time.sleep(3)

    #Login
    driver.find_element_by_xpath("//*[contains(text(), 'Log In')]").click()
    time.sleep(3)

    #go to profile page

    #get total number of post and total number of followers


    #scrape page for photos, datetime stamp, and caption

    #end session
    driver.close()

