# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 14:53:49 2018

@author: dicke
"""
from __future__ import absolute_import, print_function
#from birdy.twitter import UserClient
#import twitter
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import dataset
from sqlalchemy.exc import ProgrammingError
import csv

global writer

class StdOutListener(StreamListener):
    '''https://ljvmiranda921.github.io/notebook/2017/02/24/twitter-streaming-using-python/'''
    
    #global N
    #N = 0
    def on_status(self, status):
        print()
        print()
        #N += 1
        print(status.text)
        #with open('tweet_test.csv', 'w', encoding='utf8', newline='') as f1:
        
        writer = csv.writer(f1)   
        
        tweet = status.text.replace(',', ' ')
            #rint(f1.)
            
        #tweet = tweet.encode('ascii', 'ignore')
        tweet = tweet.replace('\\n', ' ')
        tweet = tweet.replace('\n', ' ')
        tweet = tweet.replace('\r', ' ')
        tweet = tweet.replace('\\r', ' ')
        tweet = tweet.replace('|', ' ')
        
        #post = post.replace('\n', ' ')
        writer.writerow([tweet, status.author.screen_name])
        #if N >= 2:
        return True
        
    def on_error(self,status_code):
        if status_code == 420:
            return False






CKEY = 'nX1iMiRwZKvnzXIRniMIwZXuA'
CSEC = '4MCD1ga2R7vXn2sWjvX4DVMkFhw0zf0ta02IwikYE49v0D0muT'
ATK = '1009550810240258048-1M4Dj2qdMhyUkHKCuJO8ffoVrYA5gF'
ATKS = 'RWFse0TpnH9IGAPXHM4Ozyu4e6oXP0gHuOGORLs5D5ncb'



if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(CKEY, CSEC)
    auth.set_access_token(ATK, ATKS)
    with open('july5kansas.csv', 'w', encoding='utf8', newline='') as f1:
        global writer
        writer = csv.writer(f1)
        stream = Stream(auth, l, tweet_mode='extended')
        print('Streaming...')
        stream.filter(track=['kansas school shooting', 'kansas elementary school'])
    
   
    






