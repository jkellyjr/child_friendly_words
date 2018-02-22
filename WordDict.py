from operator import itemgetter
import re
import time


start_time = time.time()

buildFiles = ['google-10000-english-no-swears.txt', 'positive-words.txt']
badWordFiles =['full-list-of-bad-words.txt', 'bad-words.txt', 'negative-words.txt', 'badwords.txt']

badWordFileDir = 'Bad_Words/'
buildWordFileDir = 'Good_Words/'
dictWordFileDir = 'Dict_Words/'


# Adds all words from buildFiles
def buildWordDict():
    totalList = []
    for filename in buildFiles:
        wordList = [re.sub("[^a-zA-Z]","", line).rstrip() for line in open(buildWordFileDir + filename) if len(re.sub("[^a-zA-Z]","", line).rstrip() ) > 2]
        totalList = wordList + totalList

    return set(totalList)


# Removes all words in the files of removeFiles list
def removeWords(dictSet):
    totalList = []
    for filename in badWordFiles:
        wordList = [re.sub("[^a-zA-Z]","", line).rstrip() for line in open(badWordFileDir + filename)]
        totalList = wordList + totalList

    return dictSet.difference(set(totalList))


# Associates the word with its frequency
def buildDict(filename, dictSet):
    totalList = [tuple(line.rstrip().split('\t')) for line in open(dictWordFileDir + filename)]

    tupList = []
    for element in totalList:
        if element[0] in dictSet:
            tup = (element[0], int(element[1]))
            tupList.append(tup)
            totalList.remove(element)

    sorted(tupList, key=itemgetter(1))

    return tupList


# Writes the tuple list to a file
def writeDictToFile(filename, tupList):
    with open(filename, 'w') as f:
        n = 0
        x = 0
        num = len(tupList)
        for s in tupList:
            n += 1
            if n <= (num * .2):
                x= 1
            elif n <= (num * .4):
                x = 2
            elif n <= (num * .6):
                x = 3
            elif n <= (num * .8):
                x = 4
            else:
                x = 5

            f.write(str(x) + "," + s[0] + "," +  str(s[1]) + "\n")



def main():
    buildSet = buildWordDict()
    #print len(buildSet)

    removeSet = removeWords(buildSet)
    #print len(removeSet)

    tupList = buildDict('count_1w.txt', removeSet)

    #print len(tupList)
    writeDictToFile('final-words.txt', tupList)

    #print("--- %s seconds ---" % (time.time() - start_time))

main()
