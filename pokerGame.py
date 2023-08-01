from deck import Deck
from handDeterminer import *

class PokerGame():
	'''
	Controls a poker game
	'''
	def __init__(self,nPlayers):
		self.deck = Deck()
		self.deck.shuffle()
		self.nPlayers = nPlayers
		self.hands = []
		self.table = []

	def dealHands(self):
		for i in range(self.nPlayers):
			self.hands.append(self.deck.dealHand())
			print("HAND DEALT")

	def dealFlop(self):
		self.table= self.deck.dealFlop()

	def dealTurnRiver(self):
		self.table.append(self.deck.dealTurnRiver())

	def GameStatus(self):
		print()
		for i in range(self.nPlayers):
			print("player"+str(i+1)+":")
			print(self.hands[i])
		print("table:" )
		print(self.table)
		print()

	def findWinner(self):
		for hand in self.hands:
			determineHand(hand,self.table)

	def newDeck(self):
		print("NEW DECK")
		self.deck.newDeck()
		self.deck.shuffle()
		self.hands = []
		self.table = []
