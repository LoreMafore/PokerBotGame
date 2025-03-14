"""

Made By Conrad Mercer 3/3/2025

"""
from functools import total_ordering
from site import abs_paths

import pygame
import random
import os

from Card import Cards
from Dealer import Dealer
from Player import Players

import globals


def _check_all_players_done(player_list, end_of_round, current_highest_bet, pos=0):
    # Base case: we've checked all players
    if pos >= len(player_list):
        # All players have been checked and met the conditions
        print("All players have acted")
        end_of_round = False
        return True

    # Check if current player meets any of the conditions
    current_player = player_list[pos]
    if (current_player.bet == current_highest_bet or
            current_player.fold_bool == True or
            current_player.all_in_bool == True):
        # This player is done, check the next player
        return _check_all_players_done(player_list, end_of_round, current_highest_bet, pos + 1)
    else:
        # Found a player who still needs to act
        # TODO This is wrong at the end
        print("\n\nPLAYER NEEDS TO ACT NOW\n\n")
        return False


# determines turn order
def _turn_order(player_list, small_blind_pos, big_blind_pos, discard_pile, current_highest_bet, total_bet):
    end_of_round = True
    while end_of_round:

        # players after big blind
        for current_player_pos in range(big_blind_pos + 1, len(player_list)):
            total_bet, current_highest_bet = player_list[current_player_pos]._player_turn(discard_pile,
                                                                                          current_highest_bet,
                                                                                          total_bet)

        # players before big blind
        for current_player in range(small_blind_pos + 1):
            total_bet, current_highest_bet = player_list[current_player]._player_turn(discard_pile, current_highest_bet,
                                                                                      total_bet)

        # checks if all players need to do more actions

        if _check_all_players_done(player_list, end_of_round, current_highest_bet, 0) == True:
            end_of_round = False

        return total_bet, current_highest_bet


def _main():
    dealer = Dealer(4)
    small_blind = 50
    big_blind = 100
    small_blind_pos = 0
    big_blind_pos = small_blind_pos + 1

    while True:
        current_highest_bet = 0
        total_bet = 0
        flop_counter = 0
        dealer.flop = []

        # reset the player
        for p in dealer.player_list:
            p.player_hand = []
            p.bet = 0
            p.fold_bool = False
            p.all_in_bool = False
            p.have_bet = False

        # Reset and shuffle the deck
        dealer.deck_of_cards = []
        dealer._cards();
        dealer.shuffle_deck()

        # Deal two cards to each player
        dealer._dealing()

        # Print out each player's hand
        for i, player in enumerate(dealer.player_list):
            print(f"Player {dealer.player_list[i].name} hand: {[str(card) for card in player.player_hand]}")

        # set up small blind
        dealer.player_list[small_blind_pos].money -= small_blind
        dealer.player_list[small_blind_pos].bet = small_blind
        total_bet += small_blind
        print(f"Player {dealer.player_list[small_blind_pos].name} posts small blind: {small_blind}")

        # set up big blind
        dealer.player_list[big_blind_pos].money -= big_blind
        dealer.player_list[big_blind_pos].bet = big_blind
        total_bet += big_blind
        current_highest_bet = big_blind
        print(f"Player {dealer.player_list[big_blind_pos].name} posts big blind: {small_blind}")

        # Pre flop betting round
        print("\n=== PRE-FLOP BETTING ===")
        total_bet, current_highest_bet = _turn_order(dealer.player_list, small_blind_pos, big_blind_pos,
                                                     dealer.discard_pile, current_highest_bet, total_bet)

        # Get all the players who are actively playing
        active_players = sum(1 for player in dealer.player_list if not player.fold_bool)
        if (active_players <= 1):
            for player in dealer.player_list:
                if not player.fold_bool:
                    # Award winnings to remaining player
                    player.money += total_bet
                    print(f"{player.name} wins {total_bet}!")
                    break
        else:
            # Continue with flop, turn and river if more than one player still active
            game_complete = False

            # Flop
            print("\n=== FLOP ===")
            result = dealer._play_on_board(flop_counter)
            game_complete, flop_counter = result

            if active_players > 1:
                # Reset bets for post-flop betting round
                for player in dealer.player_list:
                    player.bet = 0
                    player.have_bet = False
                current_highest_bet = 0

                # Post-flop betting round
                total_bet, current_highest_bet = _turn_order(dealer.player_list, small_blind_pos, big_blind_pos,
                                                             dealer.discard_pile, current_highest_bet, total_bet)

                # Check if everyone but one player folded after flop
                active_players = sum(1 for player in dealer.player_list if not player.fold_bool)

            # Turn
            if active_players > 1:
                print("\n=== TURN ===")
                result = dealer._play_on_board(flop_counter)
                game_complete, flop_counter = result

                # Reset bets for post-turn betting round
                for player in dealer.player_list:
                    player.bet = 0
                    player.have_bet = False
                current_highest_bet = 0

                # Post-turn betting round
                total_bet, current_highest_bet = _turn_order(dealer.player_list, small_blind_pos, big_blind_pos,
                                                             dealer.discard_pile, current_highest_bet, total_bet)

                # Check if everyone but one player folded after turn
                active_players = sum(1 for player in dealer.player_list if not player.fold_bool)

            # River
            if active_players > 1:
                print("\n=== RIVER ===")
                result = dealer._play_on_board(flop_counter)
                game_complete, flop_counter = result

                # Reset bets for post-river betting round
                for player in dealer.player_list:
                    player.bet = 0
                    player.have_bet = False
                current_highest_bet = 0

                # Post-river betting round
                total_bet, current_highest_bet = _turn_order(dealer.player_list, small_blind_pos, big_blind_pos,
                                                             dealer.discard_pile, current_highest_bet, total_bet)

            # Determine the winner if more than one player is still active
            active_players = sum(1 for player in dealer.player_list if not player.fold_bool)
            if active_players <= 1:
                for player in dealer.player_list:
                    if not player.fold_bool:
                        player.money += total_bet
                        print(f"{player.name} wins ${total_bet} as everyone else folded!")
                        break
            else:
                # Show all active players' hands
                print("\n=== SHOWDOWN ===")
                for player in dealer.player_list:
                    if not player.fold_bool:
                        print(f"{player.name}'s hand: {[str(card) for card in player.player_hand]}")

                winner = dealer._check_winner()
                if winner:
                    winner.money += total_bet
                    print(f"{winner.name} wins ${total_bet} with hand: {[str(card) for card in winner.player_hand]}")
                else:
                    print("No winner determined (all players folded).")

        # Move the blinds for the next hand
        small_blind_pos = (small_blind_pos + 1) % len(dealer.player_list)
        big_blind_pos = (small_blind_pos + 1) % len(dealer.player_list)

        # Ask if the player wants to continue
        play_again = input("\nPlay another hand? (y/n): ")
        if play_again.lower() != 'y':
            break


