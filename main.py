#%% 
from scraping import login, totals, get_picture_links, scrape_page, users_scrape_save
from transforming import  csvs_to_df, clean_text
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from sklearn.model_selection import train_test_split
import time
import emoji
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, punkt
import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')
#%%
#Open files with my username and password stored
u = open('/Users/keatra/.ssh/IG_username.txt', 'r')
p = open('/Users/keatra/.ssh/IG_password.txt', 'r')
my_username = u.read().strip('\n')
my_password = p.read().strip('\n')
u.close()
p.close()

#%%
#Get information from my own profile page
IGdriver = login(my_username, my_password)
my_posts , my_followers = totals(IGdriver)
p_links = get_picture_links(IGdriver, my_posts)
p_info = scrape_page(IGdriver, p_links, my_username)


#%%
#Get information from other users page's
users=['caseybarnold', 'adizz82', 'sirlawrencecharles', 'fresco5280', 'phensworld']
users_scrape_save(my_username, my_password, users)

#%%
#combine csvs to a dataframe
data_path = '/Users/keatra/Galvanize/Projects/Instagram_likes_nlp/data'
df_raw = csvs_to_df(data_path)
df_raw.head()
#%%
#This function will lowercase, remove special characters, stem,
# remove stopwords, and tokenize the words
likes_caption_df  = clean_text(df_raw)
likes_caption_df.head()

#%%
#Plot the number of likes on a histogram
fig, ax3 = plt.subplots()
likes_caption_df.hist(column = 'number_of_likes', ax = ax3, figsize = (8,8), bins = 40, color = 'orange')
plt.savefig('images/number_of_likes.png', facecolor = 'white')

#%%
#Collect data on each person's total posts and followers. 
# Create dataframe with information for user by row
names = ['adizz82', 'blake.kelch', 'briannanmoore13', 'caseybarnold', 'cclay2', 'copperhead_etx', 'faithandfuel',
'fitness_with_mercy', 'fresco5280', 'happy_hollydays_', 'jhousesrt8', '_knesbitt', 'mckensiejoo', 'oletheamclachlan',
'phensworld', 'richardrobinsonmusic', 'sirlawrencecharles']
totals_dict = {} 
driver = login(my_username, my_password)
for name in names:
    driver.get('https://www.instagram.com/{}/'.format(name))
    time.sleep(5)
    total_posts , total_followers  = totals(driver)
    totals_dict[name] = [total_posts.split(' ')[0].replace(',', ''), total_followers.split(' ')[0].replace(',', '')]
driver.close()

df_totals  = pd.DataFrame.from_dict(totals_dict, orient='index', dtype = int, columns = ['number_of_posts', 'number_of_followers'])
df_totals = df_totals.astype(int)

#%%
#Plot histograms for the number of posts and number of followers
fig, ax1 = plt.subplots()
df_totals.hist(column = 'number_of_posts', ax = ax1, figsize = (8,8), bins = 20, color = 'green')
plt.savefig('images/number_of_posts.png', facecolor = 'white')

fig, ax2 = plt.subplots()
df_totals.hist(column = 'number_of_followers', ax = ax2, figsize = (8,8), bins = 20, color= 'purple')
plt.savefig('images/number_of_followers.png', facecolor = 'white')

#%%
#Create a corpus from each row in the dataframe
#declare a test and train set from the corpus and target labels
corpus = []
for row in likes_caption_df['caption']:
    if row == []:
        corpus.append('')
    else:
        corpus.append(str(' '.join(row)))

Xtrain, Xtext, ytrain, ytest = train_test_split(corpus, likes_caption_df['number_of_likes'])
#%%
#Create Tf-dif vectorizer
vector_tf = TfidfVectorizer(max_df=0.70, min_df= 0.02)
X = vector_tf.fit_transform(Xtrain)
popular_words_tf = vector_tf.get_feature_names()

vocab = vector_tf.vocabulary_
ignored_words = vector_tf.stop_words_


#%%
#Create a second corpus that is by each word
char_set = ('*', '@', '#','.','?','!',';', ':', '/', '/\/','(', ')', '<', '>', "'", '``')
corpus_two = []
for i in range(len(corpus)):
    words = word_tokenize(corpus[i])
    for j in range(len(words)):
        if words[j] not in char_set:
            corpus_two.append(words[j])
'''len(corpus_two) = 80273'''
#%%
#Create a frequency distribution for the words in the corpus_two
fdist = FreqDist(word for word in corpus_two)    
fdist.pprint(maxlen=15)
#%%


