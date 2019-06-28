from selenium import webdriver
driver = webdriver.Chrome('/Users/keatra/Downloads/chromedriver')

def IG_login(url, my_username, my_password):
    driver.get(url)
    driver.find_element_by_name('username').send_keys(my_username)
    driver.find_element_by_name('password').send_keys(my_password)
    driver.find_element_by_xpath("//*[contains(text(), 'Log In')]").click()