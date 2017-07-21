# -*- coding: utf-8 -*-
#
# Uses the iTunes API to search the Apple App Store for apps matching tweet queries
#
# Algorithm:
# - Take a row from the csv
# - Take the powerset of the columns
# - For each query of length >=2 of the powerset, search the app store
# - If there are results, write information for the top X results to a csv
#
# Sample output:
# |-- output
# |   |-- apps
# |   |   |-- alberta+appeal+charge+additional+evacuee+fundraising+grocery
# |   |   |   |-- alberta+grocery.csv
# |   |   |   |-- appeal+fundraising.csv
# |   |   |   |-- fundraising+grocery.csv
# |   |   |-- area+mile+burning+minister+recover+central+larivee
# |   |   |   |-- area+central.csv
# |   |   |   |-- area+mile.csv
# |   |   |   |-- mile+burning.csv
# |   |   |   |-- mile+central.csv
# ...
#
# * Where each directory is named after the tweet topic and each csv is named after the search query

import csv
import json
import os
import requests
import shutil

INPUT_FILENAME = 'topics.csv'
INPUT_PATH = 'output/topics'
OUTPUT_PATH = 'output/apps'


def searchAPI(row, appLimit):
    topic = "+".join(row)

    try:
        os.makedirs(OUTPUT_PATH + '/' + topic)
    except:
        return

    headers = {
        'User-Agent':'iTunes/10.3.1 (Macintosh; Intel Mac OS X 10.6.8) AppleWebKit/533.21.1',
        'Accept-Encoding' : 'identity'
    }

    # Get every combination with length >= 2 of the words in the topic
    sQuery = powerset(row)

    # Send each query to the app store
    for query in sQuery:
        if len(query) >= 2:
            sTerm = '+'.join(query)
            endPoint = 'https://itunes.apple.com/search?term={}&media=software&retries=true&limit={}'.format(sTerm, appLimit)
            result = requests.get(endPoint, headers=headers)
            print(result)
            createCSV(result, topic, "+".join(query))


def createCSV(appInfo, topic, query):
    try:
        apps = appInfo.json()['results']
    except ValueError:
        return
    if apps:
        filename = '{}/{}/{}.csv'.format(OUTPUT_PATH, topic, query)
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Package Name', 'Description', 'Rating', 'Rating Count'])
            for pair in apps:
                name = pair.get('trackName').replace('&nbsp;', '').encode("utf-8")
                bundleId = pair.get('bundleId').replace('&nbsp;', '').encode("utf-8")
                desc = pair.get('description').replace('&nbsp;', '').encode("utf-8")
                rating = pair.get('averageUserRating')
                ratingCount = pair.get('userRatingCount')

                writer.writerow([name, bundleId, desc, rating, ratingCount])


def powerset(s):
    r = [[]]
    for e in s:
        r += [x+[e] for x in r]
    return r


def search(appLimit):
    print 'Searching the app store...\n'

    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    # Read in topics
    with open('{}/{}'.format(INPUT_PATH, INPUT_FILENAME), 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            del row[0]
            if not any(row):
                break
            row = filter(None, row)
            topic = []
            for item in row:
                topic.append(item.split('_')[1].replace("'",''))
            searchAPI(topic, appLimit)


if __name__ == '__main__':
    appLimit = input("\nEnter the maximum number of apps returned by each app store search query: ")

    search(appLimit)
