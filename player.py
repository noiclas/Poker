class Player():
	def __init__(self,playerNum, hand=[],name=None, bank=1000):
		self.playerNum = playerNum
		self.hand = hand
		self.name = name
		self.bank = bank
		self.playing = True

	def giveHand(self,hand):
		self.hand = hand

	def check(self):
		return

	def bet(self):
		return

	def fold(self):
		self.playing = False

	def setRank(self,rank):
		self.rank = rank