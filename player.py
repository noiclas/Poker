CHECK = 0
FOLD = -1
BET = 1

class Player:
	def __init__(self,playerNum, hand=[],name='no name', stack=1000):
		self.playerNum = playerNum
		self.hand = hand
		self.name = name
		self.stack = stack
		self.playing = True
		self.betting = False

	def giveHand(self,hand):
		self.hand = hand

	def bet(self,bet):
		self.stack -= bet
	
	def winPot(self,pot):
		self.stack += pot

	def setRank(self,rank):
		self.rank = rank

	def changeBettingStatus(self):
		self.betting != self.betting