"""

Made By Conrad Mercer 3/3/2025

"""

class Players():
 
 #maybe a total bet needs to be added rn there is one in the main function
 # but maybe i want to implement it here

    def __init__(self, initial_money):
        self.money = initial_money
        self.player_hand = []
        self.player_turn = False
        self.bet = 0
        self.fold_bool = False
        self.all_in_bool = False
        self.have_bet = False


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



    def _player_turn(self, discard_pile, current_highest_bet, total_bet):

        old_bet = self.bet
        if self.fold_bool == True or self.all_in_bool == True or self.bet == current_highest_bet and self.have_bet == True:
            return total_bet, current_highest_bet

        else:
            print("\nYou have",self.money, "dollars.")
            print(f"Player Hand: {[str(card) for card in self.player_hand]}")
            print("The bet was: ", current_highest_bet)
            print(f"The total bet: {total_bet}")
            print("What do you want to do?\n"
                "1: Fold\n"
                "2: Call\n"
                "3: Check\n"
                "4: Raise\n"
                "5: All in")

            player_action = int(input("Answer: "))

            if player_action == 1:
                self._fold(discard_pile)
                
            elif player_action == 2:
                self._call(current_highest_bet)

            elif player_action == 3:
                self._check(current_highest_bet)

            elif player_action == 4:
                current_highest_bet = self._raise(current_highest_bet)


            elif player_action == 5:
                current_highest_bet = self._all_in()

            total_bet += abs(self.bet - old_bet)

            return  total_bet, current_highest_bet
