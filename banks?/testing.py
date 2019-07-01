
from functions import login, totals, get_picture_links, scrape_page
import pandas as pd 
import time
import csv 
import glob
bdf = pd.read_csv('dj_banks.csv')
bdf.iloc[2,:].values

#%%
l = []
with open('dbanks.csv', 'r') as f:
    reader = csv.reader(f, )
    for row in reader:
        l.append(row)
dbdf = pd.DataFrame([sub.split("[") for sub in l])
dbdf
#%%
df2 = pd.read_csv("dbanks.csv", delimiter=']', dtype=str).transpose()
df2
#%%
new = df2[0].str.split() 
  


#%%
'''from itertools import dropwhile
with open("dbanks.csv") as f:
    r = csv.reader(f)
    df = pd.DataFrame().from_records(r)
df.transpose()'''