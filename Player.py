"""

Made By Conrad Mercer 3/3/2025

"""
from main import player
from Dealer import Dealer


class Players():

    def __init__(self, initial_money):
        self.money = initial_money
        self.player_hand = []

    def _update(self, big_blind_pos, small_blind_pos):
        #will check the position the big_blind and small_blind in relative to the player
        pass

    def _hand(self):
        #right now this will just print out your hand but this should
        #probably hold the position of your cards?
        print(self.player_hand[0], self.player_hand[1])

    def _raise(self, current_highest_bet):
        bet = int(input("Raise Amount:"))
        if bet >= self.money:
            #will change this for pygame implementation
            print("You went all in")
            self._all_in()
        elif bet > current_highest_bet:
            self.money -= bet
            current_highest_bet = bet

        else:
            print("try again")


    def _check(self, current_highest_bet):
        if current_highest_bet == 0:
            #pass turn
            pass

    def _call(self, current_highest_bet):
        if current_highest_bet != 0:
            #minus the money you already put in
            self.money -= current_highest_bet

        pass

    def _fold(self, discard_pile):
        while self.player_hand:
            discard_pile.append(self.player_hand.pop(0))
        pass

    def _all_in(self):
        pass