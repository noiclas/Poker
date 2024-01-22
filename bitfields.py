

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

lookup_bits = {'2': 1, '3': 2, '4': 4, '5': 8, '6': 16, '7': 32, '8': 64, '9': 128, '10': 256, '11': 512, '12': 1024, '13': 2048, '14': 4096}

def ffs(x):
    """Returns the index, counting from 0, of the
    least significant set bit in `x`.
    """
    return (x&-x).bit_length()-1

def clz(x):
	"""Returns the number of leading zero bits in `x`.
	"""
	return x.bit_length() - 1

def maxConsecutiveOnes(x):
	"""Returns the largest count of consecutive 1s in `x`.
	   TODO: use ffs/clz to make this faster.
	"""
	count = 0
	while (x!=0):
		# This operation reduces length
        # of every sequence of 1s by one.
		x = (x & (x << 1))
		count=count+1
	return count 

def nHighestCards(x,n):
    mask = 0
    y = 0
    for i in range(n):
        mask |= 1<<ffs(x)
        y |= x & ~mask 
    return y

def determineBestHand_(hand):
	#convert hand in a bitfield
	diamonds = 0
	hearts = 0
	spades = 0
	clubs = 0
	for card in hand:
		match card[0]:
			case 'd':
				diamonds |= lookup_bits[card[1:]]
			case 'h':
				hearts |= lookup_bits[card[1:]]
			case 's':
			    spades |= lookup_bits[card[1:]]
			case 'c':
				clubs |= lookup_bits[card[1:]]
	royal_flush = lookup_bits['14'] | lookup_bits['13'] | lookup_bits['12'] | lookup_bits['11'] | lookup_bits['10']
	royal_flush_test = (royal_flush & diamonds) == royal_flush or (royal_flush & hearts) == royal_flush or (royal_flush & spades) == royal_flush or (royal_flush & clubs) == royal_flush
	if (royal_flush_test):
		return ROYAL_FLUSH, 0
	if (maxConsecutiveOnes(diamonds) >= 5):
		return STRAIGHT_FLUSH, nHighestCards(diamonds)
	if (maxConsecutiveOnes(hearts) >= 5):
		return STRAIGHT_FLUSH, nHighestCards(hearts)
	if (maxConsecutiveOnes(spades) >= 5):
		return STRAIGHT_FLUSH, nHighestCards(spades)
	if (maxConsecutiveOnes(clubs) >= 5):
		return STRAIGHT_FLUSH, nHighestCards(clubs)
	four_of_a_kinds = diamonds & hearts & spades & clubs
	if (four_of_a_kinds.bit_count() !=0):
		mask = ~four_of_a_kinds
		highcard = (diamonds|hearts|spades|clubs) & mask
		return FOUR_OF_A_KIND, four_of_a_kinds << 13 | nHighestCards(highcard,1)
	
	three_of_a_kinds = diamonds & hearts & spades | diamonds & hearts & clubs | diamonds & spades & clubs | hearts & spades & clubs
	pairs = diamonds & hearts | diamonds & spades | diamonds & clubs | hearts & spades | hearts & clubs | spades & clubs
	
	if (pairs.bit_count() >= 2) and (three_of_a_kinds.bit_count() >= 1):
		best_trip = nHighestCards(three_of_a_kinds,1)
		tripmask = ~best_trip
		best_pair = nHighestCards(pairs & tripmask,1)
		pairmask = ~best_pair
		highcard =  (diamonds|hearts|spades|clubs) & pairmask & tripmask
		return FULL_HOUSE, best_trip << 26 | best_pair << 13 | nHighestCards(highcard,1)
	
	if diamonds.bit_count() >= 5:
		return FLUSH, nHighestCards(diamonds,5)
	if hearts.bit_count() >= 5:
		return FLUSH, nHighestCards(hearts,5)
	if spades.bit_count() >= 5:
		return FLUSH, nHighestCards(spades,5)
	if clubs.bit_count() >= 5:
		return FLUSH, nHighestCards(clubs,5)
	
	if maxConsecutiveOnes(diamonds|hearts|spades|clubs) >=5:
		return STRAIGHT, nHighestCards(diamonds|hearts|spades|clubs,5)
	
	if three_of_a_kinds.bit_count() > 0:
		mask = ~three_of_a_kinds
		highcard = (diamonds|hearts|spades|clubs) & mask
		return THREE_OF_A_KIND, three_of_a_kinds << 13 | nHighestCards(highcard,2)
	
	if pairs.bit_count() >= 2:
		higest_pair = nHighestCards(pairs,2)
		mask = ~higest_pair
		highcard = (diamonds|hearts|spades|clubs) & mask
		return TWO_PAIR, pairs << 13 | nHighestCards(highcard,1)
	
	if pairs:
		#score is pair rank, and then highcard rankDict
		mask = ~pairs
		highcard = (diamonds|hearts|spades|clubs) & mask
		return PAIR, pairs << 13 | nHighestCards(highcard,3)
	else:
		highcard = diamonds|hearts|spades|clubs
		return HIGH_CARD, nHighestCards(highcard,5)
