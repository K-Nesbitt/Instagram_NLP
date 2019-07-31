# Instagram NLP

## Background and Motivation 
I love to post on Instagram but I never know what to say in my caption. While scrolling on Instagram I began to wonder if there was a connection between the words used in the caption and the number of likes. I found one photo collage that had a higher than average number of likes for this user and analyzed the text in the caption. 

<img src="https://github.com/K-Nesbitt/Instagram_NLP/blob/master/images/presentation%20images/rich1.png" width="250" height="250">

*"Last day in Iceland. It’s been an amazing 11 days. Got to meet and work with some **amazing** people, work with an amazing company/brand, and got to play **model** while being on some epic **adventures**. I will never forget this trip and I’m looking forward to the next. Iceland, it’s been REAL, real! Shoutout to ... for extending their stay with me and for these bad ass and mostly basic shots. 😂😂 
 #iceland #niceland #LITlit #workaction #reykjavik #reiadventures #reishoot #bluelagoon **#mountains** #inclusivity **#beach #hiking** #whyhike #optoutside #adventures **#travel** #europe"*
 
This caption has a lot of buzz words like: adventure, model, travel, beach, mountains, etc. Do these words increase the number of likes for the photo?

As social media progresses so does business marketing. Many companies are now choosing to share their products through advertisements and posts on Instagram, Facebook, and Twitter. The question then becomes 'What text will lead to higher exposure and likes for a product?'

I used Natural Language Processing techniques and Machine Learning algorithms to predict which Instagram post will resonate most by analyzing caption text. The results of this project can lead to better marketing insights for businesses who mainly advertise with text on social media platforms. 

**Technologies Used:** 
Python, Pandas, Numpy, Selenium, Holoviews, Scikit-learn, NLTK, Regex


## Data Analysis
I collected data on Instagram by using the Selenium Chrome webdriver. I scraped 25 different users and collected a total of 11,529 captions with the number of likes. I also included the number of words in the caption, the users id, their total number of posts and total number of followers. 

The distribution of the number of likes is exponential with a lowering trend towards the maximum number of likes.  
<img src="https://github.com/K-Nesbitt/Instagram_NLP/blob/master/images/distribution_of_likes.png" width="350" height="350">

So the question continues, what causes certain posts to have more the average number of likes? For this set of data the average number of likes is 42. 

<img src="https://github.com/K-Nesbitt/Instagram_NLP/blob/master/images/avg_likes_by_user.png" width="350" height="350">


There appears to be no linear relationships in the data, so I have to consider a model that does not depend on a linear relationship. 
<img src="https://github.com/K-Nesbitt/Instagram_NLP/blob/master/images/bokeh_words_likes.png" width="350" height="350">

## Data Engineering

After processing the text in the captions with NLTK, I had a corpus of over 120,000 words. These were some of the words used most often:

<img src="https://github.com/K-Nesbitt/Instagram_NLP/blob/master/images/word_freq.png" width="350" height="350">

The word used most was **LOVE**. All of these top used words are considered positive, thus it was concluded that users posted a photo when they were in a good mood. 

I created a TF-IDF matrix with .25% of the words (about 600). Each caption then became a vector representing the presence of words included in the TF-IDF vocabulary set. 

## Results
I used the transformed matrix of captions with a Random Forest Regressor but could not predict the exact number of likes. 

I then added more features to the transformed matrix (number of words, user id, total followers, total posts) to make my prediction. I also changed the target from an actual value to a classification of above or below that users average number of likes. This made the model more specific to capture estimates for particular users. With a Random Forest Classifier I was able to get a precision score of 0.85 and recall of 0.58. The full summary of results are stated in the confusion matrix below:

<img src= "https://github.com/K-Nesbitt/Instagram_NLP/blob/master/images/Screen%20Shot%202019-07-30%20at%207.48.35%20PM.png" width="300" height="200">


## Reflection

