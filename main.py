import pygame
import sys
import time
import numpy as np
from GraphicalEntities import *

from pokerGame import PokerGame

pygame.init()
pygame.font.init()
pygame.display.set_caption('NIC\'S POKER')
clk = pygame.time.Clock()
windowSize = (910,726)
buttonSize = (200,50)

WHITE = (255,255,255)
GREEN = (53,101,77)
DARK_GREEN = (0,102,0)
GREY = (128,128,128)

#Set font and font size for any text in the game
font = pygame.font.Font('freesansbold.ttf',20)

#Create game window
window = pygame.display.set_mode(windowSize)
#window.fill((53,101,77))

#Load in card images from ./cards (lookup table)
CARDS = {'s2':pygame.image.load('cards/s2.png'),'s3':pygame.image.load('cards/s3.png'),'s4':pygame.image.load('cards/s4.png'),
			  's5':pygame.image.load('cards/s5.png'),'s6':pygame.image.load('cards/s6.png'),'s7':pygame.image.load('cards/s7.png'),
			  's8':pygame.image.load('cards/s8.png'),'s9':pygame.image.load('cards/s9.png'),'s10':pygame.image.load('cards/s10.png'),
			  's11':pygame.image.load('cards/s11.png'),'s12':pygame.image.load('cards/s12.png'),'s13':pygame.image.load('cards/s13.png'),
			  's14':pygame.image.load('cards/s14.png'),'c2':pygame.image.load('cards/c2.png'),'c3':pygame.image.load('cards/c3.png'),
			  'c4':pygame.image.load('cards/c4.png'),'c5':pygame.image.load('cards/c5.png'),'c6':pygame.image.load('cards/c6.png'),
			  'c7':pygame.image.load('cards/c7.png'),'c8':pygame.image.load('cards/c8.png'),'c9':pygame.image.load('cards/c9.png'),
			  'c10':pygame.image.load('cards/c10.png'),'c11':pygame.image.load('cards/c11.png'),'c12':pygame.image.load('cards/c12.png'),
			  'c13':pygame.image.load('cards/c13.png'),'c14':pygame.image.load('cards/c14.png'),'d2':pygame.image.load('cards/d2.png'),
			  'd3':pygame.image.load('cards/d3.png'),'d4':pygame.image.load('cards/d4.png'),'d5':pygame.image.load('cards/d5.png'),
			  'd6':pygame.image.load('cards/d6.png'),'d7':pygame.image.load('cards/d7.png'),'d8':pygame.image.load('cards/d8.png'),
			  'd9':pygame.image.load('cards/d9.png'),'d10':pygame.image.load('cards/d10.png'),'d11':pygame.image.load('cards/d11.png'),
			  'd12':pygame.image.load('cards/d12.png'),'d13':pygame.image.load('cards/d13.png'),'d14':pygame.image.load('cards/d14.png'),
			  'h2':pygame.image.load('cards/h2.png'),'h3':pygame.image.load('cards/h3.png'),'h4':pygame.image.load('cards/h4.png'),
			  'h5':pygame.image.load('cards/h5.png'),'h6':pygame.image.load('cards/h6.png'),'h7':pygame.image.load('cards/h7.png'),
			  'h8':pygame.image.load('cards/h8.png'),'h9':pygame.image.load('cards/h9.png'),'h10':pygame.image.load('cards/h10.png'),
			  'h11':pygame.image.load('cards/h11.png'),'h12':pygame.image.load('cards/h12.png'),'h13':pygame.image.load('cards/h13.png'),
			  'h14':pygame.image.load('cards/h14.png'),'back':pygame.image.load('cards/back7.png')
			  }
cardWidth =	CARDS['s2'].get_rect().width
cardHeight = CARDS['s2'].get_rect().height
TABLEX = windowSize[0]/7
TABLEY = windowSize[1]/2 - cardHeight/8


# Blits the currently shared cards on the center of the window
def drawTable(game):
	table = game.table
	for i in range(len(table)):
		window.blit(pygame.transform.scale(CARDS[table[i]], (cardWidth/4, cardHeight/4)),(TABLEX*(i+1),TABLEY))
	for j in range(len(table),5):
		window.blit(pygame.transform.scale(CARDS['back'],(cardWidth/4, cardHeight/4)),(TABLEX*(j+1),TABLEY))

# Blits the players' hands on the window. Only up to 4 players for now
def drawHands(game):
	hands = game.hands
	for i in range(len(hands)):
		if i < 2:
			window.blit(pygame.transform.scale(CARDS[hands[i][0]], 
				(cardWidth/4, cardHeight/4)),(TABLEX*(1+3*(i%2)),TABLEY-3*cardHeight/8))
			window.blit(pygame.transform.scale(CARDS[hands[i][1]], 
				(cardWidth/4, cardHeight/4)),(TABLEX*(2+3*(i%2)),TABLEY-3*cardHeight/8))
		else:
			window.blit(pygame.transform.scale(CARDS[hands[i][0]], 
				(cardWidth/4, cardHeight/4)),(TABLEX*(1+3*(i%2)),TABLEY+3*cardHeight/8))
			window.blit(pygame.transform.scale(CARDS[hands[i][1]], 
				(cardWidth/4, cardHeight/4)),(TABLEX*(2+3*(i%2)),TABLEY+3*cardHeight/8))

