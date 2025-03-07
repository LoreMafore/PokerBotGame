"""

Made By Conrad Mercer 3/3/2025

"""
import random

from samba.provision.common import setup_ldb

from Card import Cards
from Player import Players

class Dealer():
    def __init__(self, num_of_players):
        self.player_list = []
        self.deck_of_cards = []
        self.discard_pile = []
        self.flop = []

        # Initialize the deck
        self._cards()

        # Create the players with an initial money amount
        for i in range(num_of_players):
            self.player_list.append(Players(initial_money=1000))

    def _update(self):
        pass

    def _cards(self):
        # Initialize the card deck
        for card_suit in Cards.SUITS:
            for card_type in Cards.TYPE:
                self.deck_of_cards.append(Cards(card_type, card_suit))

    def _dealing(self):
        for player in self.player_list:
            cards = 0
            while cards != 2:
                player.player_hand.append(self.deck_of_cards[0])
                self.deck_of_cards.pop(0)  # Remove the card from the deck
                cards += 1

    def shuffle_deck(self):
        random.shuffle(self.deck_of_cards)


    def _play_on_board(self, flop_counter):
        #dealers plays first 3 cards on boards
        while(flop_counter < 3):
            self.flop.append(self.deck_of_cards[0])
            self.deck_of_cards.pop(0)  # Remove the card from the deck
            flop_counter += 1
            if flop_counter == 3:
                return 
        #dealers play 4th card
        if flop_counter == 3:
            self.flop.append(self.deck_of_cards[0])
            self.deck_of_cards.pop(0)  # Remove the card from the deck
            flop_counter += 1
            return

        #dealers play 5th card
        if flop_counter == 4:
            self.flop.append(self.deck_of_cards[0])
            self.deck_of_cards.pop(0)  # Remove the card from the deck
            flop_counter *= 0
            return
        pass

    def _check_winner(self):
        pass