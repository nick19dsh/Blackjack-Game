# Import and Global variables

import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}

playing = True

# Create Card class


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


# Create Deck class


class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


# Create Hand class


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


# Create Chip class


class Chips:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Function for taking bets


def take_bet(chips):

    while True:

        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry, a bet must be an integer ")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, you do not have enough chips! You have: {chips.total}")
            else:
                break


# Function for taking hits


def hit(deck, hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()


# Function for prompting the player to hit or stand


def hit_or_stand(deck, hand):

    global playing  # to control an upcoming while loop

    while True:

        x = input("Would you like to Hit or Stand? enter 'h' or 's': ")

        if x[0].lower() == "h":
            hit(deck, hand)
        elif x[0].lower() == "s":
            print("Player stands, Dealer is playing.")
            playing = False
        else:
            print("Sorry, Please try again. ")
            continue
        break


# Functions to display the cards


def show_some(player, dealer):

    print("\nDealer's Hand:")
    print("First card hidden")
    print(dealer.cards[1])
    print("\nPlayer' Hand:", *player.cards, sep="\n")


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep="\n")
    print(f"Value of Dealer's Hand is {dealer.value}")
    print("\nPlayer's Hand:", *player.cards, sep="\n")
    print(f"Value of Player's Hand is {player.value}")


# Functions to handle end of game scenarios


def player_busts(chips):
    print("BUST PLAYER")
    chips.lose_bet()


def player_wins(chips):
    print("PLAYER WINS!")
    chips.win_bet()


def dealer_busts(chips):
    print("PLAYER WINS! DEALER BUSTED!")
    chips.win_bet()


def dealer_wins(chips):
    print("DEALER WINS")
    chips.lose_bet()


def push():
    print("Dealer and Player TIE! PUSH")


# PLAYING THE GAME

while True:

    # Print an opening statement
    print("WELCOME TO BLACKJACK")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips

    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop

        if player_hand.value > 21:
            player_busts(player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 21
    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios

        if dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()

    # Inform Player of their chips total
    print("\n Player total chips are at {}".format(player_chips.total))

    # Ask to play again
    new_game = input("Would you like to play another game? y/n: ")

    if new_game[0].lower() == "y":
        playing = True
        continue
    else:
        print("Thank you for playing")
        break
