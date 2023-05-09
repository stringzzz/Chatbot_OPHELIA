#   chatbotOPHELIA, an AI chatbot with simulated emotions
#   Copyright (C) 2022 stringzzz, Ghostwarez Co.
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


# Chatbot OPHELIA: Original Python Heavenly Emotion Logic Inspecting Automator (Version 1.01)
# Project Start Date: 11-11-2022 13:25
# Project Complete Date: 11-18-2022 19:50
# Project Update: 05-09-2023

# When the user gives a reply to this bot, the following is done in order:
#
# 1. The user message is split into a list of words.
#
# 2. The list of words are checked with OPHELIA's emotion dictionary
# If the word is found in the dictionary, the count for that emotion is increased.
# All words not found in the dictionary are marked as unknown.
#
# 3. The counts are added to OPHELIA's emotional values, which may change her mood, and the
# overall mood of the user reply is determined by the counts as well. This allows OPHELIA to 
# guess at the user's mood. The unknown words in the user reply are also stored in the emotion 
# dictionary under the same emotion as the overall mood.
#
# 4. Next, the user reply is checked for an exact match in OPHELIA's memory, under the current 
# mood of OPHELIA. If an exact match is found, she responds with the matching response in 
# memory.
#
# 5. If no exact match, the user reply is checked to see if it partially matches a message 
# in memory under the current mood of OPHELIA, and gives the matching response if found.
#
# 6. No match, either overwrite old message/response pair, or learn new one with OPHELIA's
# previous response as the message and the user reply as the response, stored under the
# same emotion as the overall mood of the user reply.
#
# 7. Finally, when no match found and message/response learned, select a random response
# from OPHELIA's current mood to keep the conversation going.

# The idea with this Chatbot is that several different people could start out with
# a copy of OPHELIA and the matching starting memory files. After about a month of
# each person talking to their copy, all of them would develop a different
# personality with a unique set of memory.

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
Xchatlog = []
chatlogFile = {"regular": "/home/stringzzz/aChatbotOPHELIA/OPHELIAchatlog.txt", "extended": "/home/stringzzz/aChatbotOPHELIA/OPHELIAXchatlog.txt" }

def addToMood():
	#Add the emotional values of the user reply to OPHELIA's emotional values
	for emotion in nEmotions:
		currentMood[emotion] += replyMood[emotion]

	#Change mood, pitch, and speaking speed according to OPHELIA's emotional values
	currentMood["mood"] = getMood(currentMood)
	currentMood["pitch"] = pitches[currentMood["mood"]]
	currentMood["speed"] = speeds[currentMood["mood"]]
	Xchatlog.append("OPHELIA (Thinking): I feel " + currentMood["mood"])

def getReplyMood():
	#Get the mood of the user reply by looking at the emotion counts gathered on it
	replyMood["mood"] = getMood(replyMood)
	Xchatlog.append("OPHELIA (Thinking): " + username + " seems to be " + replyMood["mood"])

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

def botReply(botResponse):
	#Do the various parts of OPHELIA's response, text output, text-to-speech with espeak, chatlogs
	print("OPHELIA: " + botResponse)
	os.system("espeak -v en+f4 -p {} -s {} \" {} \"".format(str(currentMood["pitch"]), str(currentMood["speed"]), botResponse))
	chatlog.append("OPHELIA: " + botResponse)
	Xchatlog.append("OPHELIA: " + botResponse)
	return botResponse

