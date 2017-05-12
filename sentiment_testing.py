''' 
Sentiment Testing
Pattern, NLTK + one other sentiment analysis tool
'''

import sys; sys.path.append('/Users/Summer16/pattern-version-6')    
from pattern.en import sentiment                               
import os, codecs, csv                                        
import matplotlib.pyplot as plt
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pycorenlp import StanfordCoreNLP

''' Tweepy Authorization '''

consumer_key = '3x7aYWttzho8zn0tRMwo2H7jF'
consumer_secret = '4M3tgTJGbo9YyjuUmwcKSysnJPXxfXTorcxXBNb3H9HjJ6FDjN'
access_token = '2178454160-cyCz7IFgZPl6eJ20cdHBfdCz0Bkyt3k217kPtOc'
access_secret = 'Q2GKUw81JDCvDfPbxs2RDRTJITWouto8vrl413pTWCBHA'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

''' End Tweepy Authorization '''


''' Acquiring Tweets and Reviews '''

def get_tweet_list(app, category):
    tweet_list = []
    path = "C:/Users/Summer16/Documents/Summer '16 Henry/Twitter Data/Final_Compiled/Cleaned Text2/%s/%s.csv" % (category, app)
    source_file = open(path, 'rb')
    reader = csv.reader(source_file)
    data = list(reader)
    
    for i in range(len(data)):
        tweet_list.append(data[i][1])
    
    return tweet_list

def get_review_list(app):
    review_list = []
    path = "C:/Users/Summer16/Documents/Summer '16 Henry/Google Play Data/AB Reviews/%s.csv" % (app)
    source_file = open(path, 'rb')
    reader = csv.reader(source_file)
    data = list(reader)
    
    for i in range(len(data)):
        review_list.append(data[i][-3])
    
    return review_list

''' End Acquiring Tweets and Reviews '''


''' Sentiment Analysis Techniques - Pattern, NLTK, Vader, Stanford NLP, Sentistrength'''

def pattern_sentiment(app, category):
    tweet_sentiments = []
    review_sentiments = []
    tweet_list = get_tweet_list(app, category)
    review_list = get_review_list(app)
    tweet_count = 0
    review_count = 0
    tweet_err_count = 0
    review_err_count = 0
    
    for element in tweet_list:
        try:
            sentiment_tuple = sentiment(element)
            polarity = sentiment_tuple[0]
            subjectivity = sentiment_tuple[1]
            tweet_sentiments.append([polarity, subjectivity])
            print('Analyzing Tweets: %s / %s complete' % (str(tweet_count), str(len(tweet_list))))
            tweet_count += 1
        except KeyboardInterrupt:
            raise
        except:
            tweet_count += 1
            tweet_err_count += 1
            tweet_sentiments.append(-1)
            print('Error: Analyzing Tweets: %s / %s complete' % (str(tweet_count), str(len(tweet_list))))
            pass
            
    for element in review_list:
        try:
            sentiment_tuple = sentiment(element)
            polarity = sentiment_tuple[0]
            subjectivity = sentiment_tuple[1]
            review_sentiments.append([polarity, subjectivity])
            print('Analyzing Reviews: %s / %s complete' % (str(review_count), str(len(review_list))))
            review_count += 1
        except KeyboardInterrupt:
            raise
        except:
            print('Error: Analyzing Reviews: %s / %s complete' % (str(review_count), str(len(review_list))))
            review_count += 1
            review_err_count += 1
            review_sentiments.append(-1)
            pass 
    
    print("Pattern Error Count: %s, %s" % (tweet_err_count, review_err_count))
    return tweet_sentiments, review_sentiments

def nltk_sentiment(app, category):
    tweet_sentiments = []
    review_sentiments = []
    tweet_list = get_tweet_list(app, category)
    review_list = get_review_list(app)
    tweet_count = 0
    review_count = 0
    tweet_err_count = 0
    review_err_count = 0
    
    for element in tweet_list:
        try:
            element = TextBlob(element, analyzer = NaiveBayesAnalyzer())
            sent = element.sentiment
            tweet_sentiments.append(sent)
            print('Analyzing Tweets: %s / %s complete' % (str(tweet_count), str(len(tweet_list))))
            tweet_count += 1
        except KeyboardInterrupt:
            raise
        except:
            tweet_count += 1
            tweet_err_count += 1
            tweet_sentiments.append(-1)
            print('Error: Analyzing Tweets: %s / %s complete' % (str(tweet_count), str(len(tweet_list))))
            pass
        
    for element in review_list:
        try:
            element = TextBlob(element, analyzer = NaiveBayesAnalyzer())
            sent = element.sentiment
            review_sentiments.append(sent)
            print('Analyzing Reviews: %s / %s complete' % (str(review_count), str(len(review_list))))
            review_count += 1
        except KeyboardInterrupt:
            raise
        except:
            review_count += 1
            review_err_count += 1
            review_sentiments.append(-1)
            print('Error: Analyzing Reviews: %s / %s complete' % (str(review_count), str(len(review_list))))
            pass
    
    print("Tweepy NLTK Error Count: %s, %s" % (tweet_err_count, review_err_count))    
    return tweet_sentiments, review_sentiments

