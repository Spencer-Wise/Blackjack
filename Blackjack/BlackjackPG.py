from random import randrange
import sys
import json
import pygame
import inspect
import os
import time

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(path)
cardpaths = []
for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith('.png')):
            cardpaths.append(os.path.join(root,file))

#initalize pygame window
pygame.init()
winSize = winW, winH = 1920, 1080
win = pygame.display.set_mode((winSize))
pygame.display.set_caption('Blackjack')
black = 0, 0, 0
green = 0, 255, 0
white = 255, 255, 255
input_box = pygame.Rect(250, 250, 100, 100)
active = False
color = black

#open data from stats.json or create new file and format it
try:
    file1 = open('stats.json')
    data = json.load(file1)
    file1.close()
except:
    file1 = open('stats.json', 'w+')
    print('No data found')
    data = {'hands': 0, 'hits': 0, 'stands': 0, 'DDs': 0, 'splits': 0, 'wins': 0, 'losses': 0, 'pushes': 0,
            'player busts': 0, 'dealer busts': 0, 'playerBJs': 0, 'dealerBJs': 0, 'high score': 0,
            'ibets taken': 0, 'ibets won': 0, 'ibets lost': 0, 'ibets missed': 0, 'ibets avoided': 0}
    json.dump(data, file1)
    file1.close()

#establish card tuple with rank and suit
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    @property
    def iLoc(self):
        string = self.rank + self.suit[0]
        imagepath = path + r'\Cards' + chr(92) + string + '.png'
        return imagepath

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

#create a function to sort hand so aces are calculated last
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
    global balance, betbox
    yesbutton = Button(710, 490, 250, 100, green, 'yes')
    nobutton = Button(960, 490, 250, 100, green, 'no')
    while True:
        text = font.render('Would you like to play another hand?', True, white)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yesbutton.isOver(pos):
                    print('success')
                if nobutton.isOver(pos):
                    print('not success')
            if event.type == pygame.MOUSEMOTION:
                if yesbutton.isOver(pos):
                    yesbutton.color = white
                else:
                    yesbutton.color = green
                if nobutton.isOver(pos):
                    nobutton.color = white
                else:
                    nobutton.color = green
        print('restarter')
        win.fill(black)
        yesbutton.draw(win, white)
        nobutton.draw(win, white)
        win.blit(balancebanner, (850, 20))
        win.blit(text, (300, 300))
        pygame.display.flip()
        clock.tick(30)

#create function to add a card to hand
def hit(hand):
    hand.append(deck[drawCard()])

#establish function for player actions
def playeraction(i, hand):
    global balance
    while True:
        if hand[0].rank == hand[1].rank and 'split' not in options:
            options.append('split')
        if hand[0].rank != hand[1].rank and 'split' in options:
            options.remove('split')
        if len(hand) > 2:
            if 'double down' in options:
                options.remove('double down')
        if len(playerHands) > 1:
            print(f'For hand number #{i}, the total is {hand.value}. Your cards are:')
            for card in hand:
                print('{} of {}'.format(card.rank, card.suit))
        response = input('What would you like to do? Your options are: ' + ', '.join(options) + '. \n').strip().lower()
        if response == 'hit':
            data['hits'] += 1
            hit(hand.cards)
            print(f'You drew the {hand[-1].rank} of {hand[-1].suit}. Your hand is now {hand.value}.')
            if hand.bust:
                data['player busts'] += 1
                data['losses'] += 1
                print(f'You have busted. Better luck next time, {name}.')
                return True
        elif response == 'stand':
            data['stands'] += 1
            print('You have chosen to stand.')
            hand.stand = True
            break
        elif response == 'double down':
            if len(hand) > 2:
                print('You cannot double down as you\'ve already received an extra card.')
            elif hand.wager > balance:
                print('You do not have enough funds to double down.')
            else:
                data['DDs'] += 1
                balance -= hand.wager
                hand.wager *= 2
                hit(hand.cards)
                print(f'You have chosen to double down. You drew the {hand[-1].rank} of {hand[-1].suit}. Your hand is now {hand.value}.')
                if hand.bust:
                    data['player busts'] += 1
                    data['losses'] += 1
                    print(f'You have busted. Better luck next time, {name}.')
                    return True
                hand.stand = True
                break
        elif response == 'split':
            if hand.wager <= balance:
                if len(hand) == 2 and hand[0].rank == hand[1].rank:
                    data['hands'] += 1
                    data['splits'] += 1
                    nexthand = len(playerHands) + 1
                    playerHands[nexthand] = Hand()
                    playerHands[nexthand].cards.append(hand.cards.pop(1))
                    balance -= hand.wager
                    playerHands[nexthand].wager = hand.wager
                    hit(hand.cards)
                    hit(playerHands[nexthand].cards)
                    return False
                else:
                    print('You may not split this hand.')
            else:
                print('You do not have enough funds to split this hand.')
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