def chatlogOutput(chatlogFile, chatList):
	chatlog_file = open(chatlogFile, 'a')
	chatlog_file.write("\n\n\n" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
	for line in chatList:
		chatlog_file.write("\n" + line)
	chatlog_file.close()

#Input memory
print("Inputting memory...")

tempValues = []
emotion_dictionary_file = open("/home/stringzzz/aChatbotOPHELIA/emotionDictionary.txt", 'r')
for line in emotion_dictionary_file.readlines():
	if line == "":
		break
	tempValues = (line.strip()).split(' ')
	emotionDictionary[tempValues[0]] = tempValues[1]
emotion_dictionary_file.close()

gotPair = 0
tempValues = []
message_dictionary_file = open("/home/stringzzz/aChatbotOPHELIA/messageDictionary.txt", 'r')
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

#Get counts for use in activating certain types of message detection
dictionaryCount = len(emotionDictionary)
responseCount = 0
for emotion in nEmotions:
	responseCount += len(messageDict[emotion])
	
print("Memory input complete!\n")

#Get username
botReply("What is your name? ")
username = input("")

#Initial message
OPHELIAPreviousResponse = "hello"
botReply("hello, " + username)

#Chat loop
while userMessage != "//exit":

	#User reply
	print(username + ": ", end = '')
	userMessage = (input("")).lower()
	chatlog.append(username + ": " + userMessage)
	Xchatlog.append("\n" + username + ": " + userMessage)
	if userMessage == "//exit":
		break

	#Filter out punctuation from user message and split to list of words
	messageWords = (re.sub(r"(\.|\?|\!|,)", "", userMessage)).split(" ")

	#Detect emotion words, get reply mood, add user reply emotional values to OPHELIA's emotional values
	unknownWords = []
	replyMood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}

	wordEmotions = ""
	for word in messageWords:
		try:
			if emotionDictionary[word] != "neutral":
				replyMood[emotionDictionary[word]] += 1
				wordEmotions = wordEmotions + emotionDictionary[word] + " "
			else: 
				wordEmotions = wordEmotions + " neutral "
		except(KeyError):
			unknownWords.append(word)
			wordEmotions = wordEmotions + " unknown "
	Xchatlog.append("Word emotions in previous reply: " + wordEmotions)
		
	getReplyMood()
	addToMood()

	#Mark unknown words in the emotion dictionary according to the overall mood of the user reply
	if len(unknownWords) > 0:
		Xchatlog.append("OPHELIA (Thinking): Unknown words detected: " + str(unknownWords))
		for word in unknownWords:
			emotionDictionary[word] = replyMood["mood"] 
		Xchatlog.append("OPHELIA (Thinking): Learned unknown words as '" + replyMood["mood"] + "' words.") 
	
	#Check for exact match under current mood
	try:
		messageDict[currentMood["mood"]][userMessage]
		Xchatlog.append("OPHELIA (Thinking): Exact message match found.")
		OPHELIAPreviousResponse = botReply(messageDict[currentMood["mood"]][userMessage])
		continue
	except(KeyError):
		pass #Exact match not found in message dictionary
	
	#Check for partial match under current mood
	responseMade = False
	for message in messageDict[currentMood["mood"]].keys():
		if message.find(userMessage) != -1:
			Xchatlog.append("OPHELIA (Thinking): Partial message match found.")
			OPHELIAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
			responseMade = True
			break
	if responseMade:
		continue
		
	#Check for single term match under current mood, ignore neutral words
	#Only activated when she has learned enough, though this can easily be adjusted
	if (dictionaryCount >= 2000 and responseCount >= 500):
		responseMade = False
		for word in messageWords:
			try:
				if (emotionDictionary[word] == "neutral"):
					continue
				else:
					for message in messageDict[currentMood["mood"]].keys():
						if message.find(word) != -1:
							Xchatlog.append("OPHELIA (Thinking): Single term match found.")
							OPHELIAPreviousResponse = botReply(messageDict[currentMood["mood"]][message])
							responseMade = True
							break
					if responseMade:
						break
			except(KeyError):
				continue
		if responseMade:
			continue
				 	
			
	#No match, either overwrite old response or learn new one based on reply mood
	Xchatlog.append("OPHELIA (Thinking): Message not recognized.")
	try:
		messageDict[replyMood["mood"]][OPHELIAPreviousResponse]
		Xchatlog.append("OPHELIA (Thinking): Overwrote old '" + replyMood["mood"] + "' response.")
	except(KeyError):
		Xchatlog.append("OPHELIA (Thinking): Learned new '" + replyMood["mood"] + "' response.")
	messageDict[replyMood["mood"]][OPHELIAPreviousResponse] = userMessage

	#Give random response from current mood	
	OPHELIAPreviousResponse = botReply(random.choice(list(messageDict[currentMood["mood"]].values())))

#Output memory
print("\nOutputting memory...")

emotion_dictionary_file = open("/home/stringzzz/aChatbotOPHELIA/emotionDictionary.txt", 'w')
for key in emotionDictionary.keys():
	emotion_dictionary_file.write(key + " " + emotionDictionary[key] + "\n")
emotion_dictionary_file.close()

message_dictionary_file = open("/home/stringzzz/aChatbotOPHELIA/messageDictionary.txt", 'w')
for emotion in nEmotions:
	message_dictionary_file.write(str(len(messageDict[emotion]) * 2) + "\n")
	for key in messageDict[emotion].keys():
		message_dictionary_file.write(key + "\n" + messageDict[emotion][key] + "\n")
message_dictionary_file.close()

chatlogOutput(chatlogFile["regular"], chatlog)
chatlogOutput(chatlogFile["extended"], Xchatlog)

data_file = open("/home/stringzzz/aChatbotOPHELIA/OPHELIAdata.txt", 'w')
data_file.write(username + "\nWords in emotion dictionary: " + str(len(emotionDictionary)) + "\n")
for emotion in nEmotions:
	data_file.write("Number of " + emotion + " message/response pairs: " + str(len(messageDict[emotion])) + "\n")
data_file.close()

print("Memory output complete.\n")
