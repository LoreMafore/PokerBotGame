"""
Made By Conrad Mercer 3/3/2025
"""

import pygame

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
# def _turn_order(player_list, small_blind_pos, big_blind_pos, discard_pile, current_highest_bet, total_bet):
#     end_of_round = True
#     while end_of_round:
#
#         # players after big blind
#         for current_player_pos in range(big_blind_pos + 1, len(player_list)):
#             total_bet, current_highest_bet = player_list[current_player_pos]._player_turn(discard_pile,
#                                                                                           current_highest_bet,
#                                                                                           total_bet)
#
#         # players before big blind
#         for current_player in range(small_blind_pos + 1):
#             total_bet, current_highest_bet = player_list[current_player]._player_turn(discard_pile, current_highest_bet,
#                                                                                       total_bet)
#
#         # checks if all players need to do more actions
#
#         if _check_all_players_done(player_list, end_of_round, current_highest_bet, 0) == True:
#             end_of_round = False
#
#         return total_bet, current_highest_bet


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


def main():
    pygame.init()

    # Setup screen
    if not hasattr(globals, 'screen'):
        globals.screen = pygame.display.set_mode((1920, 1080))

    pygame.display.set_caption("Poker Game")
    clock = pygame.time.Clock()
    running = True

    # Load background
    background_path = "../Sprites/Table.png"
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (globals.screen.get_width(), globals.screen.get_height()))

    # Initialize font
    try:
        font = pygame.font.Font('../fonts/PixelOperator8.ttf', 24)
    except pygame.error:
        font = pygame.font.SysFont('Arial', 24)

    # Game variables
    dealer = Dealer(4)
    small_blind = 50
    big_blind = 100
    small_blind_pos = 0
    big_blind_pos = small_blind_pos + 1

    # Game state variables
    total_bet = 0
    current_highest_bet = 0
    flop_counter = 0
    active_players = 4

    # Game phases: "setup", "preflop", "flop", "turn", "river", "showdown", "results"
    game_phase = "setup"

    # Messages to display
    # messages = []
    # max_messages = 10

    def add_message(msg):
        print(msg)
        # messages.append(msg)
        # if len(messages) > max_messages:
        #     messages.pop(0)

    def start_new_hand():
        nonlocal game_phase, total_bet, current_highest_bet, flop_counter

        # Reset game state
        game_phase = "setup"
        total_bet = 0
        current_highest_bet = 0
        flop_counter = 0
        dealer.flop = []

        # Clear messages
        # messages.clear()

        add_message("Starting new hand...")

        # Reset players
        for p in dealer.player_list:
            p.player_hand = []
            p.bet = 0
            p.fold_bool = False
            p.all_in_bool = False
            p.have_bet = False

        # Reset and shuffle deck
        dealer.deck_of_cards = []
        dealer._cards()
        dealer.shuffle_deck()

        # Deal cards
        dealer._dealing()

        # Display hands
        for i, player in enumerate(dealer.player_list):
            add_message(f"{player.name} hand: {[str(card) for card in player.player_hand]}")

        # Set blinds
        dealer.player_list[small_blind_pos].money -= small_blind
        dealer.player_list[small_blind_pos].bet = small_blind
        total_bet += small_blind
        add_message(f"{dealer.player_list[small_blind_pos].name} posts small blind: {small_blind}")

        dealer.player_list[big_blind_pos].money -= big_blind
        dealer.player_list[big_blind_pos].bet = big_blind
        total_bet += big_blind
        current_highest_bet = big_blind
        add_message(f"{dealer.player_list[big_blind_pos].name} posts big blind: {big_blind}")

        # Move to preflop
        game_phase = "preflop"

    # Start the first hand
    start_new_hand()

    player_turn_index = 0

    # Main game loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                    break

                # Pass the key event to the current player's turn handler
                if game_phase in ["preflop", "flop", "turn", "river"]:
                    current_player = dealer.player_list[player_turn_index]
                    if (current_player.fold_bool):
                        player_turn_index = (player_turn_index + 1) % len(dealer.player_list)
                        break

                    did_something, new_total_bet, new_current_highest_bet = (
                        current_player.player_turn_alt(event, dealer.discard_pile, current_highest_bet, total_bet))

                    # If the player chose a valid thing
                    if did_something and new_total_bet > 0 and new_current_highest_bet > 0:
                        current_highest_bet = new_current_highest_bet
                        total_bet = new_total_bet

                        # Move to next player
                        player_turn_index = (player_turn_index + 1) % len(dealer.player_list)

        # Game state processing - happens every frame, not just on space press
        if game_phase == "preflop":
            # Check if all players have had their turn (completed the betting round)
            all_players_acted = all(player.have_bet or player.fold_bool for player in dealer.player_list)

            if all_players_acted:
                # Reset player betting states for next phase
                for player in dealer.player_list:
                    player.have_bet = False

                # Check active players
                active_players = sum(1 for player in dealer.player_list if not player.fold_bool)
                if active_players <= 1:
                    game_phase = "results"
                    add_message("Only one player remaining. Skipping to results.")
                else:
                    game_phase = "flop"
                    add_message("=== FLOP ===")
                    result = dealer._play_on_board(flop_counter)
                    game_complete, flop_counter = result

                    # Reset bets for post-flop
                    for player in dealer.player_list:
                        player.bet = 0
                    current_highest_bet = 0

        elif game_phase == "flop":
            # Check if all players have had their turn (completed the betting round)
            all_players_acted = all(player.have_bet or player.fold_bool for player in dealer.player_list)
            if all_players_acted:
                # Reset player betting states for next phase
                for player in dealer.player_list:
                    player.have_bet = False

                # Check active players
                active_players = sum(1 for player in dealer.player_list if not player.fold_bool)
                if active_players <= 1:
                    game_phase = "results"
                    add_message("Only one player remaining. Skipping to results.")
                else:
                    game_phase = "turn"
                    add_message("=== TURN ===")
                    result = dealer._play_on_board(flop_counter)
                    game_complete, flop_counter = result

                    # Reset bets for post-turn
                    for player in dealer.player_list:
                        player.bet = 0
                    current_highest_bet = 0

        elif game_phase == "turn":
            # Check if all players have had their turn (completed the betting round)
            all_players_acted = all(player.have_bet or player.fold_bool for player in dealer.player_list)
            if all_players_acted:
                # Reset player betting states for next phase
                for player in dealer.player_list:
                    player.have_bet = False

                # Check active players
                active_players = sum(1 for player in dealer.player_list if not player.fold_bool)
                if active_players <= 1:
                    game_phase = "results"
                    add_message("Only one player remaining. Skipping to results.")
                else:
                    game_phase = "river"
                    add_message("=== RIVER ===")
                    result = dealer._play_on_board(flop_counter)
                    game_complete, flop_counter = result

                    # Reset bets for post-river
                    for player in dealer.player_list:
                        player.bet = 0
                    current_highest_bet = 0

        elif game_phase == "river":
            # Check if all players have had their turn (completed the betting round)
            all_players_acted = all(player.have_bet or player.fold_bool for player in dealer.player_list)
            if all_players_acted:
                # Reset player betting states for next phase
                for player in dealer.player_list:
                    player.have_bet = False

                game_phase = "showdown"
                add_message("=== SHOWDOWN ===")

                # Show active players' hands
                for player in dealer.player_list:
                    if not player.fold_bool:
                        add_message(f"{player.name}'s hand: {[str(card) for card in player.player_hand]}")

                # Determine winner
                active_players = sum(1 for player in dealer.player_list if not player.fold_bool)
                if active_players <= 1:
                    for player in dealer.player_list:
                        if not player.fold_bool:
                            player.money += total_bet
                            add_message(f"{player.name} wins ${total_bet} as everyone else folded!")
                            break
                else:
                    winner = dealer._check_winner()
                    if winner:
                        winner.money += total_bet
                        add_message(f"{winner.name} wins ${total_bet}!")
                    else:
                        add_message("No winner determined.")

                # Move directly to results
                game_phase = "results"

        elif game_phase == "results":
            # Add a brief delay before starting a new hand (prevent instant restart)
            current_time = pygame.time.get_ticks()
            if not hasattr(globals, 'results_start_time'):
                globals.results_start_time = current_time

            # Wait 3 seconds before starting a new hand
            if current_time - globals.results_start_time > 3000:  # 3 seconds in milliseconds
                # Move the blinds for next hand
                small_blind_pos = (small_blind_pos + 1) % len(dealer.player_list)
                big_blind_pos = (small_blind_pos + 1) % len(dealer.player_list)

                # Start a new hand
                start_new_hand()

                # Reset the timer
                delattr(globals, 'results_start_time')

                # Reset to preflop phase
                game_phase = "preflop"
                add_message("=== NEW HAND ===")
                add_message("=== PRE-FLOP BETTING ===")

        # Clear screen with background
        globals.screen.blit(background, (0, 0))

        # Draw player cards
        for player in dealer.player_list:
            for card in player.player_hand:
                card.draw(globals.screen)

        # Draw community cards
        for card in dealer.flop:
            card.draw(globals.screen)

        # Display game phase
        phase_text = font.render(f"Game Phase: {game_phase}", True, (255, 255, 255))
        globals.screen.blit(phase_text, (10, 10))

        # Display current player's turn (if in a betting phase)
        if game_phase in ["preflop", "flop", "turn", "river"]:
            current_player = dealer.player_list[player_turn_index]
            turn_text = font.render(f"Current Player: {current_player.name}", True, (255, 255, 0))
            globals.screen.blit(turn_text, (10, 40))
            instructions = font.render(current_player.get_text(current_highest_bet), True, (255, 255, 255))
            globals.screen.blit(instructions, (10, 70))
        else:
            instructions = font.render("ESC/Q to quit", True, (255, 255, 255))
            globals.screen.blit(instructions, (10, 40))

        # Display pot size
        pot_text = font.render(f"Total Pot: ${total_bet}", True, (255, 255, 255))
        globals.screen.blit(pot_text, (10, 100))

        # Display player info
        player_info_x = 10
        player_info_y = globals.screen.get_height() - 150
        for i, player in enumerate(dealer.player_list):
            # Display player name, money, bet status
            color = (255, 255, 255)
            if player.fold_bool:
                status = "FOLDED"
                color = (200, 0, 0)
            elif player.all_in_bool:
                status = "ALL IN"
                color = (0, 200, 200)
            else:
                status = "Active"
                color = (0, 200, 0)

            # Highlight current player's turn
            if game_phase in ["preflop", "flop", "turn", "river"] and i == player_turn_index:
                pygame.draw.rect(globals.screen, (255, 255, 0),
                                 (player_info_x - 5, player_info_y + (i * 30) - 2, 400, 25), 1)

            player_text = font.render(f"{player.name}: ${player.money} - Bet: ${player.bet} - Status: {status}", True,
                                      color)
            globals.screen.blit(player_text, (player_info_x, player_info_y + (i * 30)))

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
