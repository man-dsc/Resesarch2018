from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
import numpy as np
import csv
from sklearn import datasets
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import LeaveOneOut
from sklearn import metrics

def random_forest(X, Y, test):
    # Processing Text
    vector = CountVectorizer(min_df = 1)
    train_key = (vector.fit_transform(X)).toarray()
    
    # Classifier
    classifier = RandomForestClassifier()
    classifier.fit(train_key, Y)
    
    return classifier.predict((vector.transform(test).toarray()))

def get_training_set():
    tweet_path = "C:/Users/Summer16/Documents/Training Set/tweets.csv"
    review_path = "C:/Users/Summer16/Documents/Training Set/reviews.csv"
    tweet_source = open(tweet_path, 'rb')
    review_source = open(review_path, 'rb')
    tweet_reader = csv.reader(tweet_source)
    review_reader = csv.reader(review_source)
    tweets = list(tweet_reader)
    reviews = list(review_reader)
    
    tweet_key = []
    tweet_value = []
    review_key = []
    review_value = []
    
    for element in tweets:
        tweet_key.append(element[1].strip())
        tweet_category = element[-1].strip()
        if len(tweet_category) > 1:
            tweet_category = tweet_category[0]
        
        if tweet_category == 'b':
            tweet_category = 1
        if tweet_category == 'f':
            tweet_category = 2
        if tweet_category == 's':
            tweet_category = 3
        if tweet_category == 'u':
            tweet_category = 4
        if tweet_category == 'a':
            tweet_category = 5
        if tweet_category == 'r':
            tweet_category = 6
        
        tweet_value.append(tweet_category)
    
    for element in reviews:
        review_key.append(element[-3].strip() + ' ' + element[-2].strip())
        review_value.append(element[-1].strip())
    
    return tweet_key, tweet_value, review_key, review_value

def random_forest_cross_validation():
    # Get the data from Training Set
    tweet_key, tweet_value, review_key, review_value = get_training_set()    
    
    # Getting Results for Tweets 
    vector = CountVectorizer(min_df = 1)
    rfc = RandomForestClassifier(n_estimators = 20)  # 20 trees
    train_key = (vector.fit_transform(tweet_key)).toarray()
    predicted = cross_val_predict(rfc, train_key, tweet_value, cv=10)  # 10 fold
    accuracy = metrics.accuracy_score(tweet_value, predicted)
    precision = metrics.precision_score(tweet_value, predicted, average='weighted')
    recall = metrics.recall_score(tweet_value, predicted, average='weighted')
    f1 = metrics.f1_score(tweet_value, predicted, average='weighted')
    
    print('******* TWEET RESULTS *******')
    print('accuracy: ' + str(accuracy))
    print('precision: ' + str(precision))
    print('recall: ' + str(recall))
    print('f-measure: ' + str(f1))
    
    # Getting Results for Reviews
    vector = CountVectorizer(min_df = 1)
    rfc = RandomForestClassifier(n_estimators = 20)  # 20 trees
    review_key = (vector.fit_transform(review_key)).toarray()
    predicted = cross_val_predict(rfc, review_key, review_value, cv=10)  # 10 fold
    accuracy = metrics.accuracy_score(review_value, predicted)
    precision = metrics.precision_score(review_value, predicted, average='weighted')
    recall = metrics.recall_score(review_value, predicted, average='weighted')
    f1 = metrics.f1_score(review_value, predicted, average='weighted')
    
    print('******* REVIEWS RESULTS *******')
    print('accuracy: ' + str(accuracy))
    print('precision: ' + str(precision))
    print('recall: ' + str(recall))
    print('f-measure: ' + str(f1))
    
if __name__ == "__main__":
    random_forest_cross_validation()




