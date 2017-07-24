import csv
import os
from PIL import Image
from os import path
import numpy as np
from nltk.corpus import stopwords
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import random



importDates = ['Jul']
inputPath = "C:/Users/Summer16/Documents/BCMAPFEAT/data_recent.csv"
imagePath = 'C:/Users/Summer16/Documents/BC.png'
stopWords = stopwords.words('english')


def extractTweets(inputPath): 
    source = open(inputPath, encoding = "utf-8")
    reader = csv.reader(source)
    data = list(reader)
    extract = []
    
    for tweet in data:
        signal = False 
        for date in importDates: 
            if date in tweet[1]:
                signal = True
        if signal == True:
            extract.append(tweet[0])
        else:
            pass
    
    massiveString = ''
    
    for element in extract:
        massiveString += element + ' '
    
    massiveString.strip()
    for element in stopWords:
        massiveString.replace(element, '')
    massiveString.replace('RT ', '')
    massiveString.replace('rt ', '')
    massiveString.replace('one', '')
    massiveString.replace(' o ', '')
    massiveString.replace('  ', ' ')
    
    massiveList = massiveString.split(' ')
    newMassiveList = []
    forbid = ['fire', 'wildfire', 'rt', 'o', 'one', 'see', 'sure', 'rock', 'lit', 'fires', 'now', '&', 'new', 'via', 'can', 'need', 'order']
    for element in massiveList:
        element = element.lower()
        if 'http' not in element and 'amp' not in element and element not in forbid: 
            newMassiveList.append(element)
    
    newMassiveString = ''
    
    print(len(newMassiveList))
    for element in newMassiveList:
        newMassiveString += element + ' '
    
    newMassiveString.strip()
    
    return newMassiveString

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def generateWordCloud(imagePath, inputPath): 
    mask = np.array(Image.open(imagePath))
    text = extractTweets(inputPath)
    stopwords = set(STOPWORDS)
    
    wc = WordCloud(width = 1500, height = 2000).generate(text)
    plt.title("BC Wildfire / Intact")
    default_colors = wc.to_array()
    plt.imshow(default_colors,
               interpolation="bilinear")
    wc.to_file("BCfire.png")

if __name__ == "__main__":
    generateWordCloud(imagePath, inputPath)
    '''
    l = extractTweets(inputPath)
    
    if not os.path.exists('C:/Users/Summer16/My Documents/'):
        os.makedirs('C:/Users/Summer16/My Documents/')
    
    if not os.path.exists('C:/Users/Summer16/My Documents/wordfile.txt'):
        f = open('C:/Users/Summer16/My Documents/wordfile.txt', "w")
        f.close()
    
    with open('C:/Users/Summer16/My Documents/wordfile.txt', 'w', encoding="utf-8") as textFile:
        textFile.write(l)
    '''