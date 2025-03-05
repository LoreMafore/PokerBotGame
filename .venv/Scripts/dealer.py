"""

Made By Conrad Mercer 3/3/2025

"""
import random
from Card import Cards
from Player import Players


class Dealer():
    deck_of_cards = []
    discard_pile = []

    def __init__(self, num_of_players):
        self.player_list = num_of_players

    def _update(self):
        pass

    def _cards(self):
        # Inialize the card deck
        for card_suit in Cards.SUITS:
            for card_type in Cards.TYPE:
                deck_of_cards.append(Cards(card_type, card_suit))

    def _dealing(self):
        increament = 0
        while increament != player_list:
            Players.player_hand.append(deck_of_cards[0])
            deck_of_cards[0].pop






    def _play_on_board(self):
        pass