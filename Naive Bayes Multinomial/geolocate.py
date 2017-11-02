#Report given in Readme File
import sys
import re
from math import log
def readfile(infile):
    global train_tweet_count
    word_dict = {}    
    city_dict={}
    with open(infile, 'r') as f:
        for line in f:
            train_tweet_count=train_tweet_count+1
            city, tweet = line.split(' ', 1) # Separate city and tweet
            if city not in city_dict:
                city_dict[city]={}
                city_dict[city]['Count_Words']=0
                city_dict[city]['Count_Tweets']=1
            else:
                city_dict[city]['Count_Tweets'] = city_dict[city]['Count_Tweets'] + 1            
            word_list = get_words(tweet) # Get only the lowercase words
            city_dict[city]['Count_Words']=city_dict[city]['Count_Words'] + len(word_list)            
            fill_dictionary(city, word_list, word_dict) # Fill in the word_dict            
    return word_dict,  city_dict


def readtestfile(infile,train_words,cities):
    #global train_tweet_count
    len_train_words = len(train_words)    
    with open(infile, 'r') as f:
        test_tweet={}
        count = 0
        for line in f:
            count += 1
            city, tweet = line.split(' ', 1) # Separate city and tweet                        
            word_list = get_words(tweet) # Get only the lowercase words
            for i in list(range(0,len(word_list))):
                if len(word_list[i]) > 5:
                    word_list[i] = word_list[i][0:5]
            test_tweet[count] = {}
            test_tweet[count]['Actual_City'] = city
            test_tweet[count]['Predicted_City'] = ''
            test_tweet[count]['Tweet'] = tweet
            test_tweet[count]['Cities_Probability'] = {}
            max_log_probability = -float("inf")
            max_probable_city = ''
            for city in cities:
               city_word_count = cities[city]['Count_Words'] 
               test_tweet[count]['Cities_Probability'][city] = log( float(cities[city]['Count_Tweets']) / float(train_tweet_count)) 
               for word in word_list:
                   try:                  
                       test_tweet[count]['Cities_Probability'][city] = test_tweet[count]['Cities_Probability'][city] + log(float(train_words[word]['Cities'][city]+1) / float(city_word_count + len_train_words ))
                   except:
                       continue
               if test_tweet[count]['Cities_Probability'][city] > max_log_probability:
                   max_log_probability = test_tweet[count]['Cities_Probability'][city]
                   max_probable_city = city
                   test_tweet[count]['Predicted_City'] = max_probable_city
                                              
    return test_tweet



def fill_dictionary(city, word_list, word_dict):
    for word in word_list:
        if word in stop_words or word.isdigit()==True or len(word)<2:
            continue
        if len(word)>5:
            word = word[0:5]
        if word in word_dict:
            word_dict[word]['Total_Count'] +=1
            if city in word_dict[word]['Cities']:
                word_dict[word]['Cities'][city] += 1
            else:
                word_dict[word]['Cities'][city] = 1
        else:            
            word_dict[word] = {}
            word_dict[word]['Cities']={}
            word_dict[word]['Cities'][city] = 1
            word_dict[word]['Total_Count']=1



def get_words(tweet):
    return [word.lower() for word in re.split(r"[\W_]", tweet) if word != '']

#Main Start
stop_words = ['a','an','and','are','the','as', 'at', 'be' ,'by' ,'us','it','too','she' ,'for', 'from', 'has','he', 'in', 'yes','is', 'its', 'of', 'on', 'that', 'to', 'was', 'were', 'will', 'with','my','you','mine','yours','we','can','this','our','because','him','his','her']    
training_file = sys.argv[1]
testing_file = sys.argv[2]
output_file = sys.argv[3]
train_tweet_count=0
#Making Words, cities and hashtag dic
words, cities = readfile(training_file)

#Filling up 0 for cities not there for word
for word in words:
    for city in cities:
        if city not in words[word]['Cities']:
            words[word]['Cities'][city]=0
    

#Making list of Train - words
train_words = words            
for word in list(train_words.keys()):
    if train_words[word]['Total_Count']==1:
        del(train_words[word])
#test file
#Laplace smoothing done to all just to be on safe side
test_tweet = readtestfile(testing_file,train_words,cities)

#Accuracy
count_correct=0
for key in test_tweet:
    if test_tweet[key]['Actual_City'] == test_tweet[key]['Predicted_City']:
        count_correct = count_correct + 1

accuracy = float(count_correct) / float(len(test_tweet))


#Printing Top 5 words associated with each location
for city in cities:
    city_words_array=[]
    city_word_count_array=[]
    top_5_words_city = []
    i = 1    
    for word in train_words:                
        city_words_array.append(word)
        city_word_count_array.append(train_words[word]['Cities'][city])
    while i <= 5:        
        index = city_word_count_array.index(max(city_word_count_array))
        top_5_words_city.append(city_words_array.pop(index))
        del(city_word_count_array[index])
        i += 1
    print( city + " " + " ".join([word for word in top_5_words_city]))        
    
    
#Writing to Output
f = open(output_file , "a+")
for index in test_tweet:
   f.write( test_tweet[index]['Predicted_City'] + " " + test_tweet[index]['Actual_City'] + " " +  test_tweet[index]['Tweet'])
f.close()