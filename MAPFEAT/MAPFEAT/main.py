import classifyTweets
import extractFeatures
import finalizeFeatures
import processTweets
import searchAppStore
import topicModeling
import validateResults

import os
import shutil


OUTPUT_PATH = 'output'

if __name__ == "__main__":
    wordsPerTopic = input("\nEnter the number of words per topic: ")
    numTopics = input("Enter the number of topics desired: ")
    appLimit = input("Enter the maximum number of apps returned by each app store search query: ")
    sharedBetween = input("Enter the minimum number of apps per query that should share each feature: ")

    print '\n-------------------------------------------------------------\n'

    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    processTweets.process()
    classifyTweets.classify()

    topicModeling.extractTopics(wordsPerTopic, numTopics)
    searchAppStore.search(appLimit)

    extractFeatures.extract()
    finalizeFeatures.finalize(sharedBetween)

    print '\n-------------------------------------------------------------\n'

    #validateResults.validate()
