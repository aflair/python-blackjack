import random

# Initiate global variabes used for defining cards and their values
suits = ('Clubs','Diamonds','Hearts','Spades')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

class Card():
    '''
    Class Object used to define a playing card, holding the rank and suit.
    Value is assigned as needed, using the 'values' global variable
    '''
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck():
    '''
    Class Object used to define a deck of playing cards. Starting at the standard
    52 number of cards. Uses attribute 'count' to determine how many cards are in
    the deck.
    '''
    def __init__(self):
        self.cards = []
        self.count = 52
        # Initiate unshuffled deck
        for x in suits:
            for y in ranks:
                self.cards.append(Card(y,x))

    def shuffleCards(self):
        try:
            random.shuffle(self.cards)
        except:
            print('Error shuffling cards')

    def drawCard(self):
        if self.count > 0:
            self.count -= 1
            return self.cards.pop()
        else:
            print('Not enough cards, grabbing new deck.')
            self.__init__()
            self.shuffleCards()
            self.count -= 1
            return self.cards.pop()

    def __len__(self):
        return self.count

    def __str__(self):
        '''
        Primarily used to print the deck.
        '''
        deck_string = ''
        for x in range(self.count):
            deck_string += str(self.cards[x]) + '\n'
        return deck_string

class Hand():

    def __init__(self):
        self.cards = []
        self.value = 0
        self.num_aces = 0

    def adjustForAce(self):

        # Check if we have aces at all, if none skip logic
        if self.num_aces != 0:
            # Recalculate total value
            self.value = 0
            for card in self.cards:
                self.value += values[card.rank]
            
            x = self.num_aces
            # Run a while loop to decrease value of aces until value is under 21
            # This also checks if the value is under 21 despite having an ace
            while x > 0 and self.value > 21:
                self.value -= 10
                x -= 1
        print('Adjusted for ace(s).')

    def addCard(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.num_aces += 1

        if self.value > 21 and self.num_aces > 0:
            self.adjustForAce()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        handString = ''
        for card in self.cards:
            handString += str(card) + '\n'
        return handString

class Chips:
    def __init__(self,total=100):
        self.total = total
        self.bet = 0

    # When player wins, add double bet to total and reset bet
    def winBet(self):
        self.total += self.bet * 2
        self.bet = 0

    # When player loses, reset the bet (total was already reduced)
    def loseBet(self):
        self.bet = 0
    
    # When player ties, add the bet back to total and reset bet
    def tieBet(self):
        self.total += self.bet
        self.bet = 0

def take_bet(chips):
    '''
    Assumes player has a positive chip count, otherwise game would be over
    '''
    print(f'\nYou have {chips.total} chips to bet.')
    while True:
        try:
            amount = int(input('How many chips would you like to bet? '))
        except:
            print('Please input a valid chip count.')
            continue
        else:
            # Check if they bet more than they have
            if amount > chips.total:
                print(f'Insufficient chips to bet {amount}')
                continue
            else:
                chips.bet = amount
                chips.total -= amount
                print(f'You bet {chips.bet} chips. New total is {chips.total}')
                break

def show_cards(dealer, player, show_dealer):
    # Print Dealer Hand First
    if show_dealer:
        print(f'\n\n----------\nDealer: ({dealer.value})')
    else:
        print('\n\n----------\nDealer: (?)')
    for x in range(len(dealer)):
        if x == 0 and not show_dealer:
            print('Hidden Card')
        else:
            print(dealer.cards[x].rank + ' of ' + dealer.cards[x].suit)

    print(f'\nYou: ({player.value})')
    for y in range(len(player)):
        print(player.cards[y].rank + ' of ' + player.cards[y].suit)
    print('----------\n')

def reset_hand(dealer, player):
    dealer.__init__()
    player.__init__()


#############################################
############################################# 
############################################# 

if __name__ == "__main__":
    
    # Initiate the game state boolean global variable
    play_again = True
    
    ############################################# 
    ################ Begin Game #################
    #############################################
    while play_again:

        # Print welcome message
        print("\n------------------------------------------")
        print("Welcome to Andrew Flair's Black Jack game.")
        print("------------------------------------------\n")

        # Ask how many chips user would like to play with.
        while True:
            try:
                starting_chip_amt = int(input('How many chips would you like to play with? '))
            except TypeError:
                print('Please enter a valid positive integer.')
                continue
            except:
                print('Error, please try again.')
                continue
            else:
                break

        # Create and shuffle game deck
        game_deck = Deck()
        game_deck.shuffleCards()

        # Create player chips and player/dealer hands
        player_chips = Chips(starting_chip_amt)
        player_hand = Hand()
        dealer_hand = Hand()

        # Prompt player for initial bet
        take_bet(player_chips)

        # Deal two cards to player and dealer
        for x in range(2):
            player_hand.addCard(game_deck.drawCard())
            dealer_hand.addCard(game_deck.drawCard())

        # Show initial cards
        show_cards(dealer_hand, player_hand, False)

        ############################################# 
        ############# Begin Round Loop ##############
        #############################################
        playing = True
        while playing:
            bust = False
            # Player turn hit/stand loop
            while True:
                # Hit or stand
                hit_or_stand = ''
                while hit_or_stand not in ['hit','stand']:
                    hit_or_stand = input('Would you like to hit or stand? [hit/stand]').lower()
                
                if hit_or_stand == 'hit':
                    player_hand.addCard(game_deck.drawCard())
                else:
                    break

                # Show the cards, still dealer hidden
                show_cards(dealer_hand, player_hand, False)

                # Check for player bust
                if player_hand.value > 21:
                    print('Ouch, you busted!')
                    print(f'You lost {player_chips.bet} chips.')
                    player_chips.loseBet()
                    bust = True
                    break

            # Player hasn't busted. Dealer's turn.
            if bust == False:
                show_cards(dealer_hand, player_hand, True)

                # Dealer hits until at least 17 or they win
                while dealer_hand.value < 17 and dealer_hand.value < player_hand.value:
                    dealer_hand.addCard(game_deck.drawCard())

                show_cards(dealer_hand, player_hand, True)

                # Check for dealer bust
                if dealer_hand.value > 21:
                    print('Dealer busted!')
                    print(f'You win {player_chips.bet} chips.')
                    player_chips.winBet()
                # Dealer didn't bust and has more than you
                elif dealer_hand.value > player_hand.value:
                    print('Dealer wins...')
                    print(f'You lost {player_chips.bet} chips.')
                    player_chips.loseBet()
                # Push (tie), reset bet
                elif dealer_hand.value == player_hand.value:
                    print('Push...\n Resetting chips.')
                    player_chips.tieBet()
                # Otherwise you have won
                else:
                    print(f'You win {player_chips.bet} chips.')
                    player_chips.winBet()

            #############################################
            ############### End of round ################
            #############################################

            print(f'Chip total = {player_chips.total}')
            
            # Player is out of chips, end current game
            if player_chips.total == 0:
                print('Sorry... you are out of chips. Better luck next time!')
                playing = False
            # Player has chips remaining
            else:
                # Ask if they want to play another round with their current chips
                new_round = ''
                while new_round not in ['y','n']:
                    new_round = input('Play another round? [y/n]')
                if new_round == 'n':
                    playing = False
                else:
                    # Deal New Cards
                    reset_hand(dealer_hand, player_hand)
                    for x in range(2):
                        dealer_hand.addCard(game_deck.drawCard())
                        player_hand.addCard(game_deck.drawCard())
                    # Ask for bet
                    take_bet(player_chips)
                    # Show cards
                    show_cards(dealer_hand, player_hand, False)

        #############################################
        ############### End of game #################
        #############################################

        # Check if they want to play a new game
        play_again_answer = ''
        while play_again_answer not in ['y','n']:
            play_again_answer = input('Do you wish to play a new game? [y/n]').lower()
        if play_again_answer == 'y':
            continue
        else:
            print('Goodbye!')
            break