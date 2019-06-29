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
    num_posts = int(post_element[0].text.split(' ')[0])    
    pages = (num_posts//24)
    followers_element = [x for x in list_elements if x.text.find('followers') != -1]
    total_followers = followers_element[0].text
    
    
    '''following_element = [x for x in list_elements if x.text.find('following') != -1]
    total_following = following_element[0].text  '''  

    #scrape page for information on each picture
    picture_info = set()
    html = webdriver.find_element_by_tag_name('html')
    
    for _ in range(pages):
        all_links = webdriver.find_elements_by_tag_name('a')   
        for link in all_links:
                picture_link = link.get_attribute('href') 
                if picture_link.find('/p/') != -1:
                        # Open new tab
                        webdriver.execute_script("window.open('');")
                        time.sleep(3)

                        # Switch to the new window
                        webdriver.switch_to.window(webdriver.window_handles[1])
                        webdriver.get(picture_link)
                        time.sleep(5)
                        likes_list = webdriver.find_elements_by_class_name('zV_Nj')
                        if len(likes_list) != 0:
                                num_likes = int(likes_list[1].text.split(' ')[0]) + 1

                                title = webdriver.find_element_by_class_name('_6lAjh').text
                                if title == my_username:
                                        caption_list = webdriver.find_elements_by_xpath("//div[@class='C4VMK']//span")
                                        '''num_of_comments = len(caption_list)'''
                                        caption = caption_list[0].text
                                else:
                                        caption = 'none'
                                picture_info.append([num_likes, caption])
                
                        webdriver.close()
                        
                        # Switch focus back to main tab
                        webdriver.switch_to.window(webdriver.window_handles[0])    
                        time.sleep(5) 
        html.send_keys(Keys.END)
        time.sleep(2)       
    #end session
    webdriver.close()
    return (total_posts, total_followers, picture_info)

if __name__ == "__main__":
        u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
        p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
        my_username = u.read().strip('\n')
        my_password = p.read().strip('\n')
        u.close()
        p.close()
        url = 'https://www.instagram.com/accounts/login'
        driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')
        (n, f, pics) = main(driver,url, my_username, my_password)

