'''
Created on Apr. 8, 2020

@author: satya
'''
import requests
import csv
import json
import re
import fileConverter
import math

# Authorization Key
Authorization_Key = {'Authorization': 'a41eae4d71ff4208be38488c39dcf880'}

# URl for retrieving the data
News_URL = 'https://newsapi.org/v2/everything'

# Keywords that needs to extract the data that are sent as a parameters in the URL
parametersForDal = {'q': 'Dalhousie University', 'language': 'en',
                      'sortBy': 'relevancy', 'pageSize': 100}
# retrieving the response for the given parameters
responseDal = requests.get(url = News_URL, headers = Authorization_Key, params = parametersForDal)
# encoding to JSON Objects
response_string_dal = json.dumps(responseDal.json())
json_Response_dal = json.loads(response_string_dal)

parametersForHalifax = {'q': 'Halifax', 'language': 'en',
                      'sortBy': 'relevancy', 'pageSize': 100}
responseHal = requests.get(url = News_URL, headers = Authorization_Key, params = parametersForHalifax)
response_string_hal = json.dumps(responseHal.json())
json_Response_hal = json.loads(response_string_hal)

parametersForCanada = {'q': 'Canada', 'language': 'en',
                      'sortBy': 'relevancy', 'pageSize': 100}
responseCan = requests.get(url = News_URL, headers = Authorization_Key, params = parametersForCanada)
response_string_Can = json.dumps(responseCan.json())
json_Response_Can = json.loads(response_string_Can)

parametersForUniv = {'q': 'University', 'language': 'en',
                      'sortBy': 'relevancy', 'pageSize': 100}
responseUniv = requests.get(url = News_URL, headers = Authorization_Key, params = parametersForUniv)
response_string_Uni = json.dumps(responseUniv.json())
json_Response_Uni = json.loads(response_string_Uni)

parametersForEdu = {'q': 'Canada Education', 'language': 'en',
                      'sortBy': 'relevancy', 'pageSize': 100}
responseEdu = requests.get(url = News_URL, headers = Authorization_Key, params = parametersForEdu)
response_string_Edu = json.dumps(responseEdu.json())
json_Response_Edu = json.loads(response_string_Edu)

# creating the article list json
articles_list = json_Response_dal['articles'] + json_Response_hal['articles'] + json_Response_Can['articles'] + json_Response_Uni['articles'] + json_Response_Edu['articles']

# initializing articles data
articles_data = []

# pattern that filters out the emoticons,symbols and other map symbols
emojiPattern = re.compile("["
                u"\U0001F600-\U0001F64F"
                u"\U0001F300-\U0001F5FF"
                u"\U0001F680-\U0001F6FF" 
                u"\U0001F1E0-\U0001F1FF"
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
            "]+")

# takes the data and clears the emoji patterns and special characters and URL's
def clear_Patterns(ip_text):
    ip_text = emojiPattern.sub(r'', ip_text)
    ip_text = " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", ip_text).split()) 
    return ip_text if ip_text != "" else "NAN"

# iterating through the response loop for filtering the emoticons,symbols and other map symbols
for article in articles_list:
    # if author and content is none enter NAN
    if article['description'] is None:
        article['description'] = 'NAN'
    if article['description'] == "":
        article['description'] = 'NAN'
    if article['content'] is None:
        article['content'] = 'NAN'
    if article['content'] == "":
        article['content'] = 'NAN'
    # append all the articles data
    articles_data.append({
        'title': clear_Patterns(article['title']),
        'description': article['description'],
        'content': clear_Patterns(article['content']) 
    })

# write the data into the json file
with open('news.json', 'w') as jsonFile:
    json_formatted_articles_data = json.dumps(articles_data)
    json.dump(json.loads(json_formatted_articles_data), jsonFile, indent=4, sort_keys=True)

# converting json to txt and cav format
fileConverter.changeToText("news.json", "news.csv", "news.txt")

# Create Individual Articles
def createIndividualArticles(fileCount):
    with open('news.csv','r', encoding="utf-8") as csvFile:
        article = csv.reader(csvFile)
        next(article)
        for line in article:
            articleFile = open('article-' + str(fileCount) + ".txt", "w", encoding="utf-8")
            articleFile.write(line[0])
            articleFile.write(line[1])
            articleFile.write(line[2])
            articleFile.close
            fileCount += 1
    return fileCount

# Retrieve All articles
totalNumberOfFiles = createIndividualArticles(1)

# word list to find the frequncy
wordsList = ['Canada', 'University', 'Dalhousie University', 'Halifax', 'Business']

# function that finds the frequency count of the word canada
def frequencyCount(writerTD_IDF, N):
    with open("frequency_count.csv", mode='w', newline="", encoding="utf-8") as FreqCountFile:
        writerFreqCount = csv.writer(FreqCountFile)
        writerFreqCount.writerow(['Term', "Canada"])
        writerFreqCount.writerow(['Canada appeared in all documents', "Total Words (m)", "Frequency (f)"])
        max_frequency = -1;
        for word in wordsList:
            fileNo = 1
            df = 0
            totalWords = 0;
            while fileNo < totalNumberOfFiles:
                f = 0
                frequency = 0
                articleFile = open("article-" + str(fileNo) + ".txt", "r", encoding="utf-8")
                article = articleFile.readline()
                if article.find(word) != -1:
                    frequency = article.count(word)
                    totalWords = len(article.replace(","," ").split(" "))
                    if word.lower() == "canada":
                        if frequency / totalWords > max_frequency:
                            max_frequency = frequency / totalWords
                            max_article = "article-" + str(fileNo) + ".txt"
                        f += frequency;
                        writerFreqCount.writerow(["article-" + str(fileNo) , str(totalWords), str(f)])
                    df += frequency
                articleFile.close()
                fileNo += 1
            try:
                frequency = N / df
                log_frequency = math.log(frequency)
                writerTD_IDF.writerow([word, str(df), str(N) + "/" + str(df), str(round(log_frequency, 2))])
            except ZeroDivisionError:
                continue
    return max_article

# function that helps to find the frequency
def termFrequencyInverse(wordsList, N):
    with open("TF-IDF.csv", mode='w', newline="", encoding="utf-8") as TDFile:
        writerTD_IDF = csv.writer(TDFile)
        writerTD_IDF.writerow(['Total Documents', str(N)])
        writerTD_IDF.writerow(['Search Query', "Document containing term(df)", "Total Documents(N)/ number of documents term appeared (df)", "Log10(N/df)"])
        max_article = frequencyCount(writerTD_IDF, N);
    return max_article;
                
max_article = termFrequencyInverse(wordsList, totalNumberOfFiles)
print(max_article)

max_article = open(max_article, "r")
print(max_article.read())