# Evaluates the processed training set and applies Naive Bayes to the processed data set
#
# 1. Evaluates the processed training set
# 2. Classifies the processed data set        -> classifiedTweets/results.csv
# 3. Sorts the results                        -> classifiedTweets/informative.csv and classifiedTweets/noninformative.csv
#
# Based off of NB_SVM.py by Henry Cho


import os
import csv
import pattern.vector
import shutil
import sys
from pattern.vector import Document, NB, kfoldcv

INPUT_PATH = 'output/processedTweets'
OUTPUT_PATH = 'output/classifiedTweets'

DATASET_FILENAME = 'dataSet.csv'
TRAININGSET_FILENAME = 'trainingSet.csv'


def buildTrainingSet():
    data = open('{}/processed{}'.format(INPUT_PATH, TRAININGSET_FILENAME.capitalize()), 'rb')
    reader = csv.reader(data)
    info = list(reader)

    trainingSet = []
    for i in range(len(info)):
        tweet = info[i][0]
        category = info[i][1]
        trainingSet.append([tweet, category])
    return trainingSet


def validate(trainingSet):
    #Displays as (accuracy, precision, recall, F1, stdev)
    print('\n10-fold cross validation results on training set:')
    print(kfoldcv(NB, trainingSet, folds=10))
    print('')
    return kfoldcv(NB, trainingSet, folds=10)


def classifyTweets(filename, trainingSet):
    print('Classifying {}...\n'.format(filename))
    data = open('{}/processed{}'.format(INPUT_PATH, filename.capitalize()), 'rb')
    reader = csv.reader(data)
    info = list(reader)

    classifier = NB(train = trainingSet, alpha = 0.0001)

    tweets = []
    for i in range(len(info)):
        tweet = info[i][0] 
        result = classifier.classify(Document(tweet))
        tweets.append([tweet, result])

    # Write all tweets to file
    with open('{}/results.csv'.format(OUTPUT_PATH), 'wb+') as f:
        writer = csv.writer(f)
        writer.writerows(tweets)


def writeResults():
    results = open('output/classifiedTweets/results.csv', 'rb')
    reader = csv.reader(results)
    info = list(reader)

    informative = []
    noninformative = []    

    # Sorts results into informative vs uninformative
    for i in range(len(info)):
        category = info[i][-1]
        category = category.replace('\r\n', '')
        category = category.strip()

        if category == 'Y':
            informative.append(info[i])

        elif category == 'N':
            noninformative.append(info[i])

    # Writes informative tweets to file
    with open('{}/informative.csv'.format(OUTPUT_PATH), 'wb+') as f:
        writer = csv.writer(f)
        writer.writerows(informative)

    # Writes uninformative tweets to file
    with open('{}/nonInformative.csv'.format(OUTPUT_PATH), 'wb+') as f:
        writer = csv.writer(f)
        writer.writerows(noninformative)


def classify():
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    # Creates a list from the training set
    trainingSet = buildTrainingSet()

    # Validates the training set using 10-fold cross validation
    results = validate(trainingSet)

    # Uses the manually-classified training set to classify the rest of the tweets
    classifyTweets(DATASET_FILENAME, trainingSet)

    # Writes informative and uninformative tweets into separate files
    writeResults()

    return results

if __name__ == "__main__":
    classify()
