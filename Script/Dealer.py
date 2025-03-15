"""

Made By Conrad Mercer 3/3/2025

"""
import random

import pygame

from Card import Cards
from Player import Players


class Dealer():
    def __init__(self, num_of_players):
        self.player_list = []
        self.deck_of_cards = []
        self.discard_pile = []
        self.flop = []
        self.num_of_players = num_of_players

        # Initialize the deck
        self._cards()

        # TODO FILL OUT NAMES HERE
        names = ["Connor", "Colllin", "Isaac", "Thomas", "Kolbe", "Tobin", "Mark", "///", "---", "..."]

        # Create the players with an initial money amount
        for i in range(num_of_players):
            self.player_list.append(Players(initial_money=1000, name=names[i], dealer=self))

    def _update(self):
        pass

    def _cards(self):
        # Initialize the card deck
        for card_suit in Cards.SUITS:
            for card_type in Cards.TYPE:
                self.deck_of_cards.append(Cards(card_type, card_suit))

    # Deals cards to all the players in the game
    def _dealing(self):
        for i, player in enumerate(self.player_list):
            cards = 0
            while cards != 2:
                player.player_hand.append(self.deck_of_cards[0])
                self.deck_of_cards.pop(0)  # Remove the card from the deck
                cards += 1
            player._hand(i)

    def shuffle_deck(self):
        random.shuffle(self.deck_of_cards)

    # TODO ADD display cards here and burning cards
    def _play_on_board(self, flop_counter):
        # dealers plays first 3 cards on boards
        print(f"Flop counter: {flop_counter}")
        x_pos = 1920 // 2 + 300
        y_pos = 1080 // 2 - 50

        padding = 10
        cw = 62  # Card width
        discard_x = x_pos - (62 + (5 + 62)) * 6

        # Pre-flop (first 3 cards)
        if flop_counter < 3:
            # burn a card
            self.deck_of_cards[0]._set_position(discard_x, y_pos)
            self.discard_pile.append(self.deck_of_cards.pop(0))

            # Make sure flop array is clear
            self.flop = []

            for i in range(3):
                x_pos -= (62 + (i + 62))

                # Add new card from the deck
                new_card = self.deck_of_cards.pop(0)
                new_card._set_position(x_pos, y_pos)
                new_card.is_showing_card = True  # Ensure card is shown face up
                new_card._load_sprite(True)  # Force load face-up sprite
                self.flop.append(new_card)

            print("Flop cards:", [str(card) for card in self.flop])
            return False, 3

        # Turn (4th card)
        if flop_counter == 3:
            # burn a card
            self.deck_of_cards[0]._set_position(discard_x, y_pos)
            self.discard_pile.append(self.deck_of_cards.pop(0))

            # Add 4th card
            new_card = self.deck_of_cards.pop(0)
            new_card._set_position(x_pos - (62 + (3 + 62)) * 4, y_pos)
            new_card.is_showing_card = True  # Ensure card is shown face up
            new_card._load_sprite(True)  # Force load face-up sprite
            self.flop.append(new_card)

            print("Turn card:", str(self.flop[-1]))
            return False, 4

        # River (5th card)
        if flop_counter == 4:
            # burn a card
            self.deck_of_cards[0]._set_position(discard_x, y_pos)
            self.discard_pile.append(self.deck_of_cards.pop(0))

            # Add 5th card
            new_card = self.deck_of_cards.pop(0)
            new_card._set_position(x_pos - (62 + (4 + 62)) * 5, y_pos)
            new_card.is_showing_card = True  # Ensure card is shown face up
            new_card._load_sprite(True)  # Force load face-up sprite
            self.flop.append(new_card)

            print("River card:", str(self.flop[-1]))
            return True, 0

    # New manual winner selection function
    def _check_winner(self):
        """Allows manual selection of the winner through command line input"""
        active_players = [player for player in self.player_list if not player.fold_bool]

        if not active_players:
            print("No active players remaining!")
            return None

        # If only one player remains, they're the winner
        if len(active_players) == 1:
            print(f"{active_players[0].name} is the only player remaining - automatic winner!")
            return active_players[0]

        # Show all active players and their hands
        print("\n=== SHOWDOWN - SELECT WINNER ===")

        print(f"Community cards: {[str(card) for card in self.flop]}")

        for i, player in enumerate(active_players):
            print(f"{i + 1}: {player.name} with hand: {[str(card) for card in player.player_hand]}")

        # Get user input for winner
        while True:
            try:
                choice = int(input(f"Enter the number (1-{len(active_players)}) of the winning player: "))
                if 1 <= choice <= len(active_players):
                    winner = active_players[choice - 1]
                    print(f"{winner.name} selected as the winner!")
                    return winner
                else:
                    print(f"Please enter a number between 1 and {len(active_players)}")
            except ValueError:
                print("Please enter a valid number")
