import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:

    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        text = ''
        for card in self.cards:
            text += str(card) + '\n'
        return text

    def drawCard(self):
        return self.cards.pop()

class Chips:

    def __init__(self, chips=100):
        self.chips = chips
        self.bet = 0

    def winBet(self):
        self.chips += self.bet

    def loseBet(self):
        self.chips -= self.bet

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0

    def addCard(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

    def __str__(self):
        text = ''
        for card in self.cards:
            text += str(card) + '\n'
        return text

def show_some(dealer_hand, player_hand):
    print("\nDealer's hand:")
    print('<hidden card>')
    print(dealer_hand.cards[1])
    print("\nPlayer's hand:")
    print(player_hand.cards[0])
    print(player_hand.cards[1])
    print('')

def show_all(dealer_hand, player_hand):
    print("\nDealer's hand:")
    for card in dealer_hand.cards:
        print(card)
    print("\nPlayer's hand:")
    for card in player_hand.cards:
        print(card)
    print('\n')

def askPlayerForBet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips do you want to bet?\n'))
        except ValueError:
            print('Please input a valid number')
        else:
            if chips.bet > chips.chips:
                print(f'Not enough chips to bet. You have {chips.chips}')
                continue
            else:
                break

    return chips

def askHitOrPass():
    while True:
        answer = input('Do you want to hit or pass? Press "h" for hit or "p" for pass\n')
        if answer.lower() == 'h':
            return True
        elif answer.lower() == 'p':
            return False

def playerWins(player_chips):
    global playing
    player_chips.winBet()
    print('Player Won!')
    playing = False

def playerBusts(player_chips):
    global playing
    player_chips.loseBet()
    print('Player Busts!')
    playing = False

def dealerWins(player_chips):
    global playing
    player_chips.loseBet()
    print('Dealer Won!')
    playing = False

def dealerBusts(player_chips):
    global playing
    player_chips.winBet()
    print('Dealer Busts!')
    playing = False

def askReplay():
    while True:
        answer = input('Do you want to play again? Write "y" for yes or "n" for no\n')
        if answer.lower() == 'y':
            return True
        elif answer.lower() == 'n':
            return False

while True:

    print('\nWelcome to Blackjack game')

    deck = Deck()
    deck.shuffle()

    # Initialize player hand
    player_hand = Hand()
    player_hand.addCard(deck.drawCard())
    player_hand.addCard(deck.drawCard())

    # Initialize dealer hand
    dealer_hand = Hand()
    dealer_hand.addCard(deck.drawCard())
    dealer_hand.addCard(deck.drawCard())

    # Initialize player chips
    player_chips = Chips()

    askPlayerForBet(player_chips)

    show_some(dealer_hand, player_hand)

    while askHitOrPass():
        player_hand.addCard(deck.drawCard())
        print(player_hand)
        if player_hand.value == 21:
            playerWins(player_chips)
            break
        elif player_hand.value > 21:
            playerBusts(player_chips)
            break

    while dealer_hand.value < 17 and playing:
        dealer_hand.addCard(deck.drawCard())

    while playing:
        if dealer_hand.value == 21:
            dealerWins(player_chips)
        elif dealer_hand.value > 21:
            dealerBusts(player_chips)
        elif dealer_hand.value < 21 and (dealer_hand.value > player_hand.value):
            dealerWins(player_chips)
        elif dealer_hand.value < 21 and (dealer_hand.value < player_hand.value):
            playerWins(player_chips)

    print(f'Player winnings: {player_chips.chips}')

    if not askReplay():
        break
