"""
Made By Conrad Mercer 3/3/2025
"""
from functools import total_ordering
import pygame
import random
import os
import sys
import time

from Card import Cards
from Dealer import Dealer
from Player import Players


def _check_game_over(player_list):
    """Check if the game is over (only one player has money left)"""
    players_with_money = 0
    winner = None

    for player in player_list:
        if player.money > 0:
            players_with_money += 1
            winner = player

    return players_with_money <= 1, winner


def _show_game_over_screen(screen, background, winner):
    """Display the game over screen with the winner"""
    # Draw background
    screen.blit(background, (0, 0))

    # Create font for game over text
    font = pygame.font.SysFont('Arial', 36)

    # Draw game over title
    title = font.render("Game Over", True, (255, 255, 255))
    screen.blit(title, (1920 // 2 - title.get_width() // 2, 400))

    # Draw winner text
    winner_text = font.render(f"{winner.name} wins the game with ${winner.money}!", True, (255, 255, 0))
    screen.blit(winner_text, (1920 // 2 - winner_text.get_width() // 2, 500))

    # Draw restart instructions
    instructions = font.render("Press SPACE to play again", True, (255, 255, 255))
    screen.blit(instructions, (1920 // 2 - instructions.get_width() // 2, 600))

    # Update the display
    pygame.display.flip()

    # Wait for spacebar to restart
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_restart = False
                    return True  # Return True to indicate restart
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.delay(50)  # Short delay to prevent CPU overuse

    return True


def _check_all_players_done(player_list, current_highest_bet):
    # Loop through all players and check if any still need to act
    for player in player_list:
        # Skip players who are broke
        if hasattr(player, 'broke') and player.broke:
            continue

        # Skip players who have folded or gone all-in
        if player.fold_bool or player.all_in_bool:
            continue

        # A player needs to act if they haven't bet the current highest amount
        # AND they haven't had a chance to act (have_bet is False)
        if player.bet != current_highest_bet and not player.have_bet:
            print(f"\n\n{player.name} NEEDS TO ACT NOW\n\n")
            return False

    # If we get here, all players have acted correctly
    print("All players have acted")
    return True


# determines turn order
def _turn_order(player_list, small_blind_pos, big_blind_pos, discard_pile, current_highest_bet, total_bet, screen,
                dealer, background, game_phase):
    # Reset have_bet flag for all players at the start of a betting round
    for player in player_list:
        player.have_bet = False

    # Start with the player after the big blind
    current_player_index = big_blind_pos + 1
    if current_player_index >= len(player_list):
        current_player_index = 0

    # Track how many players we've checked since the last bet
    players_checked = 0

    # Count active players (not folded, not broke)
    active_players = sum(1 for p in player_list if not p.fold_bool and not p.broke)

    # If everyone but one player is folded or broke, no need for betting
    if active_players <= 1:
        return total_bet, current_highest_bet

    # Main betting loop - continue until all players have acted appropriately
    while players_checked < len(player_list):
        # Get current player
        current_player = player_list[current_player_index]

        # Update the display before getting player input
        _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, current_player,
                current_highest_bet, total_bet)
        pygame.display.flip()

        # Skip players who are broke
        if current_player.broke:
            current_player_index = (current_player_index + 1) % len(player_list)
            players_checked += 1
            continue

        # Skip players who have folded or gone all-in
        if current_player.fold_bool or current_player.all_in_bool:
            current_player_index = (current_player_index + 1) % len(player_list)
            players_checked += 1
            continue

        # Skip players who have already matched the current bet
        if current_player.bet == current_highest_bet and current_player.have_bet:
            current_player_index = (current_player_index + 1) % len(player_list)
            players_checked += 1
            continue

        # Handle player's turn
        old_highest_bet = current_highest_bet
        total_bet, current_highest_bet = current_player._player_turn(discard_pile, current_highest_bet, total_bet,
                                                                     dealer.flop)

        # Mark that this player has had a chance to bet
        current_player.have_bet = True

        # If the bet was raised, reset our counter since all players need to act again
        if current_highest_bet > old_highest_bet:
            players_checked = 0
        else:
            players_checked += 1

        # Move to next player
        current_player_index = (current_player_index + 1) % len(player_list)

        # Add 5-second delay between moves
        for i in range(50):  # 50 * 0.1 = 5 seconds
            # Update display during delay to show the latest state
            _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None, current_highest_bet,
                    total_bet)
            pygame.display.flip()

            # Check for escape key during delay
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            time.sleep(0.00005)  # Small sleep to avoid high CPU usage

    # One final check to make sure everyone has acted
    if not _check_all_players_done(player_list, current_highest_bet):
        print("Warning: Not all players have properly acted, but betting round is ending")

    return total_bet, current_highest_bet


def _update(screen, dealer, background, game_phase, small_blind_pos=None, big_blind_pos=None, current_player=None,
            current_highest_bet=0, total_pot=0):
    # Create a copy of events to prevent clearing the event queue
    events = []
    for event in pygame.event.get():
        events.append(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    screen.blit(background, (0, 0))

    # Move discard pile out of view (don't need to draw them)
    for card in dealer.discard_pile:
        card._set_position(2000, 2000)  # Far off-screen

    # Draw all players' cards and player info
    for i, player in enumerate(dealer.player_list):
        # Draw cards if player has them and isn't broke
        if player.player_hand and not player.broke and not player.fold_bool:
            for card in player.player_hand:
                card.is_showing_card = True  # Show all cards
                card.draw(screen)

            # Draw player info between cards
            _draw_player_info(screen, player, i, small_blind_pos, big_blind_pos,
                           (player == current_player))  # Pass whether this is current player

    # Draw deck (only draw the top card to represent the deck)
    if dealer.deck_of_cards:
        # Set a specific position for the deck
        deck_x = 1920 // 2 + 400
        deck_y = 1080 // 2 - 50
        dealer.deck_of_cards[0]._set_position(deck_x, deck_y)
        dealer.deck_of_cards[0].draw(screen)

    # Don't draw the discard pile at all
    # Remove or comment out these lines:
    # if dealer.discard_pile:
    #     dealer.discard_pile[0].draw(screen)

    # Draw flop cards - ensure flop cards are always shown face up
    for card in dealer.flop:
        card.is_showing_card = True
        card._load_sprite(True)  # Force load face-up sprite
        card.draw(screen)

    # Display game phase and pot in top left
    font = pygame.font.SysFont('Arial', 24)
    phase_text = font.render(f"Game Phase: {game_phase}", True, (255, 255, 255))
    screen.blit(phase_text, (10, 10))

    # Display pot size using the passed total_pot parameter
    pot_text = font.render(f"Pot: ${total_pot}", True, (255, 255, 255))
    screen.blit(pot_text, (10, 40))

    # Display current highest bet
    bet_text = font.render(f"Current Bet: ${current_highest_bet}", True, (255, 255, 255))
    screen.blit(bet_text, (10, 70))

    # Display current player if available - make this more visible and persistent
    if current_player:
        current_player_text = font.render(f"Current Player: {current_player.name}", True, (255, 255, 100))
        # Add a background for better visibility
        text_rect = current_player_text.get_rect(topleft=(10, 100))
        pygame.draw.rect(screen, (50, 50, 50), text_rect.inflate(20, 10))
        screen.blit(current_player_text, (10, 100))


def _draw_player_info(screen, player, player_index, small_blind_pos=None, big_blind_pos=None, is_current=False):
    # Calculate position based on player index
    player_x, player_y = player._positions(player_index)

    # Determine player status
    if hasattr(player, 'broke') and player.broke:
        status = "BROKE"
        color = (255, 100, 100)  # Red for broke players
    elif player.fold_bool:
        status = "FOLDED"
        color = (200, 200, 200)  # Gray for folded
    elif player.all_in_bool:
        status = "ALL-IN"
        color = (255, 215, 0)  # Gold for all-in
    elif not player.have_bet:
        status = "NEEDS TO ACT"
        color = (255, 255, 100)  # Yellow for needs to act
    else:
        status = "HAS ACTED"
        color = (100, 255, 100)  # Green for active

    # Create font
    font = pygame.font.SysFont('Arial', 16)

    # Create text surfaces
    name_text = font.render(f"{player.name:^20}", True, (255, 0, 0) if not is_current else (255, 255, 0))
    bet_text = font.render(f"Bet: ${player.bet}", True, (255, 255, 255))
    money_text = font.render(f"Money: ${player.money}", True, (255, 255, 255))
    status_text = font.render(f"{status}", True, color)

    # Check if this player is small or big blind
    is_small_blind = small_blind_pos is not None and player_index == small_blind_pos
    is_big_blind = big_blind_pos is not None and player_index == big_blind_pos

    blind_text = None
    if is_small_blind:
        blind_text = font.render("SMALL BLIND", True, (255, 0, 165))  # Pink for small blind
    elif is_big_blind:
        blind_text = font.render("BIG BLIND", True, (255, 165, 0))  # Orange for big blind

    # Position text to the right of the right card
    card_spacing = 74
    text_x = player_x + 15  # Move to the right of the right card
    text_y = player_y - 80

    # Draw background highlight for current player
    if is_current:
        info_width = 150
        info_height = 100
        pygame.draw.rect(screen, (50, 50, 100),
                      (text_x - 5, text_y - 5, info_width, info_height),
                      border_radius=5)

    # Draw text left-aligned
    screen.blit(name_text, (text_x, text_y))
    text_y += 16
    screen.blit(money_text, (text_x, text_y))
    text_y += 16
    screen.blit(bet_text, (text_x, text_y))
    text_y += 16
    screen.blit(status_text, (text_x, text_y))

    # Draw blind indicator if applicable
    if blind_text:
        text_y += 16
        screen.blit(blind_text, (text_x, text_y))

    # Additional visual indicator for current player
    if is_current:
        pygame.draw.circle(screen, (255, 255, 0), (text_x - 10, player_y), 5)


def _game_logic(screen, dealer, background):
    # Game setup variables
    small_blind = 50
    big_blind = 100
    small_blind_pos = 0
    big_blind_pos = 1

    play_again = True

    while play_again:
        # Check if the game is over (only one player with money)
        game_over, winner = _check_game_over(dealer.player_list)
        if game_over:
            print(f"Game over! {winner.name} has won the game with ${winner.money}!")
            restart = _show_game_over_screen(screen, background, winner)
            if restart:
                # Reset all players with initial money for a new game
                for p in dealer.player_list:
                    p.money = 1000
                    p.broke = False
            else:
                return

        # Reset game state for new hand
        total_bet = 0
        current_highest_bet = 0
        flop_counter = 0
        dealer.flop = []
        game_phase = "Pre-Flop"

        # Reset players for new hand
        for p in dealer.player_list:
            p.player_hand = []
            p.bet = 0
            p.fold_bool = False
            p.all_in_bool = False
            p.have_bet = False

            # Mark players with 0 money as broke (they'll be skipped in this hand)
            if p.money <= 0:
                p.broke = True
                print(f"Player {p.name} is broke and will sit out this hand")
            else:
                p.broke = False

        # Reset and shuffle the deck
        dealer.deck_of_cards = []
        dealer._cards()
        dealer.shuffle_deck()

        # Deal two cards to each player
        dealer._dealing()

        # Update display after dealing
        _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None, current_highest_bet,
                total_bet)
        pygame.display.flip()

        # Output initial hands to console
        for i, player in enumerate(dealer.player_list):
            print(f"Player {dealer.player_list[i].name} hand: {[str(card) for card in player.player_hand]}")

        # Set up small blind (find next non-broke player)
        original_small_blind_pos = small_blind_pos
        while dealer.player_list[small_blind_pos].broke:
            small_blind_pos = (small_blind_pos + 1) % len(dealer.player_list)
            # If we've checked all players and come back to the original, everyone is broke
            if small_blind_pos == original_small_blind_pos:
                print("All players are broke! Game cannot continue.")
                return

        dealer.player_list[small_blind_pos].money -= small_blind
        dealer.player_list[small_blind_pos].bet = small_blind
        total_bet += small_blind
        print(f"Player {dealer.player_list[small_blind_pos].name} posts small blind: {small_blind}")

        # Set up big blind (find next non-broke player after small blind)
        big_blind_pos = (small_blind_pos + 1) % len(dealer.player_list)
        original_big_blind_pos = big_blind_pos
        while dealer.player_list[big_blind_pos].broke:
            big_blind_pos = (big_blind_pos + 1) % len(dealer.player_list)
            # If we've checked all players and come back to the original, there's only one player with money
            if big_blind_pos == original_big_blind_pos or big_blind_pos == small_blind_pos:
                print("Not enough players with money to continue.")
                # Award the pot to the small blind player and end
                dealer.player_list[small_blind_pos].money += total_bet
                return

        dealer.player_list[big_blind_pos].money -= big_blind
        dealer.player_list[big_blind_pos].bet = big_blind
        total_bet += big_blind
        current_highest_bet = big_blind
        print(f"Player {dealer.player_list[big_blind_pos].name} posts big blind: {big_blind}")

        # Update display after blinds
        _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None, current_highest_bet,
                total_bet)
        pygame.display.flip()

        # Pre-flop betting round
        print("\n=== PRE-FLOP BETTING ===")
        # Make sure all players have their have_bet flag reset
        for player in dealer.player_list:
            # The blinds count as having bet
            if player == dealer.player_list[small_blind_pos] or player == dealer.player_list[big_blind_pos]:
                player.have_bet = True
            else:
                player.have_bet = False

        total_bet, current_highest_bet = _turn_order(dealer.player_list, small_blind_pos, big_blind_pos,
                                                     dealer.discard_pile, current_highest_bet, total_bet,
                                                     screen, dealer, background, game_phase)

        # Get all active players (not folded)
        active_players = sum(1 for player in dealer.player_list if not player.fold_bool and not player.broke)

        # If only one player remains, award pot and skip to next hand
        if active_players <= 1:
            for player in dealer.player_list:
                if not player.fold_bool and not player.broke:
                    # Award winnings to remaining player
                    player.money += total_bet
                    print(f"{player.name} wins {total_bet}!")
                    game_phase = "End of Hand"
                    _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None,
                            current_highest_bet, total_bet)
                    pygame.display.flip()
                    time.sleep(2)  # Pause to show the winner
                    break
        else:
            # Continue with flop if more than one player still active
            game_phase = "Flop"
            _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None, current_highest_bet,
                    total_bet)
            pygame.display.flip()

            # Flop
            print("\n=== FLOP ===")
            result = dealer._play_on_board(flop_counter)
            game_complete, flop_counter = result

            # Update display after flop
            _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None, current_highest_bet,
                    total_bet)
            pygame.display.flip()

            if active_players > 1:
                # Reset bets for post-flop betting round
                for player in dealer.player_list:
                    player.bet = 0
                    player.have_bet = False
                current_highest_bet = 0

                # Post-flop betting round
                total_bet, current_highest_bet = _turn_order(dealer.player_list, small_blind_pos, big_blind_pos,
                                                             dealer.discard_pile, current_highest_bet, total_bet,
                                                             screen, dealer, background, game_phase)

                # Check active players after flop
                active_players = sum(1 for player in dealer.player_list if not player.fold_bool and not player.broke)

            # Turn
            if active_players > 1:
                game_phase = "Turn"
                _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None,
                        current_highest_bet, total_bet)
                pygame.display.flip()

                print("\n=== TURN ===")
                result = dealer._play_on_board(flop_counter)
                game_complete, flop_counter = result

                # Update display after turn
                _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None,
                        current_highest_bet, total_bet)
                pygame.display.flip()

                # Reset bets for post-turn betting round
                for player in dealer.player_list:
                    player.bet = 0
                    player.have_bet = False
                current_highest_bet = 0

                # Post-turn betting round
                total_bet, current_highest_bet = _turn_order(dealer.player_list, small_blind_pos, big_blind_pos,
                                                             dealer.discard_pile, current_highest_bet, total_bet,
                                                             screen, dealer, background, game_phase)

                # Check active players after turn
                active_players = sum(1 for player in dealer.player_list if not player.fold_bool and not player.broke)

            # River
            if active_players > 1:
                game_phase = "River"
                _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None,
                        current_highest_bet, total_bet)
                pygame.display.flip()

                print("\n=== RIVER ===")
                result = dealer._play_on_board(flop_counter)
                game_complete, flop_counter = result

                # Update display after river
                _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None,
                        current_highest_bet, total_bet)
                pygame.display.flip()

                # Reset bets for post-river betting round
                for player in dealer.player_list:
                    player.bet = 0
                    player.have_bet = False
                current_highest_bet = 0

                # Post-river betting round
                total_bet, current_highest_bet = _turn_order(dealer.player_list, small_blind_pos, big_blind_pos,
                                                             dealer.discard_pile, current_highest_bet, total_bet,
                                                             screen, dealer, background, game_phase)

            # Determine the winner
            active_players = sum(1 for player in dealer.player_list if not player.fold_bool and not player.broke)
            if active_players <= 1:
                for player in dealer.player_list:
                    if not player.fold_bool and not player.broke:
                        player.money += total_bet
                        print(f"{player.name} wins ${total_bet} as everyone else folded!")
                        break
            else:
                # Show all active players' hands
                game_phase = "Showdown"
                _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None,
                        current_highest_bet, total_bet)
                pygame.display.flip()

                print("\n=== SHOWDOWN ===")
                for player in dealer.player_list:
                    if not player.fold_bool and not player.broke:
                        print(f"{player.name}'s hand: {[str(card) for card in player.player_hand]}")

                # Use the manual winner selection
                winner = dealer._check_winner()
                if winner:
                    winner.money += total_bet
                    print(f"{winner.name} wins ${total_bet} with hand: {[str(card) for card in winner.player_hand]}")
                else:
                    print("No winner determined (all players folded).")

                # Update display to show winner
                game_phase = f"Winner: {winner.name if winner else 'None'}"
                _update(screen, dealer, background, game_phase, small_blind_pos, big_blind_pos, None,
                        current_highest_bet, total_bet)
                pygame.display.flip()
                time.sleep(2)  # Pause to show the winner

        # Move the blinds for the next hand
        small_blind_pos = (small_blind_pos + 1) % len(dealer.player_list)
        big_blind_pos = (big_blind_pos + 1) % len(dealer.player_list)

        # Small delay before the next hand
        # time.sleep(1.5)


