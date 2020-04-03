#!/usr/bin/env python
import numpy as np
import urllib2
import sys
from HTMLParser import HTMLParser


matchLength = 5
keepOrder = False
separate = False

# All Maps by Game Type
gameTypes = ["Showdown","Gem Grab","Heist","Bounty","Brawl Ball","Siege","Robo Rumble","Big Game","Boss Fight"]
maps = [[],[],[],[],[],[],[],[],[]]

# Game Type Sequence
useTypes = []
numMatches = 1
shuffle = False

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
	maps = [[],[],[],[],[],[],[],[],[]]
	req = urllib2.Request('https://www.starlist.pro/maps/')
	req.add_header('User-Agent', 'nodeenv/1.0 (https://github.com/ekalinin/nodeenv)')
	r = urllib2.urlopen(req)
	parser = BSMapExtracter()
	parser.feed(r.read())

def printTypeSequences(typeSequences):
	print("\nRotation separated by game types:")
	for i in range(0,len(gameTypes)):
		if len(typeSequences[i]) > 0:
			seq = ""
			for j in range(0,len(typeSequences[i])):
				seq = seq + "\n\t\t" + maps[i][typeSequences[i][j]]
			print("\t" + gameTypes[i] + ":" + seq + "\n")

def printResult(sequence):
	out = "\nMap Sequence:"
	for i in range(0,len(sequence)):
		if i%matchLength == 0:
			out = out + "\n"
		out = out + "\t" + sequence[i] + "\n"
	print(out)

# parse arguments
for i in range(1,len(sys.argv)):
	if sys.argv[i][:2] == "-r":
		try:
			seed = int(sys.argv[i][3:])
			np.random.seed(seed)
		except ValueError:
			print("Random seed must be of type integer, found \"" + sys.argv[i][3:] + "\" instead.")
	elif sys.argv[i] == "-p" or sys.argv[i] == "--praise":
		print("\n" + np.random.choice(["Keep in mind: ","It just cannot be said frequently enough: ","Just in case you forgot: "], 1)[0] + "\n\t" + np.random.choice(["Stonei is simply the best.","Stoanei rules.","Roses are red, violets are blue, Stoanei's the best and you know it's true."], 1)[0])
	elif sys.argv[i][:2] == "-t":
		useTypes = map(int, sys.argv[i][3:].strip('[]').split(','))
	elif sys.argv[i] == "-s" or  sys.argv[i] == "--shuffle":
		shuffle = True
	elif  sys.argv[i][:2] == "-n":
		try:
			numMatches = int(sys.argv[i][3:])
		except ValueError:
			print("Number of Matches must be an integer, found \"" + sys.argv[i][3:] + "\" instead.")
			numMatches = 1
	elif sys.argv[i] == "-g" or  sys.argv[i] == "--gametype":
		separate = True
	elif sys.argv[i] == "-k" or  sys.argv[i] == "--keep":
		keepOrder = True

# setup game type order
if len(useTypes) == 0:
	useTypes = [0]

matchLength = len(useTypes)
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
		m = np.random.choice(range(0,len(maps[t])), 1,p=ps)
		ps[m] = 0
		probs[t] = ps
		typeSequences[t].append(m[0])
		sequence.append(maps[t][m[0]])
	else: # choose map which has been used some time ago
		nft = nextForType[t]
		np.random.shuffle(nft)
		m = typeSequences[t][nft[0]]
		typeSequences[t].append(m)
		nft[0] = np.max(nft)+1
		sequence.append(maps[t][m])

if separate:
	printTypeSequences(typeSequences)
printResult(sequence)



