#!/usr/bin/env python
from difflib import SequenceMatcher
import discord
import numpy as np
#import urllib2
from six.moves import urllib 
import sys
import os
#from HTMLParser import HTMLParser
from html.parser import HTMLParser

keepOrder = False
separate = False

# All Maps by Game Type
gameTypes = ["Solo Showdown","Duo Showdown","Gem Grab","Heist","Bounty","Brawl Ball","Siege","Robo Rumble","Big Game","Boss Fight"]
maps = [[],[],[],[],[],[],[],[],[],[]]

# Game Type Sequence

validArguments = "Valid arguments are:\n"
validArguments = validArguments + "\t**xN** where N is the number (1,2,...) of matches to generate.\n"
validArguments = validArguments + "\t**seed [someSeed]** to set the random seed. Keeping all other arguments \n"
validArguments = validArguments + "\t\tas they are, the same seed will always yield the same \"random\" results.\n"
validArguments = validArguments + "\t**praise** to praise the current most skilled Brawl Stars player and your matches shall be blessed.\n"
validArguments = validArguments + "\t**shuffle** to shuffle the game types within each match randomly.\n"
validArguments = validArguments + "\t**separate** to additionally print the map sequence separated by game types.\n"
validArguments = validArguments + "\t**keep order**: If all maps available for a certain game type are already used,\n"
validArguments = validArguments + "\t\tthe maps will be used again in the exact same order starting over from the beginning.\n"
validArguments = validArguments + "\t\tBy default this order might be changed slightly.\n"
validArguments = validArguments + "\t**explain** to additionally print an explanation of the arguments used to generate the map sequence.\n"

validGameTypes = "Valid game types are **Solo Showdown, Duo Showdown, Gem Grab, Heist, Bounty, Brawl Ball, Siege, Robo Rumble, Big Game** and **Boss Fight**.\n Instead you could also use the numbers **0, 1, 2, 3, 4, 5, 6, 7, 8** and **9** respectively.\n"

helpText = "If you tell me a list of game types, i will give you a random list of maps for one or more matches, where each match consists of games with the types you told me.\n"
helpText = helpText + "Type \"<maps LIST | ARGUMENTS\" Where LIST contains the comma separated game types and then (optionally) a \"|\" symbol followed by a comma separated list of arguments.\n" + validGameTypes + validArguments


class BSMapExtracter(HTMLParser):
	gType = -1
	checkName = False
	checkType = False
	foundName = False
	def handle_starttag(self, tag, attrs):
		if tag == "h2":
			self.checkType = True
		elif tag == "h3" and self.gType >= 0:
			self.checkName = True
			self.foundName = False

	def handle_endtag(self, tag):
		if tag == "h2":
			self.checkType = False
		elif tag == "h3" and self.gType >= 0:
			self.checkName = False

	def handle_data(self, data):
		if self.checkType:
			if data in gameTypes:
				self.gType = gameTypes.index(data)
			else:
				self.gType = -1
		if self.checkName and self.gType >= 0:
			if self.foundName:
				maps[self.gType][-1] = maps[self.gType][-1] + "&" + data
			else:
				maps[self.gType].append(data)
				self.foundName = True
				

def getMaps():
	global maps 
	maps = [[],[],[],[],[],[],[],[],[],[]]
	#req = urllib2.Request('https://www.starlist.pro/maps/')
	#req.add_header('User-Agent', 'nodeenv/1.0 (https://github.com/ekalinin/nodeenv)')
	#r = urllib2.urlopen(req)
	r = urllib.request.urlopen(urllib.request.Request('https://www.starlist.pro/maps/', headers={'User-Agent': 'Mozilla/5.0'}))
	parser = BSMapExtracter()
	parser.feed(r.read().decode("utf8"))
	r.close()

def printTypeSequences(typeSequences):
	out = "\nRotation separated by game types:\n"
	for i in range(0,len(gameTypes)):
		if len(typeSequences[i]) > 0:
			seq = ""
			for j in range(0,len(typeSequences[i])):
				seq = seq + "\n\t\t" + maps[i][typeSequences[i][j]]
			out = out + "\t" + gameTypes[i] + ":" + seq + "\n\n"
	return out

def printResult(sequence,matchLength):
	out = "\nMap Sequence:"
	for i in range(0,len(sequence)):
		if i%matchLength == 0:
			out = out + "\n"
		out = out + "\t" + sequence[i] + "\n"
	return out

	