def drawPlayerView(game):
	player = game.players[game.turn]
	window.blit(pygame.transform.scale(CARDS[player.hand[0]], 
				(cardWidth/4, cardHeight/4)),(windowSize[0]/2-cardWidth/4,windowSize[1]-cardHeight/4))
	window.blit(pygame.transform.scale(CARDS[player.hand[1]], 
				(cardWidth/4, cardHeight/4)),(windowSize[0]/2,windowSize[1]-cardHeight/4))




		

def main():
	NPLAYERS = 2
	game = PokerGame(NPLAYERS)
	game.Allplayers[0].name = 'cracker'
	game.Allplayers[1].name = 'goober'
	foldButton = Button(window,50,windowSize[1]-150,buttonSize[0],buttonSize[1],DARK_GREEN,'FOLD BUTTON')
	checkButton = Button(window,50,windowSize[1]-200,buttonSize[0],buttonSize[1],DARK_GREEN,'CHECK BUTTON')
	betButton = Button(window,50,windowSize[1]-100,buttonSize[0],buttonSize[1],DARK_GREEN,'BET BUTTON')
	playerNameBox = TextRectangle(window,windowSize[0]/2-100,windowSize[1]-250,buttonSize[0],buttonSize[1],GREEN,'PLAYER NAME BOX')
	potBox = TextRectangle(window,windowSize[0]-50-buttonSize[0],windowSize[1]-150,buttonSize[0],buttonSize[1],GREEN,"POT : 0",35)
	stackBox = TextRectangle(window,windowSize[0]-50-buttonSize[0],windowSize[1]-100,buttonSize[0],buttonSize[1],GREEN,"STACK TEXT BOX",35)
	betEntryBox = TextEntryBox(window,50,windowSize[1]-50,buttonSize[0],buttonSize[1],GREEN,35)
	done = False
	COUNT = 0
	roundCounter = 0
	winner = False
	HANDS = False
	betting = False
	while not done:
		#Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mousePos = pygame.mouse.get_pos()
				if foldButton.isClicked(mousePos):
					print(game.playerUp.name,"folds")
					game.foldPlayer()
					game.nextTurn()
					betting = False
				elif checkButton.isClicked(mousePos):
					print(game.playerUp.name,"checks")
					game.nextTurn()
					betting = False
				elif betButton.isClicked(mousePos):
					print(game.playerUp.name,"is betting")
					betEntryBox.active = True
					betting = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
						game.newRound()
						COUNT += 1
				bet = int(betEntryBox.enterText(event))
				if bet > 0:
					game.playerUp.bet(bet)
					game.addToPot(bet)
					potBox.updateText("POT : "+str(game.pot))

		window.fill(GREEN)
		foldButton.draw()
		checkButton.draw()
		betButton.draw()
		playerNameBox.updateText(game.players[game.turn].name)
		playerNameBox.draw()
		potBox.draw()
		stackBox.updateText("STACK : "+str(game.players[game.turn].stack))
		stackBox.draw()
		if betting:
			betEntryBox.draw()

		if COUNT ==1:
			'''
			game.dealHands()
			game.dealFlop()
			game.GameStatus()
			HANDS = True
			'''
			game.dealHands()
			drawPlayerView(game)
			COUNT =-1
		if COUNT ==-1:
			drawPlayerView(game)
		elif COUNT == 2:
			game.dealTurnRiver()
			COUNT += 1
		elif COUNT == 3:
			game.dealTurnRiver()
			#force royal flush
			#game.table = ['s14','s13','s12','s11','s10']
			game.findWinner()
			COUNT += 1
		else:
			COUNT =0
		if HANDS:
			drawHands(game)
			#window.blit(pygame.transform.scale(CARDS[game.hands[0][0][0]+str(game.hands[0][0][1])], (cardWidth/4, cardHeight/4)),(TABLEX*(1),TABLEY+cardHeight/4))
			#window.blit(pygame.transform.scale(CARDS[game.hands[0][1][0]+str(game.hands[0][1][1])], (cardWidth/4, cardHeight/4)),(TABLEX*(2),TABLEY+cardHeight/4))

		drawTable(game)
		#game.nextTurn()
		#Update the pygame window
		pygame.display.update()
		'''
		winner=game.findWinner()
		if winner:
			time.sleep(100)
		'''

		#Force FPS to be 60 
		clk.tick(60)

	pygame.quit()
	sys.exit()

main()