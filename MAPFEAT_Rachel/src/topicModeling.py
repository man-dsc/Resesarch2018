# LDA topic modeling on tweets
#
# The number of topics and the number of words per topic can be configured based on the
# quality and quantity of the results
#
# Based off of Tweet_topic_modeling.py by SEDS

import csv
import gensim
import hashlib
import numpy
import os
import pylab
import re
import scipy
import shutil
import string

from collections import defaultdict
from gensim import corpora, models, similarities
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

INPUT_PATH = 'output/classifiedTweets'
INPUT_FILE = 'informative.csv'

OUTPUT_PATH = 'output/topics'
OUTPUT_FILE = 'topics.csv'


def listTweets():
	with open('{}/{}'.format(INPUT_PATH, INPUT_FILE), 'r') as r:
		reader = csv.reader(r)
		tweets = []
		for row in reader:
			tweet = row[0]
			tweets.append(tweet.split())
	return tweets


def extractTopics(wordsPerTopic, numTopics):
	print 'Topic modeling...\n'

	if os.path.exists(OUTPUT_PATH):
		shutil.rmtree(OUTPUT_PATH)
	os.makedirs(OUTPUT_PATH)

	tweets = listTweets()

	# Construct a document-term matrix
	dictionary = corpora.Dictionary(tweets)

	# Convert dictionary to a bag of words
	corpus = [dictionary.doc2bow(tweet) for tweet in tweets]

	# Apply the LDA model
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=numTopics, id2word=dictionary, passes=100)

	# Create a table for training corpus
	table = []
	for i in range(len(ldamodel.print_topics(num_topics=numTopics, num_words=wordsPerTopic))):
	    element = [0,0] 
	    str(ldamodel.print_topics(num_topics=numTopics, num_words=wordsPerTopic)[i][1])
	    element[0] = i + 1
	    element[1] = ldamodel.print_topics(num_topics=numTopics, num_words=wordsPerTopic)[i][1]
	    table.append(element)

	# Write topics to file
	with open('{}/{}'.format(OUTPUT_PATH, OUTPUT_FILE), 'wb') as w:
		writer = csv.writer(w)
		for index, row in enumerate(table):
			row[1] = row[1].replace(' ', '')
			row[1] = row[1].replace('_', '')
			row[1] = row[1].replace('*', '_')
			row[1] = row[1].replace('"', "'")
			keywords = row[1].split('+')
			w.write('"' + str(index) + '"')
			for keyword in keywords:
				if keyword:
					w.write(',"' + keyword + '"')
			w.write('\n')
		w.close()


if __name__ == '__main__':
    wordsPerTopic = input("\nEnter the number of words per topic: ")
    numTopics = input("Enter the number of topics desired: ")

    extractTopics(wordsPerTopic, numTopics)
