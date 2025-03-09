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

    #TODO ADD display cards here and burning cards
    def _play_on_board(self, flop_counter):
        #dealers plays first 3 cards on boards

        print(f"Flop counter: {flop_counter}")
        if flop_counter < 3:
            #burn a card
            self.discard_pile.append(self.deck_of_cards.append(0))

            for i in range(3):
                self.flop.append(self.deck_of_cards.pop(0))

            print("Flop cards:", [str(card) for card in self.flop])
            return False, 3

        #dealers play 4th card
        if flop_counter == 3:
            #burn a card
            self.discard_pile.append(self.deck_of_cards.append(0))

            self.flop.append(self.deck_of_cards.pop(0))

            print("Flop cards:", [str(card) for card in self.flop])
            return False, 4

        #dealers play 5th card
        if flop_counter == 4:
            #burn a card
            self.discard_pile.append(self.deck_of_cards.append(0))

            self.flop.append(self.deck_of_cards.pop(0))

            print("Flop cards:", [str(card) for card in self.flop])
            return True, 0
        pass

    #I pulled this to the end from the internet
    def _check_winner(self):
        # Map for card values from your Cards class values to the evaluation values
        value_dict = {0: 14, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13}

        # List to store each player's cards and community cards
        player_hands = []
        for player in self.player_list:
            if not player.fold_bool:  # Only consider players who haven't folded
                # Combine player's hand with community cards
                full_hand = player.player_hand + self.flop
                # Convert to format needed for evaluation
                converted_hand = [(value_dict[card.type], card.suit) for card in full_hand]
                player_hands.append((player, converted_hand))

        if not player_hands:  # No active players
            return None

        # Evaluate each player's hand
        best_rank = -1
        best_players = []

        for player, hand in player_hands:
            # Only evaluate the best 5 cards
            hand_combinations = self._get_best_hand(hand)
            hand_rank, hand_info = self._eval_hand(hand_combinations)

            print(f"Player hand: {[str(card) for card in player.player_hand]}, Rank: {hand_rank}, Info: {hand_info}")

            if hand_rank > best_rank:
                best_rank = hand_rank
                best_players = [(player, hand_combinations, hand_info)]
            elif hand_rank == best_rank:
                best_players.append((player, hand_combinations, hand_info))

        # If only one player has the best hand
        if len(best_players) == 1:
            winner = best_players[0][0]
            return winner

        # Break ties
        if len(best_players) > 1:
            best_so_far = best_players[0]
            for i in range(1, len(best_players)):
                if self._tiebreaker(best_so_far[1], best_players[i][1], best_so_far[2], best_players[i][2]):
                    continue
                else:
                    best_so_far = best_players[i]

            return best_so_far[0]  # Return the winning player

    def _get_best_hand(self, hand):
        # For now, just return the 5 highest cards
        # In a full implementation, you would check all possible 5-card combinations
        # from the 7 cards (player's 2 + community 5) and return the best one
        return sorted(hand, key=lambda x: x[0], reverse=True)[:5]

    def _eval_hand(self, hand):
        # Return ranking: high card = 0, ... royal flush = 9
        # Also return high card(s) of rank

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