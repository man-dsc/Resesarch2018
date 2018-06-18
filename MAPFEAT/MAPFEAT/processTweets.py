# Processes a data file and training set file of tweets
#
# Lemmatizes and removes duplicate tweets, stop words, urls, hashtags, special characters, and digits
#
# 1. Processes the training set               -> processedTweets/processed<filename>.csv
# 2. Processes the data set                   -> processedTweets/processed<filename>.csv
#
# Assumes that the tweets are in the first column of the csv and the category is in the second
#
# Based off of pre-lemmatization.py, lemmatization.py, and pre-processing.py by Henry Cho


import os
import csv
import pattern.vector
import re
import shutil
import sys
from pattern.vector import Document, NB
from pattern.en import parse
from stop_words import get_stop_words

INPUT_PATH = 'data/'
OUTPUT_PATH = 'output/processedTweets'

DATASET_FILENAME = 'dataSet.csv'
TRAININGSET_FILENAME = 'trainingSet.csv'


def processFile(filename):
    print('Processing {}...'.format(filename))
    data = open(INPUT_PATH + filename, 'rb')
    reader = csv.reader(data)
    info = list(reader)

    tweets = []
    results = []
    for i in range(len(info)):
        print(info[i])
        tweet = preProcess(info[i][0])
        if tweet:
            # Map the words into their dictionary form
            tweet = lemmatize(tweet)

            if tweet not in tweets:
                tweets.append(tweet)
                results.append([tweet, info[i][1]])

    with open('{}/processed{}'.format(OUTPUT_PATH, filename.capitalize()), 'wb+') as f:
        writer = csv.writer(f)
        writer.writerows(results)

    
def preProcess(tweet):
    tweet = re.sub(r'(?:\@|https?\://)\S+', ' ', tweet)
    tweet = re.sub(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', ' ', tweet)
    tweet = re.sub(r'<quote>', ' ', tweet)
    tweet = re.sub(r'[^\x00-\x7f]', ' ', tweet)
    tweet = re.sub(r'\r', ' ', tweet)
    tweet = re.sub(r'&amp', ' ', tweet)
    tweet = re.sub(r'&gt', ' ', tweet)
    tweet = re.sub(r'\d+', ' ', tweet)

    tweet = tweet.lower()

    tweet = tweet.replace("&quot;", '"')
    tweet = tweet.replace("&#39;", "'")
    tweet = tweet.replace("&gt;", '>')
    tweet = tweet.replace("&lt;", '<')
    tweet = tweet.replace("\\'", "'")

    chars = [',',' ','"','*',')','(','"',"'",'%','|','~','=',';',':','?','!','.','$','%','&','+','/','^',' - ','@','_','\\n','\\r',"\\'",'&;','&#','\\','#','>','<', 'RT ']
    for char in chars:
        tweet = tweet.replace(char, ' ');

    stop_words = get_stop_words('english')
    for word in stop_words:
        tweet = tweet.replace(' {} '.format(word), ' ');

    # Remove all extra whitespace
    tweet = ' '.join(tweet.split())
    tweet = tweet.strip()
    return tweet


def lemmatize(tweet):
    rawResult = parse(tweet, 
                   tokenize = False,
                   tags = False,
                   chunks = False,
                   relations = False,
                   lemmata = True,
                   encoding = 'utf-8',
                   tagset = None)
    rawResult = str(rawResult)
    rawResult = rawResult.split(' ')
     
    result = ''     
    for element in rawResult:
        res = ''        
        count = 0
        index = 0
        for i in range(len(element)):   
            if element[i] == '/':
                count += 1
            if count == 2:
                index = i + 1
                break
        for j in range(index, len(element)):
            res += element[j]
        result += (res + ' ')
    result = result.strip()
    return result


def process():
    print('')
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    processFile(TRAININGSET_FILENAME)
    processFile(DATASET_FILENAME)


if __name__ == "__main__":
    process()
