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

#establish the hand class
class Hand:
    def __init__(self):
        self.cards = []
    def __len__(self):
        return len(self.cards)
    def __getitem__(self, position):
        return self.cards[position]
    @property
    def value(self):
        total = 0
        for card in sorted(self.cards, key= sortHand):
            if card.rank.isnumeric():
                total += int(card.rank)
            elif card.rank == 'Ace':
                total += 11
                if total > 21:
                    total -= 10
            else:
                total += 10
        return total
    @property
    def bust(self):
        if self.value > 21:
            return True
        else:
            return False
    @property
    def blackjack(self):
        face = ['10', 'Jack', 'Queen', 'King']
        if len(self.cards) == 2:
            facecards = 0
            aces = 0
            for card in self.cards:
                if card.rank in face:
                    facecards += 1
                if card.rank == 'Ace':
                    aces += 1
            if facecards == 1 and aces == 1:
                return True
            else:
                return False
        else:
            return False

#establish a function to ask player if they want to play again
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

#create function to add a card to hand
def hit(hand):
    hand.append(deck[drawCard()])

#establish function for player actions
def playeraction(hand):
    x = 0
    while x == 0:
        if playerH[0][0] == playerH[1][0]:
            options.append('split')
        if len(hand) > 2:
            if 'double down' in options:
                options.remove('double down')
            if 'split' in options:
                options.remove('split')
        response = input('What would you like to do? Your options are: ' + ', '.join(options)).strip().lower()
        if response == 'hit':
            hit(hand.cards)
            print(f'You drew the {hand[-1][0]} of {hand[-1][1]}. Your hand is now {hand.value}.')
            if hand.bust:
                print(f'You have busted. Better luck next time, {name}.')
                restarter()
                return True
        elif response == 'stand':
            print('You have chosen to stand.')
            x += 1
        elif response == 'double down':
            if len(hand) > 2:
                print('You cannot double down as you\'ve already received an extra card.')
            else:
                hit(hand.cards)
                print(f'You have chosen to double down. You drew the {hand[-1][0]} of {hand[-1][1]}. Your hand is now {hand.value}.')
                if hand.bust:
                    print(f'You have busted. Better luck next time, {name}.')
                    restarter()
                    return True
                x += 1
        else:
            print('Please pick an option.')
    return False

# welcome the player and ask their name
name = input('Welcome to the blackjack table. What is your name?').strip()
print(f'Good luck, {name}.')


#establish face cards for blackjack purposes
face = ['10', 'Jack', 'Queen', 'King']

#start game loop
while True:
    #establish deck
    deck = FrenchDeck()

    cards = []
    for i in range(0, 52):
        cards.append(i)

    #create hands of the player and dealer and draw two cards for each
    playerH = Hand()
    hit(playerH.cards)
    hit(playerH.cards)
    dealerH = Hand()
    hit(dealerH.cards)
    hit(dealerH.cards)

    #set blackjacks to false
    playerBJ = False
    dealerBJ = False

    #set extra cards drawn to 0
    extracards = 0

    #set restart trigger to false
    done = False

    #reveal player's starting hand and the dealer's first card
    print(f'You have the {playerH[0][0]} of {playerH[0][1]} and the {playerH[1][0]} of {playerH[1][1]} for a total of {playerH.value}. The dealer is showing the {dealerH[0][0]} of {dealerH[0][1]}.')

    #if both player and dealer have blackjack
    if playerH.blackjack and dealerH.blackjack:
        print('Both you and the dealer have blackjack. The hand is a push. What are the odds?')
        restarter()
        continue

    #if just the player has blackjack
    if playerH.blackjack and not dealerH.blackjack:
        print('You have blackjack. Big money!')
        restarter()
        continue

    #if the dealer is showing an ace, ask about insurance
    w = 0
    while w == 0 and dealerH[0][0] == 'Ace' and not playerBJ:
        response = input('The dealer is showing an ace, would you like to buy insurance? (yes or no)').strip().lower()
        if response == 'yes':
            if dealerH.blackjack:
                print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} and therefore they have blackjack, but you won the insurance bet. Well done, {name}')
                restarter()
                done = True
                break
            else:
                print('The dealer does not have blackjack, so you lost the insurance bet. But, the hand continues.')
                w += 1
        elif response == 'no':
            if dealerH.blackjack:
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
    if dealerH.blackjack:
        print('The dealer\'s facedown card is an ace and therefore they have blackjack. Tough luck.')
        restarter()
        continue

    #establish options for the player's action
    options = ['hit', 'stand', 'double down']

    # ask player what they want to do
    done = playeraction(playerH)

    #restart if the game is done
    if done == True:
        continue

    #reveal the dealer's other card
    print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} for a total of {dealerH.value}.')

    #check the dealer's result and draw cards if necessary
    y = 0
    while y == 0:
        if dealerH.bust:
            print(f'The dealer has busted. {name} wins!')
            restarter()
            done = True
            break
        elif (dealerH.value <= 21) and (dealerH.value >= 17):
            y += 1
        else:
            hit(dealerH.cards)
            print(f'The dealer draws the {dealerH[-1][0]} of {dealerH[-1][1]}. The dealer now has {dealerH.value}.')

    #restart if the game is done
    if done == True:
        continue

    #if neither have busted, compare results
    if playerH.value > dealerH.value:
        print(f'You have beaten the dealer with a hand of {playerH.value} vs. their {dealerH.value}. Congratulations!')
        restarter()
        continue
    elif playerH.value < dealerH.value:
        print(f'The dealer has beaten you with a hand of {dealerH.value} vs. your {playerH.value}. Better luck next time.')
        restarter()
        continue
    else:
        assert playerH.value == dealerH.value
        print(f'You and the dealer both have {playerH.value}. The hand is a push.')
        restarter()
        continue