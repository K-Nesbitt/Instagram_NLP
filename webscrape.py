
#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
#%%
url = 'https://jan-sotelo-blc2.squarespace.com/config/analytics#sales-overview'
Request = requests.get(url)

#%%
soup = BeautifulSoup(Request.text)
soup.prettify()

#%%

