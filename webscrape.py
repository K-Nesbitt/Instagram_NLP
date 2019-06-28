
#%%
from selenium import webdriver
import pandas as pd 
import numpy as np 
from helpers import IG_login
#%%
u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
url = 'https://www.instagram.com/accounts/login'
my_username = u.read().strip('\n')
my_password = p.read().strip('\n')
IG_login(url, my_username, my_password)
u.close()
p.close()
#%%
driver.find_element_by_partial_link_text("a href='/_knesbitt/'").click()

#%%


#%%



