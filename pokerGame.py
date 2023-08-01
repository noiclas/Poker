import numpy as np
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
		self.winner = 0

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
		rankings = []
		for i in range(len(self.hands)):
			rankings.append(determineHand(self.hands[i],self.table))
		print(rankings)
		bestRank = max(rankings, key=lambda x:x[0])
		winners = [i for i,rank in enumerate(rankings) if rank[0] == bestRank[0]]
		if len(winners) == 1:
			print("Player "+str(winners[0]+1)+" wins!")
		else:
			print("Need to check best hand some more")

	def newDeck(self):
		print("NEW DECK")
		self.deck.newDeck()
		self.deck.shuffle()
		self.hands = []
		self.table = []