def vader_sentiment(app, category):
    tweet_sentiments = []
    review_sentiments = []
    tweet_parsed = []
    review_parsed = []
    tweet_list = get_tweet_list(app, category)
    review_list = get_review_list(app)
    
    tweet_count = 0
    review_count = 0
    tweet_err_count = 0
    review_err_count = 0
    
    analyzer = SentimentIntensityAnalyzer()
    
    for element in tweet_list:
        try:
            tweet_sentiments.append(analyzer.polarity_scores(element))
            print('Analyzing Tweets: %s / %s complete' % (str(tweet_count), str(len(tweet_list))))
            tweet_count += 1
        except KeyboardInterrupt:
            raise
        except:
            tweet_count += 1
            tweet_err_count += 1
            tweet_sentiments.append(-1)
            print('Error: Analyzing Tweets: %s / %s complete' % (str(tweet_count), str(len(tweet_list))))
            pass
        
    for element in review_list:
        try:
            review_sentiments.append(analyzer.polarity_scores(element))
            print('Analyzing Reviews: %s / %s complete' % (str(review_count), str(len(review_list))))
            review_count += 1
        except KeyboardInterrupt:
            raise
        except:
            review_count += 1
            review_err_count += 1
            review_sentiments.append(-1)
            print('Error: Analyzing Reviews: %s / %s complete' % (str(review_count), str(len(review_list))))
            pass
    
    for element in tweet_sentiments:
        tweet_parsed.append([element['pos'], element['neu'], element['neg']])

    for element in review_sentiments:
        review_parsed.append([element['pos'], element['neu'], element['neg']])
    
    print("VADER Error Count: %s, %s" % (tweet_err_count, review_err_count))    
    return tweet_parsed, review_parsed

def stanford_nlp_sentiment(app, category):
    tweet_sentiments = []
    review_sentiments = []
    tweet_list = get_tweet_list(app, category)
    review_list = get_review_list(app)

    tweet_count = 0
    review_count = 0
    tweet_err_count = 0
    review_err_count = 0
    
    nlp = StanfordCoreNLP('http://localhost:9000')
   
    for element in tweet_list:
        try:
            annotation = nlp.annotate(element, properties = {'annotators': 'sentiment', 'outputFormat': 'json'})      
            tweet_sentiments.append(int(annotation["sentences"][0]["sentimentValue"]))
            print('Analyzing Tweets: %s / %s complete' % (str(tweet_count), str(len(tweet_list))))
            tweet_count += 1
        except KeyboardInterrupt:
            raise
        except:
            tweet_count += 1
            tweet_err_count += 1
            tweet_sentiments.append(-1)
            print('Error: Analyzing Tweets: %s / %s complete' % (str(tweet_count), str(len(tweet_list))))
            pass
        
    for element in review_list:
        try:
            annotation = nlp.annotate(element, properties = {'annotators': 'sentiment', 'outputFormat': 'json'})      
            review_sentiments.append(int(annotation["sentences"][0]["sentimentValue"]))
            print('Analyzing Reviews: %s / %s complete' % (str(review_count), str(len(review_list))))
            review_count += 1
        except KeyboardInterrupt:
            raise
        except:
            review_count += 1
            review_err_count += 1
            review_sentiments.append(-1)
            print('Error: Analyzing Reviews: %s / %s complete' % (str(review_count), str(len(review_list))))
            pass
    
    return tweet_sentiments, review_sentiments


''' End Sentiment Analysis Techniques '''

''' Graphing Techniques '''

def vader_score(data):
    score_list = []
    for element in list(data):
        score_list.append(element['pos'] - element['neg'])
    return score_list

def graph_histogram(data):
    plt.hist(data)
    plt.xlim(-1, 1)
    plt.title("Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    #plt.savefig(title + '.png')
    plt.show()
    
def graph_distribution(data):
    x = []
    y = []    
    
    for element in data:
        x.append(element[0])
        y.append(element[1])
     
    plt.scatter(x, y, s = 10, c = 'gray')
    plt.xlim(-1, 1)
    plt.ylim(0, 1)
    plt.title('Sentiment Distribution')
    plt.xlabel('polarity')
    plt.ylabel('subjectivity')
    plt.show()

''' End Graphing Techniques ''' 


''' CSV compilation ''' 

def compile_csv(app, category, filename1, filename2):
    tweets = get_tweet_list(app, category)
    reviews = get_review_list(app)
    PatTweet, PatReview = pattern_sentiment(app, category)
    VadTweet, VadReview = vader_sentiment(app, category)
    StaTweet, StaReview = stanford_nlp_sentiment(app, category)

    tweet_list = []
    review_list = []
    
    for i in range(len(tweets)):
        tweet_list.append([tweets[i], PatTweet[i], VadTweet[i], StaTweet[i]])
    
    for j in range(len(reviews)):
        review_list.append([reviews[j], PatReview[j], VadReview[j], StaReview[j]])
    
    if not os.path.exists('C:/Users/Summer16/My Documents/Sentiments/'):
        os.makedirs('C:/Users/Summer16/My Documents/Sentiments/')
    
    if not os.path.exists('C:/Users/Summer16/My Documents/Sentiments/' + filename1):
        f = open('C:/Users/Summer16/My Documents/Sentiments/' + filename1, "w")
        f.close()
    
    with open('C:/Users/Summer16/My Documents/Sentiments/' + filename1, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(tweet_list)
        
    if not os.path.exists('C:/Users/Summer16/My Documents/Sentiments/' + filename2):
        f = open('C:/Users/Summer16/My Documents/Sentiments/' + filename2, "w")
        f.close()
        
    with open('C:/Users/Summer16/My Documents/Sentiments/' + filename2, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(review_list)   
    

if __name__ == "__main__":
    compile_csv('evernote', 'TopFree', 'evernote_tweets.csv', 'evernote_reviews.csv')
    pass