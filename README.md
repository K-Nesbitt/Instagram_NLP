# Instagram NLP

## Background and Motivation 
I love to post on Instagram but I never know what to say in my caption. While scrolling on Instagram I began to wonder if their was a connection between the words used in the caption and the number of likes. I found one photo collage that had a higher than average number of likes for this user and analyzed the text in the caption. 

![pic1](https://github.com/K-Nesbitt/Instagram_NLP/blob/master/images/presentation%20images/rich1.png)

*"Last day in Iceland. It’s been an amazing 11 days. Got to meet and work with some **amazing** people, work with an amazing company/brand, and got to play **model** while being on some epic **adventures**. I will never forget this trip and I’m looking forward to the next. Iceland, it’s been REAL, real! Shoutout to ... for extending their stay with me and for these bad ass and mostly basic shots. 😂😂 
 #iceland #niceland #LITlit #workaction #reykjavik #reiadventures #reishoot #bluelagoon **#mountains** #inclusivity **#beach #hiking** #whyhike #optoutside #adventures **#travel** #europe"*
 
This caption has a lot of buzz words like: adventure, model, travel, beach, mountains, etc. Do these words increase the number of likes for the photo?

As social media progresses so does business marketing. Many companies are now choosing to share their products through advertisements and posts on Instagram, Facebook, and Twitter. The question then becomes 'What text will lead to higher exposure and likes for a product?'

I used Natural Language Processing techniques and Machine Learning algorithms to predict which Instagram post will resonate most by analyzing caption text. The results of this project can lead to better marketing insights with social media platforms who advertise mainly by text. 

**Technologies Used::** 
Python, Pandas, Numpy, Selenium, Holoviews, Scikit-learn, NLTK, Regex


## Data Analysis



## Results
I ran the train and test sets on a Random Forest with 100 trees, and a Linear Regression.

                    Random Forest score: -0.07604367797726175
                    
                    Linear Regression score: -0.05412067220144978 

I played around with a few parameters but my conclusion is that my data was too sparse, there was errors in my scraping code, there was no correlation between captions and number of likes, and I needed more features in the data set. 

## Reflection

