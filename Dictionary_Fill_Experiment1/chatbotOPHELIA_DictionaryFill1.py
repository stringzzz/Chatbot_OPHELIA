#   chatbotOPHELIA, an AI chatbot with simulated emotions
#   This script is meant to go along with OPHELIA for her to
#   learn more words in her emotion dictionary, though right
#   now it is purely experimental
#   Copyright (C) 2023 stringzzz, Ghostwarez Co.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Chatbot OPHELIA: Original Python Heavenly Emotion Logic Inspecting Automator (Dictionary Filler)
# Dictionary Fill Experiment 1: 05-10-2023

import random
import re
import os
from datetime import datetime

emotionDictionary = {}
messageDict = {"happy": {}, "angry": {}, "sad": {}, "afraid": {}}
nEmotions = ["happy", "angry", "sad", "afraid"]
currentMood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 90, "speed": 150}
pitches = {"happy": 90, "angry": 80, "sad": 80, "afraid": 95}
speeds = {"happy": 150, "angry": 155, "sad": 135, "afraid": 155}
userMessage = " "
chatlog = []
XsentenceLog = []
chatlogFile = {"regular": "OPHELIAchatlog.txt", "extended": "OPHELIAXsentenceLog.txt" }
user_emotions = { "happy": 0, "angry": 0, "sad": 0, "afraid": 0 }

def addToMood():
	#Add the emotional values of the user reply to OPHELIA's emotional values
	for emotion in nEmotions:
		currentMood[emotion] += replyMood[emotion]

	#Change mood, pitch, and speaking speed according to OPHELIA's emotional values
	currentMood["mood"] = getMood(currentMood)
	currentMood["pitch"] = pitches[currentMood["mood"]]
	currentMood["speed"] = speeds[currentMood["mood"]]
	XsentenceLog.append("OPHELIA (Thinking): I feel " + currentMood["mood"])

def getSentenceMood():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	replyMood["mood"] = getMood(replyMood)
	XsentenceLog.append("OPHELIA (Thinking): The sentence seems to be " + replyMood["mood"])

def getMood(moodDictionary):
	#Get the overall mood of either OPHELIA or the user's response
	if moodDictionary["angry"] > moodDictionary["happy"] and moodDictionary["angry"] > moodDictionary["sad"] and moodDictionary["angry"] > moodDictionary["afraid"]:
		return "angry"
	elif moodDictionary["sad"] > moodDictionary["angry"] and moodDictionary["sad"] > moodDictionary["happy"] and moodDictionary["sad"] > moodDictionary["afraid"]:
		return "sad"
	elif moodDictionary["afraid"] > moodDictionary["angry"] and moodDictionary["afraid"] > moodDictionary["sad"] and moodDictionary["afraid"] > moodDictionary["happy"]:
		return "afraid"
	else:
		return "happy"

def chatlogOutput(chatlogFile, chatList):
	chatlog_file = open(chatlogFile, 'a')
	chatlog_file.write("\n\n\n" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
	for line in chatList:
		chatlog_file.write("\n" + line)
	chatlog_file.close()

#Input memory
print("Inputting memory...")

tempValues = []
emotion_dictionary_file = open("emotionDictionary.txt", 'r')
for line in emotion_dictionary_file.readlines():
	if line == "":
		break
	tempValues = (line.strip()).split(' ')
	emotionDictionary[tempValues[0]] = tempValues[1]
emotion_dictionary_file.close()

gotPair = 0
tempValues = []
message_dictionary_file = open("messageDictionary.txt", 'r')
for emotion in nEmotions:
	messagesNo = int(message_dictionary_file.readline())
	for messages in range(0, messagesNo):
		if gotPair < 2:
			tempValues.append(message_dictionary_file.readline().strip())
			gotPair += 1
		if gotPair == 2:
			messageDict[emotion][tempValues[0]] = tempValues[1]
			tempValues.clear()
			gotPair = 0
message_dictionary_file.close()

print("Memory input complete!\n")

text_file_name = input("Enter the name of the text file to read: ")
print(text_file_name)

try:
	text_file = open(text_file_name, 'r')
	print("OPHELIA: Reading the text file " + text_file_name + "...")
	
	text = text_file.read()
	text = re.sub(r"(\n+)", " ", text)
	text = text.lower()
	text = re.sub(r"( {2, })", " ", text)
	text = re.sub(r"(\.{2, })", ".", text)
	text = re.sub(r"(\?{2, })", "?", text)
	text = re.sub(r"(\!{2, })", "!", text)
	text = re.sub(r"(,{2, })", ",", text)
	text = re.sub(r"(\")", "", text)
	text = re.sub(r"(\. |\? |\! )", "%%$$%%", text)
	text_sentences = text.split("%%$$%%")
	
	sentences = 0;
	for sentence in text_sentences:
		if sentence == '':
			continue
			
		sentences += 1
		print("Reading sentence " + str(sentences) + "/" + str(len(text_sentences) - 1))
	
		#Filter out punctuation from sentence and split to list of words
		sentenceWords = (re.sub(r"(\.|\?|\!|,)", "", sentence)).split(" ")

		#Detect emotion words, get reply mood
		unknownWords = []
		replyMood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}

		wordEmotions = ""
		for word in sentenceWords:
			try:
				if emotionDictionary[word] != "neutral":
					replyMood[emotionDictionary[word]] += 1
					user_emotions[emotionDictionary[word]] += 1
					wordEmotions = wordEmotions + emotionDictionary[word] + " "
				else: 
					wordEmotions = wordEmotions + " neutral "
			except(KeyError):
				unknownWords.append(word)
				wordEmotions = wordEmotions + " unknown "
		XsentenceLog.append("\nWord emotions in previous sentence: " + wordEmotions)
			
		getSentenceMood()

		#Mark unknown words in the emotion dictionary according to the overall mood of the sentence
		if len(unknownWords) > 0:
			XsentenceLog.append("OPHELIA (Thinking): Unknown words detected: " + str(unknownWords))
			for word in unknownWords:
				emotionDictionary[word] = replyMood["mood"] 
			XsentenceLog.append("OPHELIA (Thinking): Learned unknown words as '" + replyMood["mood"] + "' words.") 
	
except(FileNotFoundError):
	print("Invalid file name")
	quit()
	

#Output memory
print("Reading of text file complete.")
print("\nOutputting memory...")

dictionaryCounts = { "neutral": 0, "happy": 0, "angry": 0, "sad": 0, "afraid": 0 }
nEmotions2 = ["neutral", "happy", "angry", "sad", "afraid"]
emotion_dictionary_file = open("emotionDictionary.txt", 'w')
for key in emotionDictionary.keys():
	dictionaryCounts[emotionDictionary[key]] += 1
	emotion_dictionary_file.write(key + " " + emotionDictionary[key] + "\n")
emotion_dictionary_file.close()

chatlogOutput(chatlogFile["extended"], XsentenceLog)

data_file = open("OPHELIAdata.txt", 'w')
data_file.write("stringzzz\nWords in emotion dictionary: " + str(len(emotionDictionary)) + "\n")
for emotion in nEmotions:
	data_file.write("Number of " + emotion + " message/response pairs: " + str(len(messageDict[emotion])) + "\n")
for emotion in nEmotions2:
	data_file.write(emotion + " words in dictionary: " + str(dictionaryCounts[emotion]) + "\n")
data_file.close()
#Note, number of responses not output, but it will be added properly the next time you run OPHELIA and '//exit'

print("Memory output complete.\n")
