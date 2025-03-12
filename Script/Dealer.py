"""

Made By Conrad Mercer 3/3/2025

"""
import random

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

        names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia"]

        # Create the players with an initial money amount
        for i in range(num_of_players):
            self.player_list.append(Players(initial_money=1000, name=names[i]))

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
        if flop_counter < 3:
            # burn a card
            self.discard_pile.append(self.deck_of_cards.pop(0))

            for i in range(3):
                self.flop.append(self.deck_of_cards.pop(0))
                self.flop[i]._set_position(100*i, 400)
                self.flop[i].is_showing_card = True

            print("Flop cards:", [str(card) for card in self.flop])
            return False, 3

        # dealers play 4th card
        if flop_counter == 3:
            # burn a card
            self.discard_pile.append(self.deck_of_cards.pop(0))

            self.flop.append(self.deck_of_cards.pop(0))

            print("Flop cards:", [str(card) for card in self.flop])
            return False, 4

        # dealers play 5th card
        if flop_counter == 4:
            # burn a card
            self.discard_pile.append(self.deck_of_cards.pop(0))

            self.flop.append(self.deck_of_cards.pop(0))

            print("Flop cards:", [str(card) for card in self.flop])
            return True, 0
        pass

    def get_card_value(self, card):
        """Convert card type to numerical value for comparison."""
        # Handle Ace high
        if card.type == 0:  # Ace
            return 14
        return card.type + 1

    def get_hand_strength(self, hand):
        """Calculate the strength of a hand and return a tuple for comparison."""
        # Count occurrences of each card type
        type_counts = {}
        for card in hand:
            type_counts[card.type] = type_counts.get(card.type, 0) + 1

        # Check if all cards are of the same suit (flush)
        same_suit = len(set(card.suit for card in hand)) == 1

        # Sort cards by value for checking sequences
        sorted_values = sorted([self.get_card_value(card) for card in hand])

        # Check for straight
        is_straight = False
        # Handle the case of A-5 straight
        if sorted_values == [2, 3, 4, 5, 14]:
            is_straight = True
            # For A-5 straight, Ace is treated as 1
            sorted_values = [1, 2, 3, 4, 5]
        else:
            # Regular straight check
            is_straight = all(sorted_values[i + 1] - sorted_values[i] == 1 for i in range(len(sorted_values) - 1))

        # Straight flush
        if is_straight and same_suit:
            return (8, sorted_values)

        # Four of a kind
        if 4 in type_counts.values():
            four_kind_value = [t for t, count in type_counts.items() if count == 4][0]
            four_kind_value = 14 if four_kind_value == 0 else four_kind_value + 1
            kicker = [t for t, count in type_counts.items() if count == 1][0]
            kicker = 14 if kicker == 0 else kicker + 1
            return (7, four_kind_value, kicker)

        # Full house
        if 3 in type_counts.values() and 2 in type_counts.values():
            three_kind_value = [t for t, count in type_counts.items() if count == 3][0]
            three_kind_value = 14 if three_kind_value == 0 else three_kind_value + 1
            pair_value = [t for t, count in type_counts.items() if count == 2][0]
            pair_value = 14 if pair_value == 0 else pair_value + 1
            return (6, three_kind_value, pair_value)

        # Flush
        if same_suit:
            return (5, sorted_values)

        # Straight
        if is_straight:
            return (4, sorted_values)

        # Three of a kind
        if 3 in type_counts.values():
            three_kind_value = [t for t, count in type_counts.items() if count == 3][0]
            three_kind_value = 14 if three_kind_value == 0 else three_kind_value + 1
            kickers = sorted([14 if t == 0 else t + 1 for t, count in type_counts.items() if count == 1], reverse=True)
            return (3, three_kind_value, kickers)

        # Two pair
        if list(type_counts.values()).count(2) == 2:
            pairs = sorted([14 if t == 0 else t + 1 for t, count in type_counts.items() if count == 2], reverse=True)
            kicker = [14 if t == 0 else t + 1 for t, count in type_counts.items() if count == 1][0]
            return (2, pairs, kicker)

        # One pair
        if 2 in type_counts.values():
            pair_value = [t for t, count in type_counts.items() if count == 2][0]
            pair_value = 14 if pair_value == 0 else pair_value + 1
            kickers = sorted([14 if t == 0 else t + 1 for t, count in type_counts.items() if count == 1], reverse=True)
            return (1, pair_value, kickers)

        # High card
        return (0, sorted_values[::-1])  # Reversed for high-to-low comparison

    # Hand rankings (from highest to lowest)
    # 8: Straight Flush, 7: Four of a Kind, 6: Full House, 5: Flush,
    # 4: Straight, 3: Three of a Kind, 2: Two Pair, 1: One Pair, 0: High Card
    def _check_winner(self):

        players = [player for player in self.player_list if len(player.player_hand) > 0 and not player.fold_bool]

        # Calculate strength for each player's hand
        player_strengths = [(player, self.get_hand_strength(player.player_hand)) for player in players]

        # Sort players based on hand strength (strongest first)
        sorted_players = [player for player, _ in sorted(player_strengths, key=lambda x: x[1], reverse=True)]

        return sorted_players[0]

    def _eval_hand(self, hand):
        # Return ranking: high card = 0, ... royal flush = 9
        # Also return high card(s) of rank

        # TODO this is still broken

        values = sorted([c[0] for c in hand])
        suits = [c[1] for c in hand]

        # Check for straight
        is_straight = True
        for i in range(1, len(values)):
            if values[i] != values[i - 1] + 1:
                is_straight = False
                break

        # Special case for A-5 straight
        if values == [2, 3, 4, 5, 14]:
            is_straight = True
            values[4] = 5  # Consider Ace as 5 for this straight

        # Check for flush
        is_flush = all(s == suits[0] for s in suits)

        # Royal flush and straight flush
        if is_straight and is_flush:
            if values[0] == 10 and values[4] == 14:  # 10, J, Q, K, A
                return 9, None  # Royal flush
            else:
                return 8, max(values)  # Straight flush

        # Count occurrences of each value
        value_counts = {}
        for v in values:
            if v in value_counts:
                value_counts[v] += 1
            else:
                value_counts[v] = 1

        # Four of a kind
        for v, count in value_counts.items():
            if count == 4:
                return 7, v

        # Full house
        three_value = None
        pair_value = None
        for v, count in value_counts.items():
            if count == 3:
                three_value = v
            elif count == 2:
                pair_value = v

        if three_value is not None and pair_value is not None:
            return 6, (three_value, pair_value)

        # Flush
        if is_flush:
            return 5, None

        # Straight
        if is_straight:
            return 4, max(values)

        # Three of a kind
        if three_value is not None:
            return 3, three_value

        # Two pair
        pairs = [v for v, count in value_counts.items() if count == 2]
        if len(pairs) == 2:
            return 2, sorted(pairs, reverse=True)

        # One pair
        if len(pairs) == 1:
            return 1, pairs[0]

        # High card
        return 0, max(values)

    def _tiebreaker(self, hand1, hand2, hand1_info, hand2_info):
        # Return True if hand1 wins, False if hand2 wins

        # If hand_info is available and comparable
        if isinstance(hand1_info, int) and isinstance(hand2_info, int):
            if hand1_info != hand2_info:
                return hand1_info > hand2_info

        # For pairs and other specific hand types
        if isinstance(hand1_info, tuple) and isinstance(hand2_info, tuple):
            if hand1_info[0] != hand2_info[0]:
                return hand1_info[0] > hand2_info[0]
            if len(hand1_info) > 1 and hand1_info[1] != hand2_info[1]:
                return hand1_info[1] > hand2_info[1]

        # For two pairs
        if isinstance(hand1_info, list) and isinstance(hand2_info, list):
            # Compare highest pair first
            for i in range(min(len(hand1_info), len(hand2_info))):
                if hand1_info[i] != hand2_info[i]:
                    return hand1_info[i] > hand2_info[i]

        # If we get here, compare cards from highest to lowest
        values1 = sorted([c[0] for c in hand1], reverse=True)
        values2 = sorted([c[0] for c in hand2], reverse=True)

        for i in range(min(len(values1), len(values2))):
            if values1[i] != values2[i]:
                return values1[i] > values2[i]

        # If everything is equal, it's a tie (returns True for hand1)
        return True
