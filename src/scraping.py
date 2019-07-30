import numpy as np 
import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def login(my_username, my_password):
        '''This function will initiate a webdriver, log into Instagram,
        and go to the user's profile page. 

        Parameters: Instagram username and password 
        
        Returns:
        The driver object'''

        url = 'https://www.instagram.com/accounts/login'
        chromeOptions = Options()
        chromeOptions.add_argument('--headless')
        driver = webdriver.Chrome('/Users/keatra/Galvanize/chromedriver', options=chromeOptions)
        
        #go to instagram login page 
        driver.get(url)
        time.sleep(3)

        #enter username and passwords
        driver.find_element_by_name('username').send_keys(my_username)
        driver.find_element_by_name('password').send_keys(my_password)
        time.sleep(3)

        #Login
        driver.find_element_by_xpath("//*[contains(text(), 'Log In')]").click()
        time.sleep(5)
        
        '''
        This step was commented out because when using the headless option, the 
        pop up alert is not present. 

        driver.find_element_by_xpath("//*[contains(text(), 'Not Now')]").click()
        time.sleep(3)'''

        #go to profile page
        driver.find_element_by_css_selector("a[href*='/"+my_username+"/']").click()
        
        return driver

def totals(webdriver):
        '''This function will get the total number of posts and followers
        for the user profile page that the webdriver is currently on. 

        Parameters: the active webdriver 

        Returns: tuple of the total posts and total followers.'''

        list_elements = webdriver.find_elements_by_tag_name('li')

        post_element = [x for x in list_elements if x.text.find('posts') != -1] 
        total_posts = post_element[0].text

        followers_element = [x for x in list_elements if x.text.find('followers') != -1]
        total_followers = followers_element[0].text

       ''' I commented out finding the total number of people the user is following
        because it was not useful in my data collection at the time but I still wanted 
        to keep the code if I ever decided to use it. 

        following_element = [x for x in list_elements if x.text.find('following') != -1]
        total_following = following_element[0].text'''   

        return total_posts, total_followers


