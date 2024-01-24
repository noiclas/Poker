import numpy as np
import random

SUITS = ['s','c','d','h']
VALUES = np.arange(2,15)

class Deck:
	'''
	Represents a standard deck of 52 cards

	Cards are represented by a tuple: composed of the suit spade = 's', club = 'c',
		diamond = 'd', heart = 'h' at index 0. Value 2-10 are
		2-10, jack = 11, queen = 12, king = 13, and ace = 14 at index 1.
			e.g: queen of diamonds is represented by ('d',12)

	Cards are held in a list of strings named cards
	
	Functions are self-explanatory: initializing the deck, shuffling the deck, dealing cards, 
		burning cards

	'''
	def __init__(self):
		self.cards = self.initDeck()


	def initDeck(self):
		'''
		Initializes the cards list to a fresh deck of cards
		'''
		cards = []
		for suit in SUITS:
			for value in VALUES:
				cards.append((suit+str(value)))
		return cards

	def newDeck(self):
		self.cards = self.initDeck()
		
	def shuffle(self):
		'''
		Randomly shuffles the cards
		'''
		random.shuffle(self.cards)

	def printDeck(self):
		'''
		Prints the deck out in the standard output
		'''
		print(self.cards)

	def dealCard(self):
		'''
		Deals the card at the top of the deck

		Returns:
		str: card at held at 0 index
		-1: deck is empty
		'''
		if len(self.cards)==0:
			return -1
		else:
			return self.cards.pop(0)

	def burnCard(self):
		'''
		Burns the top card i.e the card held at index 0

		Returns:
		-1: deck is empty
		'''
		if len(self.cards)==0:
			return -1
		else:
			self.cards.pop(0)	


	def dealHand(self):
		'''
		Deals the top two cards as a hand

		Returns:
		list: length-2 list containing the two cards
		'''
		hand = []
		hand.append(self.dealCard())
		hand.append(self.dealCard())
		return hand
		#Technically should be cyclically dealing but the deck is all random anyway

	def dealFlop(self):
		'''
		Burn the top card and deal three out

		Returns:
		list: length-3 list containing 3 cards
		'''
		flop = []
		self.burnCard()
		for i in range(3):
			flop.append(self.dealCard())
		return flop

	def dealTurnRiver(self):
		'''
		Burn the top card and deal one out. Turn and 
		River card have the same process

		Returns:
		str: card
		'''
		self.burnCard()
		return self.dealCard()