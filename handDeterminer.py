import numpy as np
from itertools import combinations
from collections import defaultdict
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
rankDict = {0:'high card',1:'pair',2:'two pair',3:'three of a kind',4:'straight',5:'flush',
			6:'full house',7:'four of a kind',8:'straight flush',9:'royal flush'}

def findWinner(players, table):
	ranks = [] # having annoying array/list/ndarray datatype issues
	bestHands = []
	for i in range(len(players)):
		possHands = list(combinations(players[i].hand+table,5))
		possHands = np.array(possHands)
		print('player',players[i].playerNum)
		rank,bestHand = determineBestHand(possHands)
		ranks.append(rank)
		bestHands.append(bestHand)
	bestRank = np.max(ranks)
	winnerIdx = np.where(ranks==bestRank)[0][:]
	if len(winnerIdx) == 1:
		print("Player",winnerIdx[0]+1,"wins with",rankDict[bestRank])
	else:
		for i in range(len(players)):
			'''
			need to implement tie breaking/pot splitting

			pot split when players have the exact same rank and/or card values
			tie breaking when players have same rank
			'''

def determineBestHand(possHands):
	# Find the best 5 card hand for each player
	ranks = np.zeros(len(possHands))

	for i in range(len(possHands)):
		ranks[i] = determineHand(possHands[i])
	bestRank = np.max(ranks)
	print('best rank : ',rankDict[bestRank])
	bestHandIdx = np.where(ranks==bestRank)[0][:]
	if len(bestHandIdx) == 1:
		print('best hand: ',possHands[bestHandIdx[0]],'\n')
		return bestRank,possHands[bestHandIdx]
	else:
		tieWinnerIdx = determineTie(bestRank,possHands[bestHandIdx])
		bestHand = possHands[bestHandIdx][tieWinnerIdx]
	print('best hand: ',bestHand,'\n')
	return bestRank, possHands[bestHandIdx]


def determineTie(rank,tiedHands):
	allNums = []
	allCounts = []
	for i in range(len(tiedHands)):
		nums = np.array([int(h[1:]) for h in tiedHands[i]])
		nums.sort()
		count = np.array(list(Counter(nums).values()))
		allCounts.append(count)
		allNums.append(nums)
	bestHandIdx = 0

	if rank == HIGH_CARD:
		#need to compare all cards
		for i in range(1,len(tiedHands)):
			for j in range(4,-1,-1):
				if allNums[i][j] > allNums[bestHandIdx][j]:
					bestHandIdx = i
					break
				elif allNums[i][j] < allNums[bestHandIdx][j]:
					break
		return bestHandIdx

	elif rank == PAIR:
		#need to compare 3 kickers, pair value is shared for single player possible hands
		bestPairVal = allNums[bestHandIdx][np.argmax(allCounts[bestHandIdx])]
		bestKickers = [num for num in allNums[bestHandIdx] if num!=bestPairVal]
		for i in range(1,len(tiedHands)):
			pairVal = allNums[i][np.argmax(allCounts[i])]
			kickers = [num for num in allNums[i] if num!=pairVal]
			if pairVal > bestPairVal:
				bestHandIdx = i
				bestPairVal = pairVal
				bestKickers = kickers
				continue
			elif pairVal < bestPairVal:
				continue
			for j in range(2,-1,-1):
				if kickers[j] > bestKickers[j]:
					bestHandIdx = i
					bestKickers = kickers
					break
				elif kickers[j] < bestKickers[j]:
					break
		return bestHandIdx

	elif rank == TWO_PAIR:
		#need to compare the 2 pairs and then last kicker
		bestTwoPairIdx = np.where(allCounts[bestHandIdx]==2)[0]
		bestTwoPairVals = [allNums[bestHandIdx][bestTwoPairIdx[0]],allNums[bestHandIdx][bestTwoPairIdx[1]+2]]
		bestKicker = [num for num in allNums[bestHandIdx] if num not in bestTwoPairVals][0]
		for i in range(1,len(tiedHands)):
			twoPairIdx  = np.where(allCounts[i]==2)[0]
			twoPairVals = [allNums[i][twoPairIdx[0]],allNums[i][twoPairIdx[1]+2]]
			kicker = [num for num in allNums[i] if num not in twoPairVals][0]
			if twoPairVals < bestTwoPairVals:
				continue
			if twoPairVals > bestTwoPairVals or kicker > bestKicker:
				bestHandIdx = i
				bestTwoPairVals = twoPairVals
				bestKicker = kicker
		return bestHandIdx

	elif rank == THREE_OF_A_KIND:
		#need to compare 2 kickers, trips will be shared for single player possible hands
		tripVal = allNums[bestHandIdx][np.argmax(allCounts[bestHandIdx])]
		bestKickers = [num for num in allNums[bestHandIdx] if num != tripVal]
		for i in range(1,len(tiedHands)):
			kickers = [num for num in allNums[i] if num != tripVal]
			for j in range(1,-1,-1):
				if kickers[j] > bestKickers[j]:
					bestHandIdx=i
					beskKickers = kickers
					break
				elif kickers[j] < bestKickers[j]:
					break
		return bestHandIdx

	elif rank == STRAIGHT:
		#only need to compare top card
		for i in range(1,len(tiedHands)):
			if allNums[i][4] > allNums[bestHandIdx][4]:
				bestHandIdx = i
		return bestHandIdx

	elif rank == FLUSH:
		#need to compare all cards
		for i in range(1,len(tiedHands)):
			for j in range(4,-1,-1):
				if allNums[i][j] > allNums[bestHandIdx][j]:
					bestHandIdx = i
					break
				elif allNums[i][j] < allNums[bestHandIdx][j]:
					break
		return bestHandIdx

	elif rank == FULL_HOUSE:
		#need to compare trips then pair
		bestTripVal = allNums[bestHandIdx][np.argmax(allCounts[bestHandIdx])+2]
		bestPairVal = [num for num in allNums[bestHandIdx] if num != bestTripVal][0]
		for i in range(1,len(tiedHands)):
			tripVal = allNums[i][np.argmax(allCounts[i])+2]
			pairVal = [num for num in allNums[i] if num !=bestTripVal][0]
			if tripVal < bestTripVal:
				continue 
			elif tripVal > bestTripVal:
				bestHandIdx = i
				bestTripVal = tripVal
				bestPairVal = pairVal
				continue
			elif pairVal > bestPairVal:
				bestHandIdx = i
		return bestHandIdx

	elif rank == FOUR_OF_A_KIND:
		#need to compare single kicker
		bestQuadIdx = np.argmax(allCounts[bestHandIdx])
		if bestQuadIdx == 0:
			bestKicker = allNums[bestHandIdx][4]
		else:
			bestKicker = allNums[bestHandIdx][0]
		for i in range(1,len(tiedHands)):
			quadIdx = np.argmax(allCounts[i])
			if bestQuadIdx == 0:
				kicker = allNums[i][4]
			else:
				kicker = allNums[i][0]
			if kicker < bestKicker:
				continue
			if kicker > bestKicker:
				bestHandIdx = i
				bestKicker = kicker
		return bestHandIdx

	elif rank == STRAIGHT_FLUSH:
		#need to compare top card
		for i in range(1,len(tiedHands)):
			if allNums[i][4] > allNums[bestHandIdx][4]:
				bestHandIdx = i
		return bestHandIdx

