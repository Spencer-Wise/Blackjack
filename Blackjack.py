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
        self.done = False
        self.stand = False
        self.wager = 0
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
        response = input('Would you like to play again? ').strip().lower()
        if response == 'yes':
            return
        elif response == 'no':
            print(f'Thank you for playing, {name}. Goodbye.')
            sys.exit()
        else:
            print('Please respond with yes or no. ')

#create function to add a card to hand
def hit(hand):
    hand.append(deck[drawCard()])

#establish function for player actions
def playeraction(i, hand):
    while True:
        if hand[0][0] == hand[1][0] and 'split' not in options:
            options.append('split')
        if hand[0][0] != hand[1][0] and 'split' in options:
            options.remove('split')
        if len(hand) > 2:
            if 'double down' in options:
                options.remove('double down')
        if len(playerHands) > 1:
            print(f'For hand number #{i}, the total is {hand.value}. Your cards are:')
            for card in hand:
                print('{} of {}'.format(card[0], card[1]))
        response = input('What would you like to do? Your options are: ' + ', '.join(options) + ' ').strip().lower()
        if response == 'hit':
            hit(hand.cards)
            print(f'You drew the {hand[-1][0]} of {hand[-1][1]}. Your hand is now {hand.value}.')
            if hand.bust:
                print(f'You have busted. Better luck next time, {name}.')
                return True
        elif response == 'stand':
            print('You have chosen to stand.')
            hand.stand = True
            break
        elif response == 'double down':
            if len(hand) > 2:
                print('You cannot double down as you\'ve already received an extra card.')
            else:
                hit(hand.cards)
                print(f'You have chosen to double down. You drew the {hand[-1][0]} of {hand[-1][1]}. Your hand is now {hand.value}.')
                if hand.bust:
                    print(f'You have busted. Better luck next time, {name}.')
                    return True
                hand.stand = True
                break
        elif response == 'split':
            if len(hand) == 2 and hand[0][0] == hand[1][0]:
                nexthand = len(playerHands) + 1
                playerHands[nexthand] = Hand()
                playerHands[nexthand].cards.append(hand.cards.pop(1))
                hit(hand.cards)
                hit(playerHands[nexthand].cards)
                return False
            else:
                print('You may not split this hand.')
        else:
            print('Please pick an option. ')
    return False

#establish a function to check if all hands have busted (or stands)
def endCheck(handsdict):
    count = 0
    for hand in handsdict.values():
        if hand.done == True:
            count += 1
    if count == len(handsdict):
        return True
    elif dealerH.bust == True:
        return True
    else:
        return False

# welcome the player and ask their name
name = input('Welcome to the blackjack table. What is your name? ').strip()
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
    playerHands = {}
    playerHands[1] = Hand()
    hit(playerHands[1].cards)
    hit(playerHands[1].cards)
    # playerHands[1].cards.append(deck[1])
    # playerHands[1].cards.append(deck[14])
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
    print(f'You have the {playerHands[1][0][0]} of {playerHands[1][0][1]} and the {playerHands[1][1][0]} of {playerHands[1][1][1]} for a total of {playerHands[1].value}. The dealer is showing the {dealerH[0][0]} of {dealerH[0][1]}.')

    #if both player and dealer have blackjack
    if playerHands[1].blackjack and dealerH.blackjack:
        print('Both you and the dealer have blackjack. The hand is a push. What are the odds?')
        restarter()
        continue

    #if just the player has blackjack
    if playerHands[1].blackjack and not dealerH.blackjack:
        print('You have blackjack. Big money!')
        restarter()
        continue

    #if the dealer is showing an ace, ask about insurance
    w = 0
    while w == 0 and dealerH[0][0] == 'Ace' and not playerHands[1].blackjack:
        response = input('The dealer is showing an ace, would you like to buy insurance? (yes or no)').strip().lower()
        if response == 'yes':
            if dealerH.blackjack:
                print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} and therefore they have blackjack, but you won the insurance bet. Well done, {name}')
                playerHands[1].done = True
                break
            else:
                print('The dealer does not have blackjack, so you lost the insurance bet. But, the hand continues.')
                w += 1
        elif response == 'no':
            if dealerH.blackjack:
                print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} and therefore they have blackjack. Tough luck old chap')
                playerHands[1].done = True
                break
            else:
                print('The dealer does not have blackjack. The hand continues.')
                w += 1
        else:
            print('Please respond yes or no')

    #restart if game is done
    if endCheck(playerHands) == True:
        restarter()
        continue

    #if the dealer has hidden blackjack
    if dealerH.blackjack:
        print('The dealer\'s facedown card is an ace and therefore they have blackjack. Tough luck.')
        restarter()
        continue

    #establish options for the player's action
    options = ['hit', 'stand', 'double down']

    # loop through player actions
    while True:
        playerHandsCopy = playerHands.copy()
        for i, hand in playerHandsCopy.items():
            if hand.bust == True or hand.stand == True:
                continue
            hand.done = playeraction(i, hand)
            playerHands[i] = playerHandsCopy[i]
        count = 0
        for hand in playerHands.values():
            if hand.bust == True or hand.stand == True:
                count +=1
        if count == len(playerHands):
            break

    #restart if the game is done
    if endCheck(playerHands) == True:
        restarter()
        continue

    #reveal the dealer's other card
    print(f'The dealer\'s other card is the {dealerH[1][0]} of {dealerH[1][1]} for a total of {dealerH.value}.')

    #check the dealer's result and draw cards if necessary
    while True:
        if dealerH.bust:
            print(f'The dealer has busted. {name} wins!')
            dealerH.done = True
            break
        elif (dealerH.value <= 21) and (dealerH.value >= 17):
            break
        else:
            assert dealerH.value < 17
            hit(dealerH.cards)
            print(f'The dealer draws the {dealerH[-1][0]} of {dealerH[-1][1]}. The dealer now has {dealerH.value}.')

    #restart if the game is done
    if endCheck(playerHands) == True:
        restarter()
        continue

    #if neither have busted, compare results
    for i, hand in playerHands.items():
        if hand.bust == False:
            if len(playerHands) != 1 :
                print(f'For hand number #{i}:')
            if hand.value > dealerH.value:
                print(f'You have beaten the dealer with a hand of {hand.value} vs. their {dealerH.value}. Congratulations!')
            elif hand.value < dealerH.value:
                print(f'The dealer has beaten you with a hand of {dealerH.value} vs. your {hand.value}. Better luck next time.')
            else:
                assert hand.value == dealerH.value
                print(f'You and the dealer both have {hand.value}. The hand is a push.')
            hand.done = True

    for hand in playerHands.values():
        assert hand.done
    restarter()
    continue