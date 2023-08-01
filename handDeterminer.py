import numpy as np
from itertools import combinations
from collections import Counter

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

def determineHand(hand,table):
	cardsByValue = sortCardsValue(hand,table)
	cardsBySuit = sortCardsSuit(hand,table)
	valuesSorted = [cardsByValue[i][1] for i in range(len(cardsByValue))]

	is_flush = checkFlush(cardsBySuit)
	is_straight = checkStraight(valuesSorted)
	pairs = checkPair(valuesSorted)
	threeOfKind = checkThreeOfKind(valuesSorted)
	fourOfKind = checkFourOfKind(valuesSorted)

	if fourOfKind[0]:
		print("4 OF A KIND, "+str(fourOfKind[1]))
		return (FOUR_OF_A_KIND, fourOfKind[1])
	if threeOfKind[0] and pairs[0]:
		print("FULL HOUSE")
		return FULL_HOUSE,[threeOfKind[1].pop(),pairs[1].pop()]
	elif is_flush[0]:
		print("FLUSH, "+ str(is_flush[1])+" HIGH.")
		return (FLUSH, is_flush[1])
	elif is_straight[0]:
		print("STRAIGHT, "+str(is_straight[1])+" HIGH.")
		return (STRAIGHT, is_straight[1])
	elif threeOfKind[0]:
		print("3 OF A KIND, "+str(threeOfKind[1]))
		return THREE_OF_A_KIND, threeOfKind[1]
	elif pairs[0]:
		if len(pairs[1])==2:
			print("TWO PAIR, " +str(pairs[1])+".")
			return (TWO_PAIR, pairs[1][0])
		elif len(pairs[1])==1:
			print("PAIR, "+str(pairs[1])+".")
			return (PAIR, pairs[1][0])
	else:
		print("HIGH CARD, " +str(max(card[1] for card in hand)))
		return HIGH_CARD, max(card[1] for card in hand)



def sortCardsValue(hand,table):
	allCards = hand+table
	sortedCards = sorted(allCards, key = lambda x:x[1])
	return sortedCards

def sortCardsSuit(hand,table):
	allCards = hand+table
	sortedCards = sorted(allCards, key = lambda x:x[0])
	return sortedCards

def checkPair(values):
	valueCounts = Counter(values)

	pairs = [value for value, count in valueCounts.items() if count == 2]
	if any(pairs):
		if len(pairs) > 2:
			pairs.pop(0)
		return True, pairs
	return False, None

def checkThreeOfKind(values):
	valueCounts = Counter(values)

	threeOfKind = [value for value, count in valueCounts.items() if count == 3]
	if any(threeOfKind):
		return True, threeOfKind
	return False, None

def checkFourOfKind(values):
	valueCounts = Counter(values)

	fourOfKind = [value for value, count in valueCounts.items() if count == 4]
	if any(fourOfKind):
		return True, fourOfKind
	return False, None
def checkFlush(cards):
	for five_cards in combinations(cards,5):
		if all(card[0] == five_cards[0][0] for card in five_cards):
			return True, max(card[1] for card in five_cards)
	return False, None

def checkStraight(values):
	#Create a sorted set of the card values
	sortedValuesSet = list(set(values))

	#No point in checking straight if there are less than 5 unique values
	if len(sortedValuesSet) < 5:
		return False, None

	#Check for normal straights
	for i in reversed(range(len(sortedValuesSet)-4)):
		if all(sortedValuesSet[i+j]==sortedValuesSet[i+j+1]-1 for j in range(4)):
			return True, sortedValuesSet[i+4]

	#Check for 5 high straights
	fiveHighStraight = [14,2,3,4,5]
	fiveHighCount = 0
	for val in fiveHighStraight:
		if val in sortedValuesSet:
			fiveHighCount +=1
	if fiveHighCount == 5:
		return True, 5

	return False, None