def generate(text):
	out = ""
	if SequenceMatcher(None, text.replace(" ","").lower(),"help").ratio() > 0.9 or len(text)==0:
		return helpText
	text = text.split("|",1)
	text[0] = text[0].split(",")
	if len(text) == 2:
		text[1] = text[1].split(",")
	# parse arguments
    
	# gametypes
	useTypes = []
	for i in range(0,len(text[0])):
		sims = []
		for j in range(0,len(gameTypes)):
			sims.append(SequenceMatcher(None, text[0][i].replace(" ","").lower(),gameTypes[j].replace(" ","").lower()).ratio())
		if max(sims) > 0.8:
			useTypes.append(sims.index(max(sims)))
		else:
			try:
				gt = int(text[0][i].replace(" ",""))
			except ValueError:
				gt = -1
			if gt >= 0 and gt <= 8:
				useTypes.append(gt)
			else:
				return "I did'nt recognize the game type \"" + text[0][i] + "\"." + validGameTypes + "Check your game types and try again!"
	if len(useTypes) == 0:
		return helpText
	# other parameters
	keepOrder = False
	separate = False
	shuffle = False
	explain = False
	blessed = False
	numMatches = 1
	seed = ""
	if len(text) == 2:
		for i in range(0,len(text[1])):
			arg = text[1][i].replace(" ","").lower()
			if len(arg) > 0:
				if arg[0] == "x":
					try:
						numMatches = int(arg[1:].replace(" ",""))
					except ValueError:
						return "Could'nt understand \"" + text[0][i] + "\". Did you mean xN where N is a number 1,2,...?"
				elif SequenceMatcher(None, arg[0:3],"seed").ratio() > 0.8:
					np.random.seed(hash(text[1][i].replace(" ","")[4:])%sys.maxsize)
					seed = text[1][i].replace(" ","")[4:]
				elif SequenceMatcher(None, arg,"praise").ratio() > 0.8:
					out = out + "\n" + np.random.choice(["Keep in mind: ","It just cannot be said frequently enough: ","Just in case you forgot: "], 1)[0] + "\n\t" + np.random.choice(["Stoanei is simply the best.","Stoanei rules.","Roses are red, violets are blue, Stoanei's the best and you know it's true."], 1)[0] + "\n"
					blessed = True
				elif SequenceMatcher(None, arg,"shuffle").ratio() > 0.8:
					shuffle = True
				elif SequenceMatcher(None, arg,"separate").ratio() > 0.8:
					separate = True
				elif SequenceMatcher(None, arg,"keeporder").ratio() > 0.8:
					keepOrder = True
				elif SequenceMatcher(None, arg,"explain").ratio() > 0.8:
					explain = True
				else:
					out = "What did you mean with \"" + text[1][i] + "\"? "
					out = out + validArguments
					out = out + "Check your arguments and try again!"
					return out

	if numMatches < 0:
		numMatches = 1
	# setup game type order
	if len(useTypes) == 0:
		useTypes = [0]

	matchLength = len(useTypes)
	if numMatches * matchLength > 100:
		return "I certainly could generate a map list for " + str(numMatches) + " matches making up " + str(numMatches * matchLength) + " single games. But since nobody would play them anyways, i would rather not post the list to avoid spam..."
	types = []
	for i in range(0,numMatches):
			if shuffle:
				np.random.shuffle(useTypes)
			for j in range(0,len(useTypes)):
				types.append(useTypes[j])
		
		

	# obtain available maps from https://www.starlist.pro/maps/
	getMaps()

	# init map probs equally
	probs = []
	for i in range(0,len(maps)):
		probs.append(np.ones(len(maps[i])))

	# init map list for each game type
	typeSequences = [[],[],[],[],[],[],[],[],[]]
	if keepOrder:
		nextForType = [np.array([0]),np.array([0]),np.array([0]),np.array([0]),np.array([0]),np.array([0]),np.array([0]),np.array([0]),np.array([0])]
	else:
		nextForType = [np.array([0,1]),np.array([0,1]),np.array([0,1]),np.array([0,1]),np.array([0,1]),np.array([0,1]),np.array([0,1]),np.array([0,1]),np.array([0,1])]

	sequence = []
	for i in range(0,len(types)):
		t = types[i]
		ps = probs[t]
		if sum(ps) != 0: # choose new map
			ps = ps/sum(ps)
			m = np.random.choice(range(0,len(maps[t])), 1,p=ps)[0]
			ps[m] = 0
			probs[t] = ps
			typeSequences[t].append(m)
			sequence.append(maps[t][m])
		else: # choose map which has been used some time ago
			if len(typeSequences[t]) == 1:
				typeSequences[t].append(typeSequences[t][0])
				m = typeSequences[t][0]
				sequence.append(maps[t][m])
			else:
				nft = nextForType[t]
				np.random.shuffle(nft)
				m = typeSequences[t][nft[0]]
				typeSequences[t].append(m)
				nft[0] = np.max(nft)+1
				sequence.append(maps[t][m])

	# explain
	if explain:
		out = out + "\nThis "
		if blessed:
			out = out + "blessed "
		out = out + "map sequence consists of " + str(numMatches) + " matches, each featuring games with the types *"
		for i in range(0,len(useTypes)):
			if i == len(useTypes)-2:
				out = out + gameTypes[useTypes[i]] + "* and *"
			elif i == len(useTypes)-1:
				out = out + gameTypes[useTypes[i]] + "*"
			else:
				out = out + gameTypes[useTypes[i]] + ", "
		if shuffle:
			out = out + " in shuffled order"
		if keepOrder:
			out = out + ", repeating the order of maps for each game type, if more than the available maps are needed"
			
		out = out + ".\n"
		if seed != "":
			out  = out + "Random seed was taken from \"" + seed + "\".\n"
	
	if separate:
		out = out + printTypeSequences(typeSequences)
	out = out + printResult(sequence,matchLength)
	return out



if len(sys.argv) > 1:
	TOKEN = sys.argv[1]
else:
	TOKEN = os.environ["ACCESS_TOKEN"]

client = discord.Client()	
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith('<maps'):
		print(message.content)
		msg = generate(message.content[5:])
		msg = msg.format(message)
		await message.channel.send(msg)
		
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	
client.run(TOKEN)

