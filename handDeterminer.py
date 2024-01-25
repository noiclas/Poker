import numpy as np
from binaryFuncs import *
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
	ranks = np.zeros(len(players))
	bestHands = np.zeros((len(players),5),dtype=str)
	binScores = np.zeros(len(players))
	for i in range(len(players)):
		possHands = list(combinations(players[i].hand+table,5))
		possHands = np.array(possHands)
		print('\n'+players[i].name+':')
		ranks[i],bestHands[i],handDict = determineBestHand(possHands)
		binScores[i] = getBinaryScore(ranks[i],handDict)
		print('binary score:',binScores[i])
	bestRank = np.max(ranks)
	winnersIdx = np.where(ranks==bestRank)[0][:]
	print('winnersIdx:',winnersIdx)
	if len(winnersIdx) == 1:
		print("\n"+players[winnersIdx[0]].name+" wins with "+rankDict[bestRank])
		return [players[winnersIdx[0]]]
	else:
		maxBinScore = np.max(binScores[winnersIdx])
		winnerIdx = np.where(binScores[winnersIdx]==maxBinScore)[0][:]
		print("winnerIdx:",winnerIdx)
		if len(winnerIdx) == 1:
			print("\nPlayer",players[winnersIdx[winnerIdx][0]].name,"wins with",rankDict[bestRank])
			return [players[winnersIdx[winnerIdx][0]]]
		else:
			print("\nPlayers"," and ".join(map(str,players[winnersIdx[winnerIdx]])),"chop with",rankDict[bestRank])
			return players[winnersIdx[winnerIdx]]

def determineBestHand(possHands):
	# Find the best 5 card hand for each player
	ranks = np.zeros(len(possHands))

	for i in range(len(possHands)):
		ranks[i] = determineHand(possHands[i])
	bestRank = np.max(ranks)
	print('best rank : ',rankDict[bestRank])
	bestHandIdx = np.where(ranks==bestRank)[0][:]
	winnerIdx, bestHandDict = determineBestHandSameRank(bestRank,possHands[bestHandIdx])
	print('best hand: ',possHands[bestHandIdx][winnerIdx])
	return bestRank, possHands[bestHandIdx][winnerIdx],bestHandDict
	
	


def determineBestHandSameRank(rank,tiedHands):
	allNums = []
	allCounts = []
	bestHandDict = {'nums':None,'trip':None,'pairs':None,'kickers':None}
	for i in range(len(tiedHands)):
		nums = np.array([int(h[1:]) for h in tiedHands[i]])
		nums.sort()
		count = np.array(list(Counter(nums).values()))
		allCounts.append(count)
		allNums.append(nums)
	bestHandIdx = 0

	if rank == HIGH_CARD:
		#need to compare all cards
		for i in range(len(tiedHands)):
			for j in range(4,-1,-1):
				if allNums[i][j] > allNums[bestHandIdx][j]:
					bestHandIdx = i
					break
				elif allNums[i][j] < allNums[bestHandIdx][j]:
					break
		bestHandDict['nums'] = allNums[bestHandIdx]
		return bestHandIdx, bestHandDict

	elif rank == PAIR:
		#need to compare 3 kickers, pair value is shared for single player possible hands
		bestPairVal = allNums[bestHandIdx][np.argmax(allCounts[bestHandIdx])]
		bestKickers = [num for num in allNums[bestHandIdx] if num!=bestPairVal]
		for i in range(len(tiedHands)):
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
		bestHandDict['pairs'] = bestPairVal
		bestHandDict['kickers'] = bestKickers
		return bestHandIdx, bestHandDict

	elif rank == TWO_PAIR:
		#need to compare the 2 pairs and then last kicker
		bestTwoPairIdx = np.where(allCounts[bestHandIdx]==2)[0]
		bestTwoPairVals = [allNums[bestHandIdx][bestTwoPairIdx[0]],allNums[bestHandIdx][bestTwoPairIdx[1]+2]]
		bestKicker = [num for num in allNums[bestHandIdx] if num not in bestTwoPairVals][0]
		for i in range(len(tiedHands)):
			twoPairIdx  = np.where(allCounts[i]==2)[0]
			twoPairVals = [allNums[i][twoPairIdx[0]],allNums[i][twoPairIdx[1]+2]]
			kicker = [num for num in allNums[i] if num not in twoPairVals][0]
			if twoPairVals < bestTwoPairVals:
				continue
			if twoPairVals > bestTwoPairVals or kicker > bestKicker:
				bestHandIdx = i
				bestTwoPairVals = twoPairVals
				bestKicker = kicker
		bestHandDict['pairs'] = bestTwoPairVals
		bestHandDict['kickers'] = bestKicker
		return bestHandIdx, bestHandDict

	elif rank == THREE_OF_A_KIND:
		#need to compare 2 kickers, trips will be shared for single player possible hands
		tripVal = allNums[bestHandIdx][np.argmax(allCounts[bestHandIdx])]
		bestKickers = [num for num in allNums[bestHandIdx] if num != tripVal]
		for i in range(len(tiedHands)):
			kickers = [num for num in allNums[i] if num != tripVal]
			for j in range(1,-1,-1):
				if kickers[j] > bestKickers[j]:
					bestHandIdx=i
					beskKickers = kickers
					break
				elif kickers[j] < bestKickers[j]:
					break
		bestHandDict['trip'] = tripVal
		bestHandDict['kickers'] = bestKickers 
		return bestHandIdx, bestHandDict

	elif rank == STRAIGHT:
		#only need to compare top card
		for i in range(len(tiedHands)):
			if allNums[i][4] > allNums[bestHandIdx][4]:
				bestHandIdx = i
		bestHandDict['nums'] = allNums[bestHandIdx]
		return bestHandIdx, bestHandDict

	elif rank == FLUSH:
		#need to compare all cards
		for i in range(len(tiedHands)):
			for j in range(4,-1,-1):
				if allNums[i][j] > allNums[bestHandIdx][j]:
					bestHandIdx = i
					break
				elif allNums[i][j] < allNums[bestHandIdx][j]:
					break
		bestHandDict['nums'] = allNums[bestHandIdx]
		return bestHandIdx, bestHandDict

	elif rank == FULL_HOUSE:
		#need to compare trips then pair
		bestTripVal = allNums[bestHandIdx][np.argmax(allCounts[bestHandIdx])+2]
		bestPairVal = [num for num in allNums[bestHandIdx] if num != bestTripVal][0]
		for i in range(len(tiedHands)):
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
		bestHandDict['trip'] = bestTripVal
		bestHandDict['pairs'] = bestPairVal
		return bestHandIdx, bestHandDict

	elif rank == FOUR_OF_A_KIND:
		#need to compare single kicker
		bestQuadIdx = np.argmax(allCounts[bestHandIdx])
		if bestQuadIdx == 0:
			bestKicker = allNums[bestHandIdx][4]
		else:
			bestKicker = allNums[bestHandIdx][0]
		for i in range(len(tiedHands)):
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
		bestHandDict['kickers'] = bestKicker
		return bestHandIdx, bestHandDict

	elif rank == STRAIGHT_FLUSH:
		#need to compare top card
		for i in range(len(tiedHands)):
			if allNums[i][4] > allNums[bestHandIdx][4]:
				bestHandIdx = i
		bestHandDict['nums'] = allNums[bestHandIdx]
		return bestHandIdx, bestHandDict
	else:
		return 0, bestHandDict

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