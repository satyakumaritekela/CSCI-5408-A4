'''
Created on Apr. 7, 2020

@author: satya
'''
import requests
import csv
import json
import re

tweets_data = []
tweets_BOW = []
postive_words = []
negative_words = []

with open('tweets.json', 'r', encoding='UTF-8') as jsonFile:
    # loading json
    tweets_data = json.load(jsonFile)
    
# counting of frequency of words in a sentence
def word_count(str):
    word_count = dict()
    words = str.split()

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

# creating a bag of words list
i = 1;
for tweet in tweets_data:
    try:
        bagOfWords = word_count(tweet['Text'])
        tweets_BOW.append({
            "bow"+ str(i) : bagOfWords
        }) 
        i = i + 1;
    except KeyError:
        pass   
        
# write the data into the json file
with open('tweets_bow.json', 'w', encoding='UTF-8') as jsonFile:
    json_formatted_tweets_data = json.dumps(tweets_BOW)
    json.dump(json.loads(json_formatted_tweets_data), jsonFile, indent=4, sort_keys=True)
    
# Split positive, negative words
def splitPositiveWords():
    with open("PositiveWords.txt", 'r') as PositiveWords:
        return PositiveWords.read().split("\n")

def splitNegativeWords():
    with open("NegativeWords.txt", 'r') as NegativeWords:
        return NegativeWords.read().split("\n")
    
# retrieving positive and negative words into the list
postive_words = splitPositiveWords()
negative_words = splitNegativeWords()

# finding polarity of each tweet
with open("tweets.json", 'r') as inputFile:
    tweets_data = json.load(inputFile)
    with open('tweets_sentiment.csv', mode='w', newline='', encoding="utf-8") as outputFile:
        tweet_count = 1;
        csvWriter = csv.writer(outputFile);
        csvWriter.writerow(['Tweet', 'Message/tweets', 'match', 'polarity']);
        
        # iterating each tweet
        for tweet in tweets_data:
            try:
                bagOfWords = word_count(tweet['Text'])
                i = i + 1;
            except KeyError:
                pass  
            
            IsPostiveOrNegative = False
            
            # finding sentiment of each tweet
            for word in bagOfWords.keys():
                if word in postive_words:
                    csvWriter.writerow([tweet_count, tweet['Text'], word, "Positive"])
                    IsPostiveOrNegative = True
                    break;
                elif word in negative_words:
                    csvWriter.writerow([tweet_count, tweet['Text'], word, "Negative"])
                    IsPostiveOrNegative = True
                    break;
                    
            if not IsPostiveOrNegative:
                csvWriter.writerow([tweet_count, tweet['Text'], "", "Neutral"])
                
            tweet_count = tweet_count + 1
            