def _main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Poker Game")
    clock = pygame.time.Clock()

    # Try to load the background with error handling
    try:
        background_path = "../Sprites/Table.png"
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (1920, 1080))
    except pygame.error:
        print(f"Warning: Could not load background image from {background_path}")
        print("Creating a plain color background instead")
        background = pygame.Surface((1920, 1080))
        background.fill((0, 100, 0))  # Dark green background

    # Initialize the dealer with players
    dealer = Dealer(7)

    # Position the cards for each player once at the start
    for player_index, player in enumerate(dealer.player_list):
        player._positions(player_index)

    # Main game loop
    running = True
    game_started = False
    game_over = False

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if not game_started:
                        game_started = True
                    elif game_over:
                        # Reset players for a new game
                        for p in dealer.player_list:
                            p.money = 1000
                            p.broke = False
                        game_started = True
                        game_over = False

            if event.type == pygame.QUIT:
                running = False

        # Draw background
        screen.blit(background, (0, 0))

        if not game_started:
            # Show start screen
            font = pygame.font.SysFont('Arial', 36)
            title = font.render("Texas Hold'em Poker", True, (255, 255, 255))
            screen.blit(title, (1920 // 2 - title.get_width() // 2, 400))

            instructions = font.render("Press SPACE to start game", True, (255, 255, 255))
            screen.blit(instructions, (1920 // 2 - instructions.get_width() // 2, 500))

            # Show player names and positions
            y_pos = 600
            for i, player in enumerate(dealer.player_list):
                player_text = font.render(f"Player {i + 1}: {player.name}", True, (255, 255, 255))
                screen.blit(player_text, (1920 // 2 - player_text.get_width() // 2, y_pos))
                y_pos += 40
        else:
            # Start the main game logic - this won't return until the game is over
            _game_logic(screen, dealer, background)
            # Reset game_started after a complete game
            game_started = False
            game_over = True

        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    _main()
