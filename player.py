CHECK = 0
FOLD = -1
BET = 1

class Player:
	def __init__(self,playerNum, hand=[],name=None, stack=1000):
		self.playerNum = playerNum
		self.hand = hand
		self.name = name
		self.stack = stack
		self.playing = True

	def giveHand(self,hand):
		self.hand = hand

	def check(self):
		return CHECK

	def bet(self):
		self.stack -= bet
		return BET, bet

	def fold(self):
		self.playing = False
		return FOLD

	def setRank(self,rank):
		self.rank = rank