def reset_game(dealer):
    # Reset players
    for p in dealer.player_list:
        p.player_hand = []
        p.bet = 0
        p.fold_bool = False
        p.all_in_bool = False
        p.have_bet = False

    # Reset and shuffle the deck
    dealer.deck_of_cards = []
    dealer.flop = []
    dealer.discard_pile = []
    dealer._cards()
    dealer.shuffle_deck()

    # Deal two cards to each player
    dealer._dealing()


pygame.init()
globals.screen
# screen = pygame.display.set_mode((1920, 1080))

pygame.display.set_caption("Poker Game")
clock = pygame.time.Clock()
running = True

background_path = "../Sprites/Table.png"
abs_path = os.path.abspath(background_path)
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (1920, 1080))

# Initialize the dealer
dealer = Dealer(4)

# Reset and shuffle the deck
dealer.deck_of_cards = []
dealer._cards()  # Note: removed the semicolon (;) which is not needed in Python
dealer.shuffle_deck()

# Deal two cards to each player
dealer._dealing()

# Game state variables
flop_counter = 0
game_phase = "preflop"  # preflop, flop, turn, river, showdown

background = pygame.transform.scale(background, (globals.screen.get_width(), globals.screen.get_height()))

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False  # Changed from pygame.quit() to properly exit the loop
            elif event.key == pygame.K_SPACE:
                # Progress the game when spacebar is pressed
                if game_phase == "preflop":
                    game_phase = "flop"
                    done, flop_counter = dealer._play_on_board(flop_counter)
                elif game_phase == "flop":
                    game_phase = "turn"
                    done, flop_counter = dealer._play_on_board(flop_counter)
                elif game_phase == "turn":
                    game_phase = "river"
                    done, flop_counter = dealer._play_on_board(flop_counter)
                elif game_phase == "river":
                    game_phase = "showdown"
                elif game_phase == "showdown":
                    # Reset the game
                    reset_game(dealer)
                    game_phase = "preflop"
                    flop_counter = 0

        if event.type == pygame.QUIT:
            running = False

    # Draw background
    globals.screen.blit(background, (0, 0))

    # drawing the draw cards is cool but is a lot of effort for something
    # that doesn't really work. same with drawing the discard pile
    for cards in dealer.deck_of_cards:
        # cards._set_scale(96, 144)
        # cards.draw(globals.screen)
        continue

    for discarded in dealer.discard_pile:
        # discarded.draw(globals.screen)
        continue

    # Draw all players' cards
    for player in dealer.player_list:
        for card in player.player_hand:
            card.draw(globals.screen)

    # Draw flop cards
    for card in dealer.flop:
        card.draw(globals.screen)

    # Display game phase
    font = pygame.font.Font('../fonts/PixelOperator8.ttf', 24)
    phase_text = font.render(f"Game Phase: {game_phase}", True, (255, 255, 255))
    globals.screen.blit(phase_text, (10, 10))

    # Display instructions
    instructions = font.render("Press SPACE to advance game, ESC/Q to quit", True, (255, 255, 255))
    globals.screen.blit(instructions, (10, 40))

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
