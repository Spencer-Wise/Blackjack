from random import randrange
import collections
import sys

Card = collections.namedtuple('Card', ['rank', 'suit'])

#create deck class
class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + 'Jack Queen King Ace'.split()
    suits = 'Spades Diamonds Clubs Hearts'.split()
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, position):
        return self._cards[position]

#establish deck
deck = FrenchDeck()
# for card in deck:
#     print(card, card.rank, card.suit)
cards = []
for i in range(0, 52):
    cards.append(i)

#create a function to draw a card from remaining deck
def drawCard():
    return cards.pop(randrange(0, len(cards)))

#create a function to calculate the value of a hand
def handValue(hand):
    total = 0
    for card in hand:
        if card.rank.isnumeric():
            total += int(card.rank)
        elif card.rank == 'Ace':
            total += 11
            if total > 21:
                total -= 10
        else:
            total += 10
    return total

#draw two cards for the player and the dealer
playerH, dealerH = [deck[drawCard()], deck[drawCard()]], [deck[drawCard()], deck[drawCard()]]



#set blackjacks to false
playerBJ = False
dealerBJ = False

#welcome the player
print('Welcome to the blackjack table. Good luck.')

#reveal player's starting hand and the dealer's first card
print(f'You have the {playerH[0][0]} of {playerH[0][1]} and the {playerH[1][0]} of {playerH[1][1]} for a total of {handValue(playerH)}. The dealer is showing the {dealerH[0][0]} of {dealerH[0][1]}.')

#check if player has blackjack
if (playerH[0][0] == 'Ace' and (playerH[1][0] == '10' or playerH[1][0] == 'Jack' or playerH[1][0] == 'Queen' or playerH[1][0] == 'King')) or (playerH[1][0] == 'Ace' and (playerH[0][0] == '10' or playerH[0][0] == 'Jack' or playerH[0][0] == 'Queen' or playerH[0][0] == 'King')):
    playerBJ = True

#check if the dealer has blackjack
if (dealerH[0][0] == 'Ace' and (dealerH[1][0] == '10' or dealerH[1][0] == 'Jack' or dealerH[1][0] == 'Queen' or dealerH[1][0] == 'King')) or (dealerH[1][0] == 'Ace' and (dealerH[1][0] == '10' or dealerH[0][0] == 'Jack' or dealerH[0][0] == 'Queen' or dealerH[0][0] == 'King')):
    dealerBJ = True

#if both player and dealer have blackjack, end game
if playerBJ and dealerBJ:
    print('Both you and the dealer have blackjack. The hand is a push.')
    sys.exit()

#if player has blackjack
if playerBJ and not dealerBJ:
    print('You have blackjack. Big money!')
    sys.exit()

#if dealer is showing an ace, ask about insurance
w = 0
while w == 0 and dealerH[0][0] == 'Ace' and not playerBJ:
    response = input('The dealer is showing an ace, would you like to buy insurance? (yes or no)').lstrip()
    if response == 'yes':
        if dealerBJ:
            print('The dealer has blackjack, but you won the insurance bet. Congratulations')
            sys.exit()
        else:
            print('The dealer does not have blackjack, so you lost the insurance bet. But, the hand continues.')
        w += 1
    elif response == 'no':
        if dealerBJ:
            print('The dealer has blackjack. Tough luck old chap')
            sys.exit()
        else:
            print('The dealer does not have blackjack. The hand continues.')
        w += 1
    else:
        print('Please respond yes or no')

# ask player what they want to do
x = 0
while x == 0:
    response = input('What would you like to do? Hit, stand, or double down?').lstrip()
    if response == 'hit':
        playerH.append(deck[drawCard()])
        print(f'You drew the {playerH[-1][0]} of {playerH[-1][1]}. Your hand is now {handValue(playerH)}.')
        if handValue(playerH) > 21:
            print('You have busted. Better luck next time.')
            sys.exit()
    elif response == 'stand':
        print('You have chosen to stand.')
        x += 1
    elif response == 'double down':
        playerH.append(deck[drawCard()])
        print(f'You have chosen to double down. You drew the {playerH[-1][0]} of {playerH[-1][1]}. Your hand is now {handValue(playerH)}.')
        if handValue(playerH) > 21:
            print('You have busted. Better luck next time.')
            sys.exit()
        x += 1
    else:
        print('Please pick an option.')

#reveal the dealer's hand
print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} for a total of {handValue(dealerH)}.')

#check the dealer's result and draw cards if necessary
y = 0
while y == 0:
    if handValue(dealerH) > 21:
        print('The dealer has busted. You win. Congratulations!')
        sys.exit()
    elif (handValue(dealerH) <= 21) and (handValue(dealerH) >= 17):
        y += 1
    else:
        dealerH.append(deck[drawCard()])
        print(f'The dealer draws the {dealerH[-1][0]} of {dealerH[-1][1]}. The dealer now has {handValue(dealerH)}.')

#if neither have busted, compare results
if handValue(playerH) > handValue(dealerH):
    print(f'You have beaten the dealer with a hand of {handValue(playerH)} vs. their {handValue(dealerH)}. Congratulations!')
elif handValue(playerH) < handValue(dealerH):
    print(f'The dealer has beaten you with a hand of {handValue(dealerH)} vs. your {handValue(playerH)}. Better luck next time.')
else:
    print(f'You and the dealer both have {handValue(playerH)}. The hand is a push.')