class InputBox:
    def __init__(self, x, y, w, h, text= ''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = green
        self.text = text
        self.textsurface = font.render(text, True, self.color)
        self.active = False
        self.deactivate = False

    def handle_event(self, event):
        if self.deactivate == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
                self.color = white if self.active else green
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.deactivate = True
                        push = self.text
                        self.text = ''
                        return push
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    self.textsurface = font.render(self.text, True, self.color)
    def update(self):
        if self.deactivate == False:
            width = max(200, self.textsurface.get_width() + 10)
            self.rect.w = width

    def draw(self, window):
        if self.deactivate == False:
            window.blit(self.textsurface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(window, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, w, h, color, text= ''):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.w + 4, self.h + 4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, white)
            win.blit(text, (self.x + (self.w/2 -text.get_width()/2), self.y + (self.h/2 - text.get_height()/2)))
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False

#give them 1000 chips to start with
balance = 1000

text = ''
font = pygame.font.SysFont('comicsans', 30)
clock = pygame.time.Clock()
namebox = InputBox(300, 450, 100, 30)
betbox = InputBox(300, 450, 100, 30)
inputboxes = [namebox, betbox]
name = ''

# establish deck
deck = FrenchDeck()

#start game by asking player's name
while True:
    intro = font.render('Welcome to the blackjack table. What is your name?', True, white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        name = namebox.handle_event(event)
    if name is not None:
        win.fill(black)
        intro = font.render(f'Good luck, {name}. You have 1000 chips to start.', True, white)
        win.blit(intro, (300, 300))
        pygame.display.flip()
        time.sleep(3)
        break

    namebox.update()
    win.fill(black)
    win.blit(intro, (300, 300))
    namebox.draw(win)
    pygame.display.flip()
    clock.tick(30)

#start game loop
while True:

    #create deck for this hand
    cards = []
    for i in range(0, 52):
        cards.append(i)

    #create hands of the player and dealer and draw two cards for each
    playerHands = {}
    playerHands[1] = Hand()
    hit(playerHands[1].cards)
    hit(playerHands[1].cards)
    # data['hands'] += 1
    # playerHands[1].cards.append(deck[1])
    # playerHands[1].cards.append(deck[14])
    dealerH = Hand()
    hit(dealerH.cards)
    hit(dealerH.cards)
    # dealerH.cards.append(deck[-1])
    # dealerH.cards.append(deck[-2])

    bet = None
    #ask player how much they want to wager for the hand
    while True:
        betbox.deactivate = False
        text = font.render('How much would you like to wager on this hand?', True, white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            bet = betbox.handle_event(event)
        if bet is not None:
            try:
                bet = int(bet)
                if bet > 0 and bet < balance:
                    balance -= bet
                    playerHands[1].wager = bet
                    break
            except:
                bet = None
        balancebanner = font.render(f'Balance: {balance}', True, white)
        betbox.update()
        win.fill(black)
        win.blit(balancebanner, (850, 20))
        win.blit(text, (300, 300))
        betbox.draw(win)
        pygame.display.flip()
        clock.tick(30)

    balancebanner = font.render(f'Balance: {balance}', True, white)
    card1 = pygame.image.load(playerHands[1][0].iLoc)
    card2 = pygame.image.load(playerHands[1][1].iLoc)
    card3 = pygame.image.load(dealerH[0].iLoc)
    card4 = pygame.image.load(path + r'\Cards\Cardback.png')
    win.fill(black)
    win.blit(balancebanner, (850, 20))
    win.blit(card1, (50, 50))
    win.blit(card2, (190, 50))
    win.blit(card3, (50, 240))
    win.blit(card4, (190, 240))
    pygame.display.flip()
    time.sleep(2)

    #if both player and dealer have blackjack
    if playerHands[1].blackjack and dealerH.blackjack:
        # data['playerBJs'] += 1
        # data['dealerBJs'] += 1
        # data['pushes'] += 1
        balance += playerHands[1].wager
        balancebanner = font.render(f'Balance: {balance}', True, white)
        text = font.render('Both you and the dealer have blackjack. What are the odds?', True, white)
        win.fill(black)
        win.blit(balancebanner, (850, 20))
        win.blit(text, (300, 300))
        pygame.display.flip()
        time.sleep(2)
        restarter()
        continue

    #if just the player has blackjack
    if playerHands[1].blackjack and not dealerH.blackjack:
        # data['playerBJs'] += 1
        # data['wins'] += 1
        balance += int((playerHands[1].wager * 2.5))
        balancebanner = font.render(f'Balance: {balance}', True, white)
        text = font.render('You have blackjack. Big money!', True, white)
        win.fill(black)
        win.blit(balancebanner, (850, 20))
        win.blit(text, (300, 300))
        pygame.display.flip()
        time.sleep(2)
        restarter()
        continue

    #if the dealer is showing an ace, ask about insurance
    w = 0
    while w == 0 and dealerH[0].rank == 'Ace' and not playerHands[1].blackjack:
        insurance = int(playerHands[1].wager / 2)
        if insurance <= balance:
            yesbutton = Button(600, 600, 150, 100, green, 'yes')
            nobutton = Button(750, 600, 150, 100, green, 'no')
            while True:
                text1 = font.render('The dealer is showing an ace, would you like to buy insurance?', True, white)
                text2 = font.render(f'It is half the amount of your original bet, so {insurance}. (yes or no)', True, white)
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if yesbutton.isOver(pos):
                            print('success')
                        if nobutton.isOver(pos):
                            print('not success')
                    if event.type == pygame.MOUSEMOTION:
                        if yesbutton.isOver(pos):
                            yesbutton.color = white
                        else:
                            yesbutton.color = green
                        if nobutton.isOver(pos):
                            nobutton.color = white
                        else:
                            nobutton.color = green
                    # if response is not None:
                    #     if response == 'yes':
                    #         # data['ibets taken'] += 1
                    #         balance -= insurance
                    #         if dealerH.blackjack:
                    #             # data['dealerBJs'] += 1
                    #             # data['losses'] += 1
                    #             # data['ibets won'] += 1
                    #             balance += insurance * 3
                    #             print(f'The dealer\'s other card is the {dealerH[1].rank} of {dealerH[1].suit} and therefore they have blackjack, but you won the insurance bet. Well done, {name}.')
                    #             playerHands[1].done = True
                    #             break
                    #         else:
                    #             # data['ibets lost'] += 1
                    #             print('The dealer does not have blackjack, so you lost the insurance bet. But, the hand continues.')
                    #             break
                    #     elif response == 'no':
                    #         if dealerH.blackjack:
                    #             # data['dealerBJs'] += 1
                    #             # data['losses'] += 1
                    #             # data['ibets missed'] += 1
                    #             print(f'The dealer\'s other card is the {dealerH[1].rank} of {dealerH[1].suit} and therefore they have blackjack. Tough luck old chap')
                    #             playerHands[1].done = True
                    #             break
                    #         else:
                    #             # data['ibets avoided'] += 1
                    #             print('The dealer does not have blackjack. The hand continues.')
                    #             break
                    #     else:
                    #         print('Please respond yes or no.')
                    #         response = None
                win.fill(black)
                nobutton.draw(win,white)
                yesbutton.draw(win, white)
                win.blit(text1, (400, 300))
                win.blit(text2, (400, 330))
                pygame.display.flip()
                clock.tick(30)
        else:
            print('The dealer is showing an ace, but you do not have enough funds to buy insurance.')
            if dealerH.blackjack:
                # data['dealerBJs'] += 1
                # data['losses'] += 1
                print(f'The dealer\'s other card is the {dealerH[1].rank} of {dealerH[1].suit} and therefore they have blackjack. Tough luck old chap')
                playerHands[1].done = True
                break
            else:
                print('The dealer does not have blackjack. The hand continues.')
                break

    #restart if game is done
    if endCheck(playerHands) == True:
        restarter()
        continue
    #
    # #if the dealer has hidden blackjack
    # if dealerH.blackjack:
    #     data['losses'] += 1
    #     data['dealerBJs'] += 1
    #     print('The dealer\'s facedown card is an ace and therefore they have blackjack. Tough luck.')
    #     restarter()
    #     continue
    #
    #establish options for the player's action
    options = ['hit', 'stand', 'double down']
    #
    # # loop through player actions
    # while True:
    #     playerHandsCopy = playerHands.copy()
    #     for i, hand in playerHandsCopy.items():
    #         if hand.bust == True or hand.stand == True:
    #             continue
    #         hand.done = playeraction(i, hand)
    #         playerHands[i] = playerHandsCopy[i]
    #     count = 0
    #     for hand in playerHands.values():
    #         if hand.bust == True or hand.stand == True:
    #             count +=1
    #     if count == len(playerHands):
    #         break
    #
    # #restart if the game is done
    # if endCheck(playerHands) == True:
    #     restarter()
    #     continue
    #
    # #reveal the dealer's other card
    # print(f'The dealer\'s other card is the {dealerH[1].rank} of {dealerH[1].suit} for a total of {dealerH.value}.')
    #
    # #check the dealer's result and draw cards if necessary
    # while True:
    #     if dealerH.bust:
    #         data['dealer busts'] += 1
    #         for hand in playerHands.values():
    #             if hand.done == False:
    #                 data['wins'] += 1
    #                 balance += hand.wager * 2
    #         print(f'The dealer has busted. {name} wins!')
    #         dealerH.done = True
    #         break
    #     elif (dealerH.value <= 21) and (dealerH.value >= 17):
    #         break
    #     else:
    #         assert dealerH.value < 17
    #         hit(dealerH.cards)
    #         print(f'The dealer draws the {dealerH[-1].rank} of {dealerH[-1].suit}. The dealer now has {dealerH.value}.')
    #
    # #restart if the game is done
    # if endCheck(playerHands) == True:
    #     restarter()
    #     continue
    #
    # #if neither have busted, compare results
    # for i, hand in playerHands.items():
    #     if hand.bust == False:
    #         if len(playerHands) != 1 :
    #             print(f'For hand number #{i}:')
    #         if hand.value > dealerH.value:
    #             balance += hand.wager * 2
    #             data['wins'] += 1
    #             print(f'You have beaten the dealer with a hand of {hand.value} vs. their {dealerH.value}. Congratulations!')
    #         elif hand.value < dealerH.value:
    #             data['losses'] += 1
    #             print(f'The dealer has beaten you with a hand of {dealerH.value} vs. your {hand.value}. Better luck next time.')
    #         else:
    #             assert hand.value == dealerH.value
    #             balance += hand.wager
    #             data['pushes'] += 1
    #             print(f'You and the dealer both have {hand.value}. The hand is a push.')
    #         hand.done = True
    #
    # for hand in playerHands.values():
    #     assert hand.done
    restarter()
    continue