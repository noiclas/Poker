import numpy as np
from deck import Deck
from player import Player
from handDeterminer import *

SMALL_BLIND = 5
BIG_BLIND = 10
STAGES = ['PRE FLOP','FLOP','TURN','RIVER']

class PokerGame:
	'''
	Controls a poker game
	'''
	def __init__(self,nPlayers):
		self.deck = Deck()
		self.deck.shuffle()
		self.nPlayers = nPlayers
		self.Allplayers = [Player(i+1) for i in range(nPlayers)]
		self.players = np.copy(self.Allplayers)
		self.hands = []
		self.table = []
		self.turn = 0
		self.pot = 0
		self.playerUp = self.players[self.turn]
		self.playersLeft = len(self.players)
		self.dealerIdx = 0
		self.bettingRound = False
		self.playersReady = 0

	def dealHands(self):
		for i in range(self.nPlayers):
			hand = self.deck.dealHand()
			self.hands.append(hand)
			self.players[i].giveHand(hand)

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
		winner = findWinner(self.players,self.table)
		#winner = findWinner(self.players,['c10','c11','c12','c13','c14']) this is for chop testing
		for player in winner:
			player.winPot(self.pot/len(winner))
			print(player.name+" wins "+str(self.pot/len(winner)))

	def newRound(self):
		print("Starting New Round")
		self.deck.newDeck()
		self.deck.shuffle()
		self.players = np.copy(self.Allplayers)
		self.playersLeft = self.nPlayers
		self.hands = []
		self.dealHands()
		self.table = []
		self.pot = 0
		self.dealerIdx += 1
		self.dealerIdx %= self.nPlayers
		self.bettingRound = False
		self.playersReady = 0

	def nextPlayer(self):
		self.turn += 1
		self.turn %= self.playersLeft
		self.playerUp = self.players[self.turn]

	def removePlayer(self,playerIdx):
		del self.Allplayers[playerIdx]
		self.nPlayers -= 1

	def foldPlayer(self):
		self.players = np.delete(self.players,self.turn)
		self.turn -= 1
		self.playersLeft -= 1
		if self.playersLeft == 1:
			print(self.players[0].name,"wins!")
			self.newRound()

	def addToPot(self,bet):
		self.pot += bet

	def nextStage(self):
		if len(self.table) == 0:
			print("\nDealing Flop")
			self.dealFlop()
		elif len(self.table) == 3:
			print("\nDealing Turn")
			self.dealTurnRiver()
		elif len(self.table) == 4:
			print("\nDealing River")
			self.dealTurnRiver()
		else:
			self.findWinner()
			self.newRound()
		self.playersReady = 0

	def addReadyPlayer(self):
		self.playersReady += 1

	def resetReadyPlayers(self):
		self.playersReady = 1
