"""

Made By Conrad Mercer 3/3/2025

"""
from functools import total_ordering

import pygame
import random

from Card import Cards
from Dealer import Dealer
from Player import Players


def _check_all_players_done(player_list, end_of_round, current_highest_bet, pos=0):
    # Base case: we've checked all players
    if pos >= len(player_list):
        # All players have been checked and met the conditions
        print("All players have acted")
        return True
        end_of_round = False

    # Check if current player meets any of the conditions
    current_player = player_list[pos]
    if (current_player.bet == current_highest_bet or
            current_player.fold_bool == True or
            current_player.all_in_bool == True):
        # This player is done, check the next player
        return _check_all_players_done(player_list, end_of_round,current_highest_bet, pos + 1)
    else:
        # Found a player who still needs to act
        print("\n\nPLAYER NEEDS TO ACT NOW\n\n")
        return False

#determines turn order
def _turn_order(player_list, small_blind_pos, big_blind_pos, discard_pile, current_highest_bet):
    end_of_round = True
    while end_of_round:
        #players after big blind
        for current_player_pos in range(big_blind_pos + 1, len(player_list)):
            player_list[current_player_pos]._player_turn(discard_pile, current_highest_bet)
        #players before big blind
        for current_player in range(small_blind_pos+1):
            player_list[current_player]._player_turn(discard_pile, current_highest_bet)
        #checks if all players need to do more actions
        _check_all_players_done(player_list, end_of_round, current_highest_bet, 0)

        if _check_all_players_done(player_list, end_of_round, current_highest_bet, 0) == True:
            end_of_round = False

        pass
    

def _main():
    start_of_round = True
    dealer = Dealer(4)
    small_blind = 50
    big_blind = 100
    small_blind_pos = 0
    big_blind_pos = small_blind_pos + 1

    if start_of_round:
        current_highest_bet = 0
        total_bet = 0
        # Shuffle the deck
        dealer.shuffle_deck()

        # Deal two cards to each player
        dealer._dealing()

        # Print out each player's hand
        for i, player in enumerate(dealer.player_list):
            print(f"Player {i + 1} hand: {[str(card) for card in player.player_hand]}")

        #set up small blind
        dealer.player_list[small_blind_pos].money -= small_blind
        dealer.player_list[small_blind_pos].bet = small_blind
        total_bet += small_blind

        #set up big blind
        dealer.player_list[big_blind_pos].money -= big_blind
        dealer.player_list[big_blind_pos].bet = big_blind
        total_bet += big_blind
        current_highest_bet = big_blind

        #player turns
        _turn_order(dealer.player_list, small_blind_pos, big_blind_pos, dealer.discard_pile, current_highest_bet )

        #TODO dealer plays then _turn_order

        #at the end of everything this shifts small and big blind
        if small_blind_pos < len(dealer.player_list) + 1:
            small_blind_pos += 1
            if small_blind_pos == len(dealer.player_list):
                big_blind = 0
            else:
                big_blind = small_blind_pos + 1

        else:
            small_blind_pos = 0

        #TODO There probably needs a game manger script

if __name__ == '__main__':
    _main()



# pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
#
# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("purple")
#
#     # RENDER YOUR GAME HERE
#
#     # flip() the display to put your work on screen
#     pygame.display.flip()
#
#     clock.tick(60)  # limits FPS to 60
#
# pygame.quit()