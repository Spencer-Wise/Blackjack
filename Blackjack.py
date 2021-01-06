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

#create a function to draw a card from remaining deck
def drawCard():
    return cards.pop(randrange(0, len(cards)))

#create a function to sort hand so aces are last
def sortHand(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value

#create a function to calculate the value of a hand
def handValue(hand):
    total = 0
    for card in sorted(hand, key= sortHand):
        if card.rank.isnumeric():
            total += int(card.rank)
        elif card.rank == 'Ace':
            total += 11
            if total > 21:
                total -= 10
        else:
            total += 10
    return total

def restarter():
    while True:
        response = input('Would you like to play again?').strip().lower()
        if response == 'yes':
            return
        elif response == 'no':
            print(f'Thank you for playing, {name}. Goodbye.')
            sys.exit()
        else:
            print('Please response with yes or no.')

def hit(hand):
    hand.append(deck[drawCard()])

# welcome the player and ask their name
name = input('Welcome to the blackjack table. What is your name?').strip()
print(f'Good luck, {name}.')


#establish face cards for blackjack purposes
face = ['10', 'Jack', 'Queen', 'King']

while True:
    #establish deck
    deck = FrenchDeck()

    cards = []
    for i in range(0, 52):
        cards.append(i)

    #draw two cards for the player and the dealer
    playerH, dealerH = [deck[drawCard()], deck[drawCard()]], [deck[drawCard()], deck[drawCard()]]

    #set blackjacks to false
    playerBJ = False
    dealerBJ = False

    #set extra cards drawn to 0
    extracards = 0

    #set restart trigger to false
    done = False

    #reveal player's starting hand and the dealer's first card
    print(f'You have the {playerH[0][0]} of {playerH[0][1]} and the {playerH[1][0]} of {playerH[1][1]} for a total of {handValue(playerH)}. The dealer is showing the {dealerH[0][0]} of {dealerH[0][1]}.')

    #check if player has blackjack
    if (playerH[0][0] == 'Ace' and (playerH[1][0] in face)) or (playerH[1][0] == 'Ace' and (playerH[0][0] in face)):
        playerBJ = True

    #check if the dealer has blackjack
    if (dealerH[0][0] == 'Ace' and (dealerH[1][0] in face)) or (dealerH[1][0] == 'Ace' and (dealerH[1][0] in face)):
        dealerBJ = True

    #if both player and dealer have blackjack
    if playerBJ and dealerBJ:
        print('Both you and the dealer have blackjack. The hand is a push.')
        restarter()
        continue

    #if just the player has blackjack
    if playerBJ and not dealerBJ:
        print('You have blackjack. Big money!')
        restarter()
        continue

    #if the dealer is showing an ace, ask about insurance
    w = 0
    while w == 0 and dealerH[0][0] == 'Ace' and not playerBJ:
        response = input('The dealer is showing an ace, would you like to buy insurance? (yes or no)').strip().lower()
        if response == 'yes':
            if dealerBJ:
                print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} and therefore they have blackjack, but you won the insurance bet. Well done, {name}')
                restarter()
                done = True
                break
            else:
                print('The dealer does not have blackjack, so you lost the insurance bet. But, the hand continues.')
                w += 1
        elif response == 'no':
            if dealerBJ:
                print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} and therefore they have blackjack. Tough luck old chap')
                restarter()
                done = True
                break
            else:
                print('The dealer does not have blackjack. The hand continues.')
                w += 1
        else:
            print('Please respond yes or no')

    #restart if game is done
    if done == True:
        continue

    #if the dealer has hidden blackjack
    if dealerBJ:
        print('The dealer\'s facedown card is an ace and therefore they have blackjack. Tough luck.')
        restarter()
        continue

    # ask player what they want to do
    x = 0
    while x == 0:
        if extracards == 0:
            response = input('What would you like to do? Your options are to hit, stand, or double down.').strip().lower()
        else:
            response = input('What would you like to do? Your options are to hit or stand.').strip().lower()
        if response == 'hit':
            hit(playerH)
            extracards += 1
            print(f'You drew the {playerH[-1][0]} of {playerH[-1][1]}. Your hand is now {handValue(playerH)}.')
            if handValue(playerH) > 21:
                print(f'You have busted. Better luck next time, {name}.')
                restarter()
                done = True
                break
        elif response == 'stand':
            print('You have chosen to stand.')
            x += 1
        elif response == 'double down':
            if extracards != 0:
                print('You cannot double down as you\'ve already received an extra card.')
            else:
                hit(playerH)
                print(f'You have chosen to double down. You drew the {playerH[-1][0]} of {playerH[-1][1]}. Your hand is now {handValue(playerH)}.')
                if handValue(playerH) > 21:
                    print(f'You have busted. Better luck next time, {name}.')
                    restarter()
                    done = True
                    break
                x += 1
        else:
            print('Please pick an option.')

    #restart if the game is done
    if done == True:
        continue

    #reveal the dealer's other card
    print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} for a total of {handValue(dealerH)}.')

    #check the dealer's result and draw cards if necessary
    y = 0
    while y == 0:
        if handValue(dealerH) > 21:
            print(f'The dealer has busted. {name} wins!')
            restarter()
            done = True
            break
        elif (handValue(dealerH) <= 21) and (handValue(dealerH) >= 17):
            y += 1
        else:
            hit(dealerH)
            print(f'The dealer draws the {dealerH[-1][0]} of {dealerH[-1][1]}. The dealer now has {handValue(dealerH)}.')

    #restart if the game is done
    if done == True:
        continue

    #if neither have busted, compare results
    if handValue(playerH) > handValue(dealerH):
        print(f'You have beaten the dealer with a hand of {handValue(playerH)} vs. their {handValue(dealerH)}. Congratulations!')
        restarter()
        continue
    elif handValue(playerH) < handValue(dealerH):
        print(f'The dealer has beaten you with a hand of {handValue(dealerH)} vs. your {handValue(playerH)}. Better luck next time.')
        restarter()
        continue
    else:
        print(f'You and the dealer both have {handValue(playerH)}. The hand is a push.')
        restarter()
        continue

