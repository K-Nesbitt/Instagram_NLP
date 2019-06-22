
#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
#%%
url = 'https://www.instagram.com/atxhelitours/'
Request = requests.get(url)

#%%
soup = BeautifulSoup(Request.text, features="lxml")
soup.findAll(class_ ='_7UhW9')

#%%


profile_name = 