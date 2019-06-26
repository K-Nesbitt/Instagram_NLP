
#%%
from selenium import webdriver
import pandas as pd 
import numpy as np 
#%%

driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')

#%%

def IG_login(url, my_username_, my_password):
    driver.get(url)
    driver.find_element_by_name('username').send_keys(my_username)
    driver.find_element_by_name('password').send_keys(my_password)
    driver.find_element_by_xpath("//*[contains(text(), 'Log In')]").click()


#%%
url = 'https://www.instagram.com/accounts/login'
my_username = '_knesbitt'
my_password = '2016riley'
IG_login(url, my_username, my_password)

#%%
driver.find_element_by_partial_link_text("a href='/_knesbitt/'").click()

#%%


#%%
