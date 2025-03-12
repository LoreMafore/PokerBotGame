"""

Made By Conrad Mercer 3/3/2025

"""
import pygame.math
from Dealer import Dealer


class Players():
 
 #maybe a total bet needs to be added rn there is one in the main function
 # but maybe i want to implement it here

    def __init__(self, initial_money, name):
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


    def _update(self, big_blind_pos, small_blind_pos):
        #will check the position the big_blind and small_blind in relative to the player
        pass


    def _hand(self, player_index):
    #should have a function or logic here to determine position of player
    #chat gpt says for a oval centerted at (h,k) we need to do
    # x = h+ a cos(theta) --- a being the horinztal radius
    # y = k + b sin(theta) --- b being the vertical radius
    #theta = 2pi/number of player times which player you are currently on


        if len(self.player_hand) >= 2:
            print(f"Player {self.name} has: {self.player_hand[0]}, {self.player_hand[1]}")

            table_center_x = 1920 // 2
            table_center_y = 1080 // 2

            # Oval dimensions - these may not be right
            a = 500  # Horizontal radius
            b = 300

            #total_players = dealer .player_list.size()
            #angle = 2 * math.pi * (player_index / total_players)

            card_spacing = self.player_hand[0].width + 10
            card_pos = pygame.math.Vector2(200 + player_index * 100)

            self.player_hand[0]._set_position(card_pos.x,card_pos.y)
            self.player_hand[1]._set_position(card_pos.x + card_spacing, card_pos.y)

            self.player_hand[0]._load_sprite(True)
            self.player_hand[1]._load_sprite(True)

            self.player_hand[0]._set_scale(96, 144)
            self.player_hand[1]._set_scale(96, 144)

            # self.player_hand[0]._set_scale(64, 96)
            # self.player_hand[1]._set_scale(64, 96)

            self.player_hand[0].is_showing_card = True
            self.player_hand[1].is_showing_card = True

    def _raise(self, current_highest_bet):
        bet = int(input("Raise Amount:"))
        if bet >= self.money:
            #will change this for pygame implementation
            print("You went all in")
            current_highest_bet = self._all_in()
            self.have_bet = True
            return current_highest_bet

        elif bet > current_highest_bet:
            self.money -= bet
            self.bet += bet - self.bet
            current_highest_bet = bet
            self.have_bet = True
            return current_highest_bet

        else:
            print("try again")
            self._raise(current_highest_bet)

    def _check(self, current_highest_bet):
        print("check")
        if current_highest_bet == 0:
            self.have_bet = True
            return current_highest_bet

    def _call(self, current_highest_bet):
        print("call")
        if current_highest_bet != 0:
            #this needs to check if you will go all in or not
            self.money -= current_highest_bet - self.bet
            self.bet += current_highest_bet
            self.have_bet = True
            return  current_highest_bet


    def _fold(self, discard_pile):
        print("fold")
        while self.player_hand:
            discard_pile.append(self.player_hand.pop(0))
        self.fold_bool = True

    def _all_in(self, current_highest_bet):
        print("all in")
        self.bet += self.money
        self.money -= self.money
        self.all_in_bool = True
        self.have_bet = True

        if self.bet > current_highest_bet:
            current_highest_bet = self.bet
            return current_highest_bet

        else:
            return current_highest_bet


    # The actual player input on their turn

    def _player_turn(self, discard_pile, current_highest_bet, total_bet):

        old_bet = self.bet

        # Skip the players turn if they've gone all in, folded, or have already bet the right amount
        if self.fold_bool == True or self.all_in_bool == True or (self.bet == current_highest_bet and self.have_bet == True):
            return total_bet, current_highest_bet

        else:
            print(f"\n{self.name} has",self.money, "dollars.")
            print(f"Player Hand: {[str(card) for card in self.player_hand]}")
            print(f"The bet was: ", current_highest_bet)
            print(f"The pot is : {total_bet}")

            # are we able to check?
            can_check = current_highest_bet == self.bet

            # how much we have to call
            call_amount = current_highest_bet - self.bet;

            print("What do you want to do (enter index)?\n"
                "1: Fold\n"
                f"{'2' if call_amount > 0 else 'X'}: Call\n"
                f"{'X' if not can_check else '3'}: Check\n"
                "4: Raise\n"
                "5: All in")

            player_action = int(input("Answer: "))

            # Choose the player decision
            if player_action == 1:
                self._fold(discard_pile)
            elif player_action == 2 and call_amount > 0:
                self._call(current_highest_bet)
            elif player_action == 3 and can_check:
                self._check(current_highest_bet)
            elif player_action == 4:
                current_highest_bet = self._raise(current_highest_bet)
            elif player_action == 5:
                current_highest_bet = self._all_in(current_highest_bet)

            # how much is being added to the pot
            total_bet += abs(self.bet - old_bet)

            return  total_bet, current_highest_bet
