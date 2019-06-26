
#%%
from selenium import webdriver
import pandas as pd 
import numpy as np 
#%%

driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')
driver.get('https://www.instagram.com/_knesbitt/')
#%%

def IG_login(url, username, password):
    driver.get(url)
    driver.find_element_by_id(“ID”).send_keys(username)
    driver.find_element_by_id (“ID”).send_keys(password)
    driver.find_element_by_id(“submit”).click()


#%%
