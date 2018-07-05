# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 12:23:58 2018

@author: dicke
"""


import tweepy
import csv
import sys
#import jsonpickle
import os
import pandas as pd




####input your credentials here
consumer_key = 'nX1iMiRwZKvnzXIRniMIwZXuA'
consumer_secret = '4MCD1ga2R7vXn2sWjvX4DVMkFhw0zf0ta02IwikYE49v0D0muT'
access_token = '1009550810240258048-1M4Dj2qdMhyUkHKCuJO8ffoVrYA5gF'
access_token_secret = 'RWFse0TpnH9IGAPXHM4Ozyu4e6oXP0gHuOGORLs5D5ncb'

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

searchQuery = 'Santa fe school'
tweetsPerQry = 100
maxTweets=100000
sinceId = None
max_id = -100
fName = 'newsf4.csv'

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w', encoding='utf8', newline='') as csvFile:
    csvWriter = csv.writer(csvFile)
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended')
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId, tweet_mode='extended')
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1), tweet_mode='extended')
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId, tweet_mode='extended')
            if not new_tweets:
                print("No more tweets found")
                break
            for twt in new_tweets:
                tweet = twt.full_text
                tweet = tweet.replace('\\n', ' ')
                tweet = tweet.replace('\n', ' ')
                tweet = tweet.replace('\r', ' ')
                tweet = tweet.replace('\\r', ' ')
                tweet = tweet.replace('|', ' ')
                csvWriter.writerow([tweet])
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))


#csvFile = open('Santafe.csv', 'a')


'''
for tweet in tweepy.Cursor(api.search,q="#santafestrong",count=3000,
                           lang="en",
                           since="2018-05-17").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    '''