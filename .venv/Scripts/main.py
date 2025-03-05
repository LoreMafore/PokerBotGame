"""

Made By Conrad Mercer 3/3/2025

"""

import pygame
import random
from Card import Cards

deck_of_cards = []
discard_pile = []


#Inialize the card deck
for card_suit in Cards.SUITS:
    for card_type in Cards.TYPE:
        deck_of_cards.append(Cards(card_type, card_suit))

random.shuffle(deck_of_cards)

for i in range(len(deck_of_cards)):
    print(deck_of_cards[i])


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