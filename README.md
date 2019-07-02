# Instagram NLP

Goal: The goal of this project is to discover the relationship between the caption and the number of likes on a picture from Instagram

Data Collection: I collected my data by scraping Instagram profiles and recorded the following information:
          - number of posts
          - number of followers
          - number of likes for pictures only
          - the caption of the photo

Issues: Some issues I encountered were getting the number of likes when it was not displayed as 
" Liked by users_friend and 30 others". If the post said "_ likes" then it was a button and I defaulted to say the number of likes was equal to 5. According to Instagram myth, if a frequent user likes your photo, no matter how few others liked it, then the post would still read "Liked by frequent_friend and _ others" and the _ others could be as small as 1. Therefore I assumed there would be a low number of posts that were not liked by a frequent friend of that user. 


## Exploratory Data Analysis

I collected data from 17 users (including myself). There was a total of 6806 posts.

The average number of posts was 432. 

![hist1](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_posts.png)

The lowest number of posts was 87 and the highest was 1386.

The average number of followers was 708. 

![hist2](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_followers.png)

The lowest number of followers was 169 and the highest was 2161 (a local musician).

The average number of likes is 31. The most likes was 402. (Again from the musician)
![hist3](https://github.com/K-Nesbitt/Instagram_likes_nlp/blob/master/images/number_of_likes.png)

## Results
Using sklearn's Tdidf text vectorizer I found the most popular names (term frequency of at least 2%) to be: 

## Reflection
I would like to collect data on more users outside of Austin and Texas. I would also like to collect data on the timestamp so that I could recommend the best time to post a picture and the words to use to maximize the number of likes. 

I realize that the goal of this project can seem superficial but it was really interesting to continue building my webscraping skills, see real world data with something that I use daily, and conduct natural language processing on the information that I found. 