def determineHand(hand):
	suits = set(h[0] for h in hand)
	nums = [int(h[1:]) for h in hand]
	nums.sort()
	counts = Counter(nums)

	if checkRoyalFlush(suits,nums):
		return ROYAL_FLUSH
	elif checkStraightFlush(suits,nums):
		return STRAIGHT_FLUSH
	elif checkFourOfKind(counts):
		return FOUR_OF_A_KIND
	elif checkFullHouse(counts):
		return FULL_HOUSE
	elif checkFlush(suits):
		return FLUSH
	elif checkStraight(nums):
		return STRAIGHT
	elif checkThreeOfKind(counts):
		return THREE_OF_A_KIND
	elif checkTwoPair(counts):
		return TWO_PAIR
	elif checkPair(counts):
		return PAIR
	else:
		return HIGH_CARD

def checkFlush(suits):
	if len(suits) == 1:
		return True
	else:
		return False

def checkStraight(nums):
	if nums == [2,3,4,5,14]:
		return True
	for i in range(4):
		if nums[i] != nums[i+1] - 1:
			return False
	return True

def checkRoyalFlush(suit,nums):
	topCard = nums[4]
	if checkStraightFlush(suit,nums) and topCard == 14:
		return True
	else:
		return False

def checkStraightFlush(suit,nums):
	if checkFlush(suit):
		if checkStraight(nums):
			return True

def checkFourOfKind(counts):
	if sorted(counts.values()) == [1,4]:
		return True
	else:
		return False

def checkFullHouse(counts):
	if sorted(counts.values()) == [2,3]:
		return True
	else:
		return False

def checkThreeOfKind(counts):
	if sorted(counts.values()) == [1,1,3]:
		return True
	else:
		return False

def checkTwoPair(counts):
	if sorted(counts.values()) == [1,2,2]:
		return True
	else:
		return False

def checkPair(counts):
	if sorted(counts.values()) == [1,1,1,2]:
		return True
	else:
		return False

