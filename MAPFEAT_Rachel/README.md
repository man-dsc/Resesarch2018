# MAPFEAT

The turnkey solution for MAPFEAT, a method designed for extracting software features from tweets through a combination of machine learning techniques, app store mining, and crowdsourcing.<sup>[1]</sup> Developed as part of a Software Engineering research project course at the University of Calgary.

<br />
## Setup

To set up:
```
$ pip install pattern nltk scipy sklearn stop_words requests gensim matplotlib
```

To run:
```
$ python src/main.py
```

<br />
## Overview

This tool is a Python implementaton of MAPFEAT, a method that introduces software features to emergency apps by automating the mining of needs from general purpose tweets and their translation into real app features. The tool has been evaluated by a case study of the 2016 wildfire in Fort McMurray, Canada, in which it identified a significant amount of new and valuable functionality.


<br />
## Process

<br />
![Alt text](mappingProcess.jpg?raw=true)

<br />
__Input:__  
data/trainingSet.csv  
data/dataSet.csv

The training set is a manually classified CSV with a list of tweets in the first column and a "Y" or "N" in the second column to indicate whether the tweet is informative or not. The data set is a CSV with a list of tweets. 

Sample input files have been included in the project.


<br />
### 1. process.py

Processes the training set and the data set.

* Lemmatizes
* Removes duplicate tweets, stop words, urls, hashtags, special characters, and digits

__Output:__  
output/processedTweets/processedDataSet.csv  
output/processedTweets/processedTrainingSet.csv

<br />
### 2. classify.py

Finds the relevant tweets by using the Naive Bayes classifier to categorize them as either 'informative' or uninformative' (Step 1).

* Evaluates the performance of the classifier by performing 10-fold cross validation on the manually classified training set
* Displays the accuracy, precision, recall, F1, and stdev
* Using the training set, the classifier categorizes the tweets in the data set

__Output:__  
output/classifiedTweets/informative.csv  
output/classifiedTweets/non_informative.csv

<br />
### 3. topicModeling.py

Uses LDA topic modeling (Step 2) to extract common sets of words from the tweets that were classified as 'informative' from the previous step.

The number of words per topic and the number of topics are both configurable.

__Ouput:__  
output/topics/topics.csv

<br />
### 4. searchAppStore.py

Searches the Apple app store to find apps matching the topics discovered in the previous step.

* Generates search queries using the combination of words in each topic (Step 3)
* Sends queries with length > 2 to the app store (Step 4)
* Stores the descriptions of apps that are retrieved (Step 5)

The limit of how many apps can be retrieved per query is configurable.

__Sample Output:__  
 |-- output  
 |      |-- apps  
 |      |      |-- alberta+appeal+charge+additional+evacuee+fundraising+grocery  
 |      |      |      |-- alberta+grocery.csv  
 |      |      |      |-- appeal+fundraising.csv  
 |      |      |      |-- fundraising+grocery.csv  
 |      |      |-- area+mile+burning+minister+recover+central+larivee  
 |      |      |      |-- area+central.csv  
 |      |      |      |-- area+mile.csv  
 ...  
 
<br />
### 5. extractFeatures.py
 
Prepares the app descriptions for processing and then mines software features from them (Step 6).

* Uses NLTK's N-gram CollocationFinder package to extract 'featurelets'
* Applies greedy hierarchical clustering to aggregate similar featurelets, resulting in groupings of two or three words

__Sample Ouput:__  
 |-- output  
 |      |-- air+help+donate  
 |      |-- evacuee+food+donation    
 |      |-- resident+need+help  
 ...  
 
<br />
### 6. finalizeFeatures.py

Narrows down the features by selecting the ones that are mutually 'shared' between at least a certain number of apps originating from the same search query (Step 7). For features to be considered as 'shared' between apps, they must have a cosine similarity measure greater than 60\%. Lastly, each feature is linked back to its original tweet topic (Step 8).

The number of apps that a feature should be 'shared' by is configurable.

__Output:__  
output/finalizedFeatures.csv  

<br />
### 7. validateFeatures.py


Validates the accuracy of the results using crowdsourcing to assess the semantic relationship between each topic and its resulting features (Step 9). 

* Uses the Amazon Mechanical Turk API to post a survey which contains the extracted features along with their corresponding tweet topic
* Asks workers to select all features related to the topic
* Waits for results and then parses the survey answers to find the 'validated' features. These features make up the final proposed feature set

The number of workers required to answer the survey is configurable, and so is the number of votes required for a feature to be considered 'validated'.

__Output:__  
output/validatedFeatures.csv  

<br />
## References

[1]		Nayebi, M.; Marbouti, M; Quapp, R; Maurer, F and Ruhe, G. " Crowdsourced Exploration of Mobile App Features: A Case Study of the Fort McMurray Wildfire " In Proceedings of the 39th International Conference on Software Engineering (ICSE), pp. to appear. ACM, 2017
