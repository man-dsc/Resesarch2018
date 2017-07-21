import csv
#import StringIO
import time
import semanticSimilarity

''' Producing a Stream of Tweets '''

def readInput(inputPath):
    source = open(inputPath, 'rU')
    reader = csv.reader(source)
    data = list(reader)
    del(data[0])
    refinedData = []
    
    for element in data:
        if len(element) == 4 and element[0].strip() != '' and element[1].strip() != '' \
              and element[2].strip() != '' and element[3].strip() != '': 
                  refinedData.append(element)
          
    return(refinedData)

def sortData(inputFile):
    sortedList = []
    
    for element in inputFile:
        datestamp = element[1]
        if datestamp[-5] == ' ':
            timestamp = int(datestamp[2]) * 86400 + int(datestamp[-4]) * 3600 \
                           + int(datestamp[-2] + datestamp[-1]) * 60
        else:
            timestamp = int(datestamp[2]) * 86400 + int(datestamp[-5] + datestamp[-4]) * 3600 \
                           + int(datestamp[-2] + datestamp[-1]) * 60
        sortedList.append([timestamp, element])
    
    sortedList.sort(key = lambda x:x[0])
    return sortedList

def twitterStream(sortedData):
    print('####################################################################################################')
    print('#################### Starting Tweet Simulation: 1 second = 50 minutes real time ####################')
    print('####################################################################################################')
    print('\n')
    
    
    for i in range(len(sortedData) - 1):
        if semanticSimilarity.similarity('#ymmfire is there any ooen gas stations in fort mckay #ymmfires', sortedData[i][1][0], False) > 0.3:
            print('User' + ': ' + sortedData[i][1][-1])
            print('Tweet' + ': ' + sortedData[i][1][0])
            print('Time' + ': ' + sortedData[i][1][1])
            print(semanticSimilarity.similarity('#ymmfire is there any ooen gas stations in fort mckay #ymmfires', sortedData[i][1][0], False))
            print('\n')

        for j in range((sortedData[i + 1][0] - sortedData[i][0]) / 1200):
            time.sleep(1)
    
    print('User' + ': ' + sortedData[i][-1][-1])
    print('Tweet' + ': ' + sortedData[i][-1][0])
    print('Time' + ': ' + sortedData[i][-1][1])


if __name__ == "__main__":
    filepath = 'C:/Users/Summer16/My Documents/UpdatedFortMacDataSet.csv'
    rawData = readInput(filepath)
    sortedData = sortData(rawData)
    twitterStream(sortedData)