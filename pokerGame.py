import numpy as np
from deck import Deck
from player import Player
from handDeterminer import *

class PokerGame():
	'''
	Controls a poker game
	'''
	def __init__(self,nPlayers):
		self.deck = Deck()
		self.deck.shuffle()
		self.nPlayers = nPlayers
		self.players = [Player(i+1) for i in range(nPlayers)]
		self.hands = []
		self.table = []
		self.winner = None

	def dealHands(self):
		for i in range(self.nPlayers):
			hand = self.deck.dealHand()
			self.hands.append(hand)
			self.players[i].giveHand(hand)
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
		self.winner = findWinner(self.players,self.table)
		return self.winner

	def newDeck(self):
		print("NEW DECK")
		self.deck.newDeck()
		self.deck.shuffle()
		self.hands = []
		self.table = []
		self.winner = None
