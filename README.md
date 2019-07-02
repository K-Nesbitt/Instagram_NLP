# Instagram NLP

**Goal**: The goal of this project is to discover the relationship between the caption and the number of likes on a picture from Instagram

**Data Collection**: I collected my data by scraping Instagram profiles and recorded the following information:
          - number of posts
          - number of followers
          - number of likes for pictures only
          - the caption of the photo

**Issues**: Some issues I encountered were getting the number of likes when it was not displayed as 
" Liked by users_friend and 30 others". If the post said "_ likes" then it was a button and I defaulted to say the number of likes was equal to 5. According to Instagram myth, if a frequent user likes your photo, no matter how few others liked it, then the post would still read "Liked by frequent_friend and _ others" and the _ others could be as small as 1. Therefore I assumed there would be a low number of posts that were not liked by a frequent friend of that user. 


## Exploratory Data Analysis

I collected data from 17 users (including myself). There was a total of 6806 posts.

The average number of posts was 432. 

![hist1](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_posts.png)

The lowest number of posts was 87 and the highest was 1386.

The average number of followers was 708. 

![hist2](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_followers.png)

The lowest number of followers was 169 and the highest was 2161 (a local musician).

The average number of likes is 31.
                    
![hist3](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_likes.png)

The most number of likes was 402, again from the local musician. The caption read: 

*"Last day in Iceland. It’s been an amazing 11 days. Got to meet and work with some amazing people, work with an amazing company/brand, and got to play model while being on some epic adventures. I will never forget this trip and I’m looking forward to the next. Iceland, it’s been REAL, real! Shoutout to @jamesharnoisphoto and @hownottotravellikeabasicbitch for extending their stay with me and for these bad ass and mostly basic shots. 😂😂 
 #iceland #niceland #LITlit #workaction #reykjavik #reiadventures #reishoot #bluelagoon #mountains #inclusivity #beach #hiking #whyhike #optoutside #adventures #travel #europe"*
                    
## Results
The total number of words (or strings since there are emojis and words with emojis) is 81,125.
Using sklearn's Tdidf text vectorizer I found the most popular names to be:

**_Top 3%_**

beauti, day, friend, get, go, good, got, great, happi, im, know, life, 

like, **lit**, littl, love, new, night, one, see, thank, time, today, work, year

**_Top 5%_**

day, get, love, time, today


**_Only word in top 10% (most used word): LOVE_**



## Reflection
I would like to collect data on more users outside of Austin and Texas. I would also like to collect data on the timestamp so that I could recommend the best time to post a picture and the words to use to maximize the number of likes. 

I realize that the goal of this project can seem superficial but it was really interesting to continue building my webscraping skills, see real world data with something that I use daily, and conduct natural language processing on the information that I found. 
