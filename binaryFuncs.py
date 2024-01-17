import numpy as np

HIGH_CARD = 0
PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
STRAIGHT = 4
FLUSH = 5
FULL_HOUSE = 6
FOUR_OF_A_KIND = 7
STRAIGHT_FLUSH = 8
ROYAL_FLUSH = 9

def getBinaryScore(rank,handDict):
	binScore = ''
	if rank == HIGH_CARD:
		for i in range(4,-1,-1):
			binScore += bin(handDict['nums'][i]-1)[2:].zfill(4)
		return binScore
	elif rank == PAIR:
		binScore += bin(handDict['pairs']-1)[2:].zfill(4)
		for kicker in reversed(handDict['kickers']):
			binScore += bin(kicker-1)[2:].zfill(4)
		return binScore
	elif rank == TWO_PAIR:
		binScore += bin(handDict['pairs'][1]-1)[2:].zfill(4)
		binScore += bin(handDict['pairs'][0]-1)[2:].zfill(4)
		binScore += bin(handDict['kickers']-1)[2:].zfill(4)
		return binScore
	elif rank == THREE_OF_A_KIND:
		binScore += bin(handDict['trip']-1)[2:].zfill(4)
		for kicker in reversed(handDict['kickers']):
			binScore += bin(kicker-1)[2:].zfill(4)
		return binScore
	elif rank == STRAIGHT:
		#binscore not really necessary but whatever
		binScore = bin(handDict['nums'][4]-1)[2:].zfill(4)
		return binScore
	elif rank == FLUSH:
		for i in range(4,-1,-1):
			binScore += bin(handDict['nums'][i]-1)[2:].zfill(4)
		return binScore
	elif rank == FULL_HOUSE:
		binScore += bin(handDict['trip']-1)[2:].zfill(4)
		binScore += bin(handDict['pairs']-1)[2:].zfill(4)
		return binScore
	elif rank == FOUR_OF_A_KIND:
		binScore += bin(handDict['kickers']-1)[2:].zfill(4)
		return binScore
	elif rank == STRAIGHT_FLUSH:
		#binscore not really necessary but whatever
		binScore = bin(handDict['nums'][4]-1)[2:].zill(4)
		return binScore
	else:
		return '0'