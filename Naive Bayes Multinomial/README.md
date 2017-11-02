# Tweet Classification (Naive Bayes Multinomial Implementation):
Reference: http://sebastianraschka.com/Articles/2014_naive_bayes_1.html

## Given:
A training set and a test set, each containing tweets and their corresponding locations (12 Locations in total for the training set).

## Task:
Based on Training set, create a Naive Bayes model which, just based on the content of the tweet, predicts the corresponding location

## Approach:
Naive Bayes Multinomial Implementation:

Every tweet in the test set contains specific words (w1, w2, w3 ... wN)

Probability(Location | w1,w2,w3...wn) = Probability(location) * Probability(w1,w2,w3...wN | Location) / Probability(w1,w2,w3...wN)

By Naive Bayes Assumption, given a class (Location in this case), all other factors / variables are independent of each other.
So,

P(Location | w1,w2,w3...wn) = P(location) * P(w1| Location)* P(w2| Location)...* P(wN| Location) / P(w1,w2,w3...wN) 

P(wN | Location) 
= Number of times 'wN' word has appeared in training set for all tweets in that Location / Total words in all tweets of that location

For all the locations, denominator is constant.
So, for every location, we compute the numerator, and assign location to the tweet for which numerator is maximum.

## Additional Smoothing and Operations in the Equation:
- A) Laplace Smoothing: (For every P(wN | Location), Numerator has been added by 1, and denominator by count of unique words.
It has been done to prevent any probability from becoming 0 
- B) Log of Probabilities - Since the probability can become infinitesimal, log has been taken. log(A*B*C) = logA + logB + logC
- C) Skipping New word - If a new word comes, which has never been encountered in Training data set, it has been skipped. 
If all words are new, then the city with the maximum count in training data will be assigned (since P(Location) will be highest)


## Data Cleaning:
From the training and test inputs, following cleaning operations have been done:
1) Punctuations and symbols have been removed.
2) Stop words have been ignored.
3) All words converted to Lower case
4) Words have been trimmed till the length of 5
5) If total count of any word is only 1, it has been ignored

## Implementation:
A separate dictionary for 'words', 'training words', 'cities' and 'test_tweet' have been made.

1) words- contains all words, with their corresponding total count and count in any particular city
eg: `{'night':{'Cities':{'Washington':90, 'New York': 39},'Total Count: 345'}}`

2) training words - subset of words which you want to consider for training
Format similar to words

3) cities - list of cities, with the total count of tweets, and total count of words in tweets of the city in training data
eg: `{'Atlanta,_GA': {'Count_Tweets': 1910, 'Count_Words': 22236}}`

4) test tweet - Actual City, Predicted city, log of probability for all cities, and tweet 
eg: 
```
{1: {'Actual_City': 'Washington,_DC',
  'Cities_Probability': {'Atlanta,_GA': -65.40391952512454,
   'Boston,_MA': -69.06901104949196,   
   'San_Francisco,_CA': -66.30099526766189,
   'Toronto,_Ontario': -65.10784692886673,
   'Washington,_DC': -65.2815225233324},
  'Predicted_City': 'Chicago,_IL',
  'Tweet': 'So many activities! Drink specials all night!\r\r#bbqhappyhour #bbqjoint14th #acreativedc\xc9 \n'}}
```
Calling the program:
```
python geolocate.py tweets.train.txt tweets.test1.txt output_final.txt
```

## Result:
The model has a prediction accuracy of 66%. 330 out of 500 tweets have been predicted correctly.

There are 12 cities in total. So, by pure guess work, we would have been able to predict on an average 
500 / 12 = 42 cities correctly, giving accuracy of less than 10%

Naive Bayes gives a far superior accuracy of 66%, and it keeps learning based on the usage of words by the people, without
any application of rules
