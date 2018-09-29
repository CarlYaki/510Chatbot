# Win10 64bit
# python2.7
# pip install ACAutomation pyttsx pywin32
# (ACAutomation needs python c++ support)

# commented out the print part in "get_sentiment.py" and changed the output to score

from __future__ import print_function
import re
import random
import time
import pyttsx
import threading
from ACAutomation import ACAutomation
from get_sentiment import get_sentiment

def sign(num):
    sig = num and (1, -1)[num < 0]
    return int(sig)

def CheckBye(str):
    if str.lower() == "bye"\
            or str.lower() == "quit"\
            or str.lower() == "exit"\
            or str.lower() == "q":
        return True
    else:
        return False

def mechPrint(str):
    for char in str:
        time.sleep(0.05)
        print(char, end='')

def speak(str):
    t2sEngine.say(str)
    t2sEngine.runAndWait()

def mechOutput(str):
    task1 = threading.Thread(mechPrint(str + "\n"))
    task2 = threading.Thread(speak(str))
    task1.start()
    task2.start()
    task1.join()
    task2.join()

with open("positive-words.txt") as f:
    lines = f.readlines()
positive_words = [line.strip() for line in lines]
with open("negative-words.txt") as f:
    lines = f.readlines()
negative_words = [line.strip() for line in lines]

# building ACAutomation trie for efficient string compare
positive_acAutomation = ACAutomation()
for positive_word in positive_words:
    positive_acAutomation.insert(positive_word)
positive_acAutomation.build()

negative_acAutomation = ACAutomation()
for negative_word in negative_words:
    negative_acAutomation.insert(negative_word)
negative_acAutomation.build()

question = ["So how's your day, ",
            "How are you today, ",
            "How are you doing, ",
            "How's it going, ",
            "How's everything, "
            ]
answer = [["That sucks", "Bummer"], ["Hmm..", "I see"], ["Great", "Cool"]]

t2sEngine = pyttsx.init()


while 1:
    while 1:
        mode = raw_input("Please choose chat bot version: 1-basic, 2-sentiment. Type 1 or 2.\n")
        if mode == "1" or mode == "2":
            break
        print("please type 1 or 2.\n")

    mechOutput("Hi there, what's your name?")
    name = raw_input()
    if CheckBye(name):
        break

    questionIndex = random.randint(1, 100) % 4
    mechOutput(question[questionIndex] + name + "?")
    howIsTheDay = raw_input()
    if CheckBye(howIsTheDay):
        break

    # basic info

    lettersCnt = len(howIsTheDay)
    howIsTheDay = re.sub('[^0-9a-zA-Z]+', ' ', howIsTheDay).lower()

    words = howIsTheDay.split()
    wordsCnt = len(words)


# analysis

    if mode == "1":
        # basic
        positiveAnalysis = positive_acAutomation.matchAll(howIsTheDay)
        negativeAnalysis = negative_acAutomation.matchAll(howIsTheDay)

        reversedPositive = 0
        reversedNegative = 0

        # deal with "not bad" scenario
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

        # if the # of positive words exceeds that of negative words, consider as positive response
        sense = positiveCnt - negativeCnt
    else:
        sense = get_sentiment(howIsTheDay)
    answerIndex = random.randint(1, 100) % 2

    print("(You entered " + str(lettersCnt) + " letters and " + str(wordsCnt) + " words.)\n")

    mechPrint(answer[sign(sense) + 1][answerIndex] + "\n")
    t2sEngine.say(answer[sign(sense) + 1][answerIndex])
    t2sEngine.runAndWait()

    mechPrint("\n-------INITIALIZING-------\n")


print("Bye")
