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

# get sign of a number
def sign(num):
    sig = num and (1, -1)[num < 0]
    return int(sig)

# exit method
def CheckBye(str):
    if str.lower() == "bye"\
            or str.lower() == "quit"\
            or str.lower() == "exit"\
            or str.lower() == "q":
        return True
    else:
        return False

# print char by char
def mechPrint(str):
    for char in str:
        time.sleep(0.05)
        print(char, end='')

# text to speech
def speak(str):
    t2sEngine.say(str)
    t2sEngine.runAndWait()

# threading for mech-like output
def mechOutput(str):
    task1 = threading.Thread(mechPrint(str + "\n"))
    task2 = threading.Thread(speak(str))
    task1.start()
    task2.start()
    task1.join()
    task2.join()

# open file
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

# q&a pool
question = ["So how's your day, ",
            "How are you today, ",
            "How are you doing, ",
            "How's it going, ",
            "How's everything, "
            ]
answer = [["That sucks", "Bummer"], ["Hmm..", "I see"], ["Great", "Cool"]]

# text 2 speech init
t2sEngine = pyttsx.init()

# main loop
while 1:
    # choose between basic version and google sentiment analysis version
    while 1:
        mode = raw_input("Please choose chat bot version: 1-basic, 2-sentiment. Type 1 or 2.\n")
        if mode == "1" or mode == "2":
            break
        print("please type 1 or 2.\n")

    mechOutput("Hi there, what's your name?")
    name = raw_input()
    if CheckBye(name):
        break

    # randomize the question
    questionIndex = random.randint(1, 100) % 4
    mechOutput(question[questionIndex] + name + "?")
    howIsTheDay = raw_input()
    if CheckBye(howIsTheDay):
        break

    # basic info statistics
    lettersCnt = len(howIsTheDay)
    howIsTheDay = re.sub('[^0-9a-zA-Z]+', ' ', howIsTheDay).lower()

    words = howIsTheDay.split()
    wordsCnt = len(words)


    # analysis
    if mode == "1":
        # basic version

        # use AC Automation to find keywords in the sentence efficiently
        positiveAnalysis = positive_acAutomation.matchAll(howIsTheDay)
        negativeAnalysis = negative_acAutomation.matchAll(howIsTheDay)

        # deal with "not bad" or "not good" scenario
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

        # if the # of positive words exceeds that of negative words, consider as positive response
        sense = positiveCnt - negativeCnt
    else:
        # google online sentiment analysis version
        sense = get_sentiment(howIsTheDay)

    # randomize the answer
    answerIndex = random.randint(1, 100) % 2

    # print basic info
    print("(You entered " + str(lettersCnt) + " letters and " + str(wordsCnt) + " words.)\n")

    # print ans
    # the answer pool is set up in the order of negative, neutral and positive.
    # the sign of sentiment plus 1 will be the index of answer pool
    mechOutput(answer[sign(sense) + 1][answerIndex])

    mechPrint("\n-------INITIALIZING-------\n")

print("Bye\n")
