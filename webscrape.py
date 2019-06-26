
#%%
from selenium import webdriver
import pandas as pd 
import numpy as np 
#%%

driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')

#%%

def IG_login(url, username, password):
    driver.get(url)
    driver.find_element_by_name(“username”).send_keys(username)
    driver.find_element_by_name(“password”).send_keys(password)
    driver.find_element_by_name(“submit”).click()


#%%
url = 'https://www.instagram.com/'
username = '_knesbitt'
password = '2016riley'
IG_login(url, username, password)