"""

Made By Conrad Mercer 3/3/2025

"""
from functools import total_ordering

import pygame
import random

from Card import Cards
from Dealer import Dealer
from Player import Players

start_of_round = True

player_1 = Players(initial_money=1000)
player_2 = Players(initial_money=1000)
player_3 = Players(initial_money=1000)

player_list = [player_1,player_2,player_3]

dealer = Dealer(player_list)
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

    player_list[small_blind_pos].money -= small_blind
    total_bet += small_blind

    player_list[big_blind_pos].money -= big_blind
    total_bet += big_blind
    current_highest_bet = big_blind

    #TODO Implement a turn function that allows player to do there normal turn
    #TODO There probably needs a game manger script










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