def get_picture_links(webdriver, total_posts):
        '''This function will find all links that have
        pictures on the page. Note that there are only about 12 photos per page
        so the program will 'scroll' as many times as necessary to get all photos.

        Parameters: the active webdriver, the total posts for that user

        Returns: a set of picture and video links
        '''
        posts = total_posts.split(' ')[0].replace(',', '')
        num_posts = int(posts)   
        pages = (num_posts//12) #This will determine how many times we scroll on a page
                                
        
        link_set = set()
        html = webdriver.find_element_by_tag_name('html')

        for _ in range(pages):
                all_links = webdriver.find_elements_by_tag_name('a')   
                for link in all_links:
                        picture_link = link.get_attribute('href') 
                        if picture_link.find('/p/') != -1: #only adding links that have are pictures
                                link_set.add(picture_link)
                        
                html.send_keys(Keys.END)
                time.sleep(3)

        return link_set

def scrape_page(webdriver, links, username):
        '''This function will go to all links provided
        and scrape each picture for the number of likes
        and the caption. If the link is a video no information is recorded. 
        The function will only save the caption if the title is the 
        identified user
        
        Parameters: the active webdriver, a set of picture links, 
        the username of the page your are scraping

        Returns: a list of lists with the number of likes and caption
        '''
        picture_info = []

        for link in links:
                # Open new tab
                webdriver.execute_script("window.open('');")
                time.sleep(3)

                # Switch to the new window
                webdriver.switch_to.window(webdriver.window_handles[1])
                webdriver.get(link)
                time.sleep(5)
                try:
                        likes_list = webdriver.find_elements_by_class_name('zV_Nj')

                        if len(likes_list) != 0: #If the length is 0, then it is a video
                                
                                if len(likes_list) == 1: #No common friends liked the photo
                                        num_likes = webdriver.find_elements_by_class_name('Nm9Fw')[0].text.split(' ')[0]
                                
                                else:
                                        num_likes = int(likes_list[1].text.split(' ')[0]) + 1

                                try:
                                        title = webdriver.find_element_by_class_name('_6lAjh').text
                                        if title == username:
                                                caption_list = webdriver.find_elements_by_xpath("//div[@class='C4VMK']//span")
                                                
                                                '''This code works but not active since I did not use the information
                                                num_of_comments = len(caption_list)'''
                                                
                                                caption = caption_list[0].text
                                        else:
                                                caption = None #if the user was not the title
                                except:
                                        caption = None #photo does not have a caption or any comments
                                        

                                picture_info.append([num_likes, caption])
                except:
                        pass
                webdriver.close()
                
                # Switch focus back to main tab
                webdriver.switch_to.window(webdriver.window_handles[0])    
                time.sleep(5)        
       
        return picture_info
 
def users_scrape_save(my_username, my_password, users, folder_name):
        '''This function will log into Instagram and scrape a given set of user pages and 
        save the information by page into a csv in the given folder name.  

        Parameters: Instagram username and password, list of usernames,
        and the name of the folder to save the data to. 
        
        Returns: None. Files are saved as the program is running. '''

        #First logs in to Instagram
        IGdriver = login(my_username, my_password)

        for user in users:
                time.sleep(8)
                IGdriver.get('https://www.instagram.com/{}/'.format(user))
                time.sleep(10)
                user_posts, user_followers = totals(IGdriver)
                time.sleep(3)
                user_links = get_picture_links(IGdriver, user_posts)
                time.sleep(7)
                user_info = scrape_page(IGdriver, user_links, user)

                df = pd.DataFrame(user_info, columns=['number_of_likes', 'caption'])
                df.to_csv(path_or_buf= './{}/{}.csv'.format(folder_name, user))
        return None


def user_totals(username, password, users):
	'''Since the totals function does not save users total posts and total followers, 
        this function will go through each user and save their information to a dataframe
        for later reference. 

        Parameters: Instagram username and password, and list of usernames

        Returns: Dataframe with username, total posts, and total followers. '''
	
	totals_dict = {}
	driver = login(my_username, my_password)
	for name in names:
		driver.get('https://www.instagram.com/{}/'.format(name))
		time.sleep(8)
		total_posts , total_followers  = totals(driver)
		totals_dict[name] = [total_posts.split(' ')[0].replace(',', ''), total_followers.split(' ')[0].replace(',', '')]
		
	driver.close()
	df_totals  = pd.DataFrame.from_dict(totals_dict, orient='index', dtype = int, columns = ['user_posts', 'user_followers'])
	
	df_totals['user_followers'] = df_totals['user_followers'].apply(lambda x: x.replace('.', '') if type(x)==str else x)
	df_totals['user_followers'] = df_totals['user_followers'].apply(lambda x: x.replace('k', '00') if type(x)==str else x)
	df_totals['user_followers']= df_totals['user_followers'].astype(int)
	df_totals['user_posts']= df_totals['user_posts'].astype(int)

	return df_totals


if __name__ == "__main__":
        
        u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
        p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
        my_username = u.read().strip('\n')
        my_password = p.read().strip('\n')
        u.close()
        p.close()


        users= [ 'adizz82', 'blake.kelch', 'briannanmoore13', 'caseybarnold', 'cclay2', 'copperhead_etx', 'faithandfuel',
                'fitness_with_mercy', 'fresco5280', 'happy_hollydays_', 'jhousesrt8','_knesbitt', 'mckensiejoo', 
                'oletheamclachlan', 'phensworld', 'richardrobinsonmusic', 'sirlawrencecharles', 'keilam7', 'dr_kerrie', 
                'pina.risa', 'presmith', 'giftedhands_crochet_and_crafts','jeffersonmason4', 'dmdanamitchell', 
                'suntanned_superman_', 'laceycooley', 'goulding_jr']

        users_scrape_save(my_username, my_password, users)

        

        


       

       

