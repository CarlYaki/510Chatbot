# python2.7
# pip install -U ACAutomation

import re
from get_sentiment import get_sentiment
from ACAutomation import ACAutomation

def CheckBye(str):
    if str == "Bye":
        return True
    else:
        return False


with open("positive-words.txt") as f:
    lines = f.readlines()
positive_words = [line.strip() for line in lines]
with open("negative-words.txt") as f:
    lines = f.readlines()
negative_words = [line.strip() for line in lines]

positive_acAutomation = ACAutomation()
for positive_word in positive_words:
    positive_acAutomation.insert(positive_word)
positive_acAutomation.build()

negative_acAutomation = ACAutomation()
for negative_word in negative_words:
    negative_acAutomation.insert(negative_word)
negative_acAutomation.build()

while 1:
    name = raw_input("Hi there, what's your name?\n")
    if CheckBye(name):
        break
    howIsTheDay = raw_input("So how's your day, " + name + "?\n")
    if CheckBye(howIsTheDay):
        break

# basic info

    lettersCnt = len(howIsTheDay)
    howIsTheDay = re.sub('[^0-9a-zA-Z]+', ' ', howIsTheDay).lower()

    words = howIsTheDay.split()
    wordsCnt = len(words)

    print("You entered " + str(lettersCnt) + " letters and " + str(wordsCnt) + " words.")

# analysis

    positiveAnalysis = positive_acAutomation.matchAll(howIsTheDay)
    negativeAnalysis = negative_acAutomation.matchAll(howIsTheDay)

    reversedPositive = 0
    reversedNegative = 0

    for i in range(wordsCnt-1):
        if words[i] == "not":
            tempPositive = positive_acAutomation.matchAll(words[i+1])
            tempNegative = negative_acAutomation.matchAll(words[i+1])
            if len(tempPositive) > len(tempNegative):
                reversedNegative += 1
            elif len(tempPositive) < len(tempNegative):
                reversedPositive += 1
            else:
                continue

    deviation = reversedPositive - reversedNegative

    positiveCnt = len(positiveAnalysis) + deviation
    negativeCnt = len(negativeAnalysis) - deviation

    if positiveCnt > negativeCnt:
        print("positive\n")
    elif positiveCnt < negativeCnt:
        print("negative\n")
    else:
        print("neutral\n")

    print(get_sentiment(howIsTheDay))

print("Bye")
