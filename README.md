# Instagram NLP

**Goal**: The goal of this project is to discover the relationship between the caption and the number of likes on a picture from Instagram

**Data Collection**: I collected my data by scraping Instagram profiles and recorded the following information:
  * number of posts 
  * number of followers 
  * number of likes for pictures only 
  * the caption of the photo 

## Exploratory Data Analysis

I collected data from 17 users (including myself). There was a total of 6806 posts.

The average number of posts was 432 per user. 

![hist1](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_posts.png)

The lowest number of posts was 87 and the highest was 1386.

The average number of followers was 708 per user. 

![hist2](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_followers.png)

The lowest number of followers was 169 and the highest was 2161 (a local musician).

The average number of likes is 31 per picture.
                    
![hist3](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_likes.png)

The most number of likes was 402, again from the local musician. The caption read: 

*"Last day in Iceland. It’s been an amazing 11 days. Got to meet and work with some amazing people, work with an amazing company/brand, and got to play model while being on some epic adventures. I will never forget this trip and I’m looking forward to the next. Iceland, it’s been REAL, real! Shoutout to @jamesharnoisphoto and @hownottotravellikeabasicbitch for extending their stay with me and for these bad ass and mostly basic shots. 😂😂 
 #iceland #niceland #LITlit #workaction #reykjavik #reiadventures #reishoot #bluelagoon #mountains #inclusivity #beach #hiking #whyhike #optoutside #adventures #travel #europe"*

**Why is there a peak at 5 likes?**
I set a default in my scraping code and it was obviously an error. 
                    
The total number of "words" are about 76,400.


![plot1](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/freq2_plot.png)


Using sklearn's Tf-idf text vectorizer I found the most popular names to be:

**_Top 3%_**

beauti, day, friend, get, go, good, got, great, happi, im, know, life, 

like, **lit**, littl, love, make, new, one, see, thank, time, today, work, year

**_Top 5%_**

day, love, time, today


**_Only word in top 10% (most used word): LOVE_**

I created a vector with a **minimum document frequency of .25%**  which contained **786 words** in the vocabulary set 
(about 1% of the total words).

There were 10485 ignored words:

          {central, schwinn, aspir, horatio, grandfath, supportthemov, mysong, buongiorno, splash, earn, 
          weallscreamforicecream, livebig, hermitfal, whoever, accur, recalibr, af, lifetim, catsoutofthebag, 
          sidelin, munchkin, blacksand, beatbama, californiaadventur, goldenbirthday, bekind, tidbitnippi, 
          nerdingout, worldtradecent ...}

## Results
I ran the train and test sets on a Random Forest with 100 trees, and a Linear Regression.

                    Random Forest score: -0.07604367797726175
                    
                    Linear Regression score: -0.05412067220144978 

I played around with a few parameters but my conclusion is that my data was too sparse, there was errors in my scraping code, there was no correlation between captions and number of likes, and I needed more features in the data set. 

## Reflection
I plan to continue this project by updating my scraping code to fix the error capturing the actual number of likes and collect the timestamp of the picture. When organizing the data I can add another feature of the total number of followers (still with caution as the number of followers changes over time). I would also like figure out how to separate emoji's and then identify them as tokens as well as address multiple words that are strung together in hashtags. 

With a new model I could recommend the best time to post a picture and the words to use to maximize the number of likes. 

I realize that the goal of this project can seem superficial but it was really interesting to continue building my webscraping skills, see real world data with something that I use daily, and conduct natural language processing on the information that I found. 
