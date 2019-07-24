from scraping import login, totals
import pandas as pd 
import time

def user_totals():
    #Read in username and password from file
    u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
    p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
    my_username = u.read().strip('\n')
    my_password = p.read().strip('\n')
    u.close()
    p.close()

    #Collect data on each person's total posts and followers. 

    totals_dict = {} 
    driver = login(my_username, my_password)
    for name in names:
        driver.get('https://www.instagram.com/{}/'.format(name))
        time.sleep(8)
        total_posts , total_followers  = totals(driver)
        totals_dict[name] = [total_posts.split(' ')[0].replace(',', ''), total_followers.split(' ')[0].replace(',', '')]
    driver.close()

    # Create dataframe with information for user by row
    df_totals  = pd.DataFrame.from_dict(totals_dict, orient='index', dtype = int, columns = ['number_of_posts', 'number_of_followers'])
    df_totals = df_totals.astype(int)

    return df_totals