#%%
%load_ext autoreload
%autoreload 2
#%% 
from helpers import main
from selenium import webdriver

#%%
u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
my_username = u.read().strip('\n')
my_password = p.read().strip('\n')
u.close()
p.close()
url = 'https://www.instagram.com/accounts/login'
driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')
(n, f, pics) = main(driver,url, my_username, my_password)



#%%



#%%
