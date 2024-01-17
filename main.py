import pygame
import sys
import time
import numpy as np

from pokerGame import PokerGame

pygame.init()
pygame.font.init()
pygame.display.set_caption('NIC\'S POKER')
clk = pygame.time.Clock()
windowSize = (910,726)

WHITE = (255,255,255)
GREEN = (53,101,77)

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
			  'h14':pygame.image.load('cards/h14.png')
			  }
cardWidth =	CARDS['s2'].get_rect().width
cardHeight = CARDS['s2'].get_rect().height
TABLEX = windowSize[0]/7
TABLEY = windowSize[1]/2 - cardHeight/8


# Blits the currently shared cards on the center of the window
def draw_table(table):
	for i in range(len(table)):
		window.blit(pygame.transform.scale(CARDS[table[i]], (cardWidth/4, cardHeight/4)),(TABLEX*(i+1),TABLEY))

# Blits the players' hands on the window. Only up to 4 players for now
def draw_hands(hands):
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

		

def main():
	NPLAYERS = 4
	game = PokerGame(NPLAYERS)
	done = False
	COUNT = 0
	winner = False
	HANDS = False
	while not done:
		#Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				pass
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
						game.newDeck()
						COUNT += 1
		'''
		game.newDeck()
		game.dealHands()
		game.dealFlop()
		game.dealTurnRiver()
		game.dealTurnRiver()'''
		window.fill(GREEN)
		if COUNT ==1:
			game.dealHands()
			game.dealFlop()
			game.GameStatus()
			HANDS = True
			COUNT +=1
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
			draw_hands(game.hands)
			#window.blit(pygame.transform.scale(CARDS[game.hands[0][0][0]+str(game.hands[0][0][1])], (cardWidth/4, cardHeight/4)),(TABLEX*(1),TABLEY+cardHeight/4))
			#window.blit(pygame.transform.scale(CARDS[game.hands[0][1][0]+str(game.hands[0][1][1])], (cardWidth/4, cardHeight/4)),(TABLEX*(2),TABLEY+cardHeight/4))

		draw_table(game.table)
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