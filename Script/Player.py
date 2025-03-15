"""
Made By Conrad Mercer 3/3/2025
"""

import math
import random

import Card

import pygame.math


class Players():

    # maybe a total bet needs to be added rn there is one in the main function
    # but maybe i want to implement it here

    def __init__(self, initial_money, name, dealer=None):
        self.money = initial_money
        self.player_hand = []
        self.player_position = []
        self.player_rotation = []
        self.player_turn = False
        self.bet = 0
        self.fold_bool = False
        self.all_in_bool = False
        self.have_bet = False
        self.name = name
        self.dealer = dealer
        # self.font = pygame.font.Font('../fonts/PixelOperator8.ttf', 24)

    def _update(self, big_blind_pos, small_blind_pos):
        # will check the position the big_blind and small_blind in relative to the player
        pass

    def _positions(self, player_index):

        table_center_x = 1920 / 2
        table_center_y = 1080 / 2

        # Oval dimensions - these may not be right
        a = 750  # Horizontal radius
        b = 350

        total_players = self.dealer.num_of_players
        angle = 2 * math.pi * (player_index / total_players)

        # Calculate position for this player
        player_x = table_center_x + a * math.cos(angle)
        player_y = table_center_y + b * math.sin(angle)

        # offset by card width / height
        player_x -= (96 // 2)
        player_y -= (144 // 2)

        return player_x, player_y

    def _hand(self, player_index):

        player_x, player_y = self._positions(player_index)
        # Card spacing
        card_spacing = 74

        # Initialize player_position and player_rotation if empty
        while len(self.player_position) < 2:
            self.player_position.append((0, 0))
        while len(self.player_rotation) < 2:
            self.player_rotation.append(0)

        # Set positions for each card
        self.player_hand[0]._set_position(player_x - card_spacing, player_y)
        self.player_hand[1]._set_position(player_x + card_spacing, player_y)

        # Show cards for current player
        self.player_hand[0]._load_sprite(True)
        self.player_hand[1]._load_sprite(True)

        # Set scale for each card
        # self.player_hand[0]._set_scale(96, 144)
        # self.player_hand[1]._set_scale(96, 144)

        # Update positions in player_position array
        self.player_position[0] = (player_x - card_spacing, player_y)
        self.player_position[1] = (player_x + card_spacing, player_y)

    def _raise(self, current_highest_bet, amount):
        # Validate the raise amount
        bet = amount

        # All in case
        if bet >= self.money + self.bet:
            print(f"{self.name} went all in")
            current_highest_bet = self._all_in(current_highest_bet)
            self.have_bet = True
            return current_highest_bet

        # Regular raise
        elif bet > current_highest_bet:
            # Calculate the additional amount needed
            additional_amount = bet - self.bet

            # Ensure we have enough money
            if additional_amount > self.money:
                return self._all_in(current_highest_bet)

            # Update money and bet
            self.money -= additional_amount
            self.bet = bet  # Set the total bet to the raise amount
            current_highest_bet = bet
            self.have_bet = True
            return current_highest_bet

        # Invalid raise (less than current bet)
        else:
            return self._call(current_highest_bet)

    def _check(self, current_highest_bet):
        print(f"{self.name} checks")
        if current_highest_bet == 0 or current_highest_bet == self.bet:
            self.have_bet = True
            return current_highest_bet
        return current_highest_bet

    def _call(self, current_highest_bet):
        print(f"{self.name} calls {current_highest_bet}")

        # Calculate the additional amount needed to call
        additional_amount = current_highest_bet - self.bet

        # Check if we have enough money
        if additional_amount > self.money:
            return self._all_in(current_highest_bet)

        # Update money and bet
        self.money -= additional_amount
        self.bet = current_highest_bet
        self.have_bet = True
        return current_highest_bet

    def _fold(self, discard_pile):
        print(f"{self.name} folds")
        while self.player_hand:
            discard_pile.append(self.player_hand.pop(0))
        self.fold_bool = True
        return 0  # No change to current_highest_bet

    def _all_in(self, current_highest_bet):
        print(f"{self.name} goes all in with {self.money}")

        # Update the bet to include all money
        self.bet += self.money
        self.money = 0
        self.all_in_bool = True
        self.have_bet = True

        # Return the new highest bet if our all-in is higher
        if self.bet > current_highest_bet:
            return self.bet
        else:
            return current_highest_bet

    def get_check_or_call(self, options: [str]):
        return ("CALL", 0) if "CALL" in options else ("CHECK", 0)

    def random_bot_action(self, current_highest_bet: int, total_pot: int, flop: [], options: [str]):
        # Force fold if current_highest_bet exceeds the bot's money
        if current_highest_bet > self.money:
            # If "fold" is not in options, return whatever is available, but logically should include fold
            return "fold" if "fold" in options else random.choice(list(options)), 0
        else:
            action = random.choice(list(options))

            # If the chosen action is RAISE, limit the raise amount
            if action == "RAISE":
                # Limit raise to between the minimum raise and 25% of the bot's money
                min_raise = current_highest_bet + 1
                max_raise = min(current_highest_bet + int(self.money * 0.25), self.money)

                # If max_raise is less than min_raise (shouldn't happen but just in case)
                if max_raise < min_raise:
                    # Bot doesn't have enough for a reasonable raise, so choose another action
                    remaining_options = [opt for opt in options if opt != "RAISE"]
                    if remaining_options:
                        action = random.choice(remaining_options)
                        return action, 0
                    else:
                        # If no other options, just call or check
                        return self.get_check_or_call(options)

                # Return a random amount between min_raise and max_raise
                return action, random.randint(0, max_raise - current_highest_bet)
            elif action == "ALLIN":
                # Reduce the chance of going all-in
                if random.random() < 0.1:  # Only 10% chance to actually go all-in
                    return action, 0
                else:
                    # Choose a different action instead
                    remaining_options = [opt for opt in options if opt != "ALLIN"]
                    if remaining_options:
                        return random.choice(remaining_options), 0
                    else:
                        return self.get_check_or_call(options)
            else:
                return action, 0

    def default_bot_action(self, current_highest_bet: int, total_pot: int, flop: [], options: [str]):

        # `self` is your player object, it has fields like:
        #   `money` : How much money you have (does not include betted)
        #   `bet` : How much money has been betted in this match
        #   `player_hand` : Array of card objects, see `flop` for more details.

        # `current_highest_bet` is how much has been bet in this round
        # of betting so far

        # `total_pot` is how much is currently in the pot

        # `flop` is an array of Card objects that are currently on the flop
        # Card objects have a `type` and a `suit` that look like so:
        # SUITS = {0: "S", 1: "H", 2: "C", 3: "D"}
        # TYPE = {0: "A", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8", 8: "9", 9: "T", 10: "J", 11: "Q", 12: "K"}

        # `options` is a dictionary of {string: int} pairs. The options "CALL"
        # a
        # nd "CHECK" will not always be available, so it is recommended to
        # check your options, and use a backup option if you can't
        # `if "CHECK" in options: # Do logic`
        #   "FOLD"  : 1
        #   "CALL"  : 2
        #   "CHECK" : 3
        #   "RAISE" : 4
        #   "ALLIN" : 5

        hearts = 0
        clubs = 0
        spades = 0
        diamonds = 0

        # Check for suits on hand
        for card in self.player_hand:
            hearts += card.suit == "H"
            clubs += card.suit == "C"
            spades += card.suit == "S"
            diamonds += card.suit == "D"

        stay_in = 0

        # If we have pocket suits, thats a good sign for a flush
        if hearts == 2 or clubs == 2 or spades == 2 or diamonds == 2:
            stay_in += 1

        # If first flop is out and there are 4 of a suit between hand and flop
        # its a good idea to stay in
        if len(flop) >= 3:
            for card in flop:
                hearts += card.suit == "H"
                clubs += card.suit == "C"
                spades += card.suit == "S"
                diamonds += card.suit == "D"
            # These numbers include own hand
            stay_in += (hearts > 4 or clubs > 4 or spades > 4 or diamonds > 4)

        card_types = {}
        for card in (self.player_hand + flop):
            ct = card.type
            if ct not in card_types:
                card_types[ct] = 1
            else:
                card_types[ct] += 1

        # Find most card pairs
        max_count = 0
        max_type = None

        for ct, count in card_types.items():
            if count > max_count:
                max_type = ct
                max_count = count

        # two of a kind is a good sign
        if max_count >= 2:
            stay_in += 1

            # Bet a lot more if we're dealing with a pair of face cards or
            # have a three pair or better
            if max_type > 10 or max_count >= 3:
                return ("RAISE", self.money / 5) if self.money > 0 else self.get_check_or_call(options)

            # two pair low card isn't great, but good to bet on
            # early game
            if max_type < 6 and len(flop) < 4:
                return ("RAISE", self.money / 10) if self.money > 0 else self.get_check_or_call(options)

            # It's a good bet
            if total_pot < 20:
                return ("RAISE", self.money / 10) if self.money > 0 else self.get_check_or_call(options)

        if stay_in <= 1 and current_highest_bet > self.money:
            return ("FOLD", 0)

        if (stay_in > 0):
            return self.get_check_or_call(options)

        entropy = random.randint(0, 11) / 10.0
        if (entropy >= .4):
            return ("RAISE", random.randint(1, self.money)) if self.money > 0 else self.get_check_or_call(options)


        return ("FOLD", 0)

    # The actual player input on their turn
    def _player_turn(self, discard_pile, current_highest_bet, total_bet, flop):
        # Store the original bet amount to calculate the difference later
        old_bet = self.bet

        # Skip the player's turn if they've gone all in, folded, or have already bet the right amount
        if self.fold_bool or self.all_in_bool or (self.bet == current_highest_bet and self.have_bet):
            return total_bet, current_highest_bet

        else:
            print(f"\n{self.name} has ${self.money} (bet: ${self.bet}).")
            print(f"Player Hand: {[str(card) for card in self.player_hand]}")
            print(f"Current bet: ${current_highest_bet}")
            print(f"Total pot: ${total_bet}")

            # Check if we can check
            can_check = current_highest_bet == self.bet

            # How much we have to call
            call_amount = current_highest_bet - self.bet

            print("What do you want to do (enter index)?\n"
                  "1: Fold\n"
                  f"{'2' if call_amount > 0 else 'X'}: Call\n"
                  f"{'X' if not can_check else '3'}: Check\n"
                  "4: Raise\n"
                  "5: All in")

            options = {"FOLD": 1, "CALL": 2, "CHECK": 3, "RAISE": 4, "ALLIN": 5}

            if not call_amount > 0:
                options.pop("CALL")

            if not can_check:
                options.pop("CHECK")

            # Get the bot's action
            if self.name == "Alice":
                (player_action_name, raise_amount) = self.random_bot_action(
                    current_highest_bet, total_bet, flop, options)
            else:
                (player_action_name, raise_amount) = self.default_bot_action(
                    current_highest_bet, total_bet, flop, options)

            player_action = options[player_action_name]

            # Choose the player decision
            if player_action == 1:
                self._fold(discard_pile)
            elif player_action == 2 and call_amount > 0:
                # Check if player has enough money to call
                if call_amount > self.money:
                    # Not enough money to call, go all in instead
                    current_highest_bet = self._all_in(current_highest_bet)
                else:
                    current_highest_bet = self._call(current_highest_bet)
            elif player_action == 3 and can_check:
                current_highest_bet = self._check(current_highest_bet)
            elif player_action == 4:
                # We want to raise here
                if raise_amount <= 0:
                    # Invalid raise amount, default to minimum raise
                    raise_amount = current_highest_bet + 1
                else:
                    raise_amount = current_highest_bet + raise_amount

                # Ensure raise amount is at least the current highest bet
                raise_amount = max(raise_amount, current_highest_bet + 1)

                # Limit raise to available money
                available_for_raise = self.money + self.bet
                if raise_amount > available_for_raise:
                    raise_amount = available_for_raise

                current_highest_bet = self._raise(current_highest_bet, raise_amount)
            elif player_action == 5:
                current_highest_bet = self._all_in(current_highest_bet)

            # Calculate how much is being added to the pot
            bet_difference = self.bet - old_bet
            if bet_difference > 0:
                total_bet += bet_difference

            return total_bet, current_highest_bet
