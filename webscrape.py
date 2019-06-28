#%%
%load_ext autoreload
%autoreload 2
#%% 
from helpers import main
from selenium import webdriver
import time
#%%
u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
my_username = u.read().strip('\n')
my_password = p.read().strip('\n')
u.close()
p.close()
url = 'https://www.instagram.com/accounts/login'
#%% 
driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')
main(driver,url, my_username, my_password)

#%%
pictures = driver.find_elements_by_class_name('v1Nh3.kIKUG._bz0w')
print(pictures)
for pic in pictures:
    link = pic.get_attribute('href')
    
    #images = driver.find_elements_by_tag_name('img')
    
    # Open new tab
    driver.execute_script("window.open('');")
    time.sleep(3)

    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link)
    time.sleep(3)        

    # close the active tab
    driver.close()

    # Switch focus back to main tab
    driver.switch_to.window(driver.window_handles[0])
    
#%%
header_classes = driver.find_elements_by_class_name('_3dEHb')
print(header_classes)
for header in header_classes:
    header_info = header.find_elements_by_class_name('LH36I')
    info_list = []
    for info in header_info:
        text = info.text.split('\n')
        info_list.append(text)       
print(info_list)

#%%
