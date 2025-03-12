"""

Made By Conrad Mercer 3/3/2025

"""
#card creator
import pygame



#card creator
class Cards:
    SUITS = {0: "S", 1: "H", 2: "C", 3: "D"}
    TYPE = {0: "A", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7",
            7: "8", 8: "9", 9: "T", 10: "J", 11: "Q", 12: "K"}

    def __init__(self, type: int, suit: int):
        if type not in self.TYPE:
            raise ValueError("Value must be btwn 0-12")
        if suit not in self.SUITS:
            raise ValueError("Suit must be an integer between 0 - 3")

        self.type = type
        self.suit = suit
        self.sprite = None
        self.pos = (0,0)
        self.width = 64 #64
        self.height = 96 #96
        self.rotate = 0
        self.is_showing_card = False
        self._load_sprite(self.is_showing_card)

    def _load_sprite(self, showing_card):
        card_name = f"{self.TYPE[self.type]}-{self.SUITS[self.suit]}.png"
        card_path = f"C:/Users/momer/Coding/PythonProjects/PokerBotGame/Sprites/dark-cards/{card_name}"
        card_back_path = f"C:/Users/momer/Coding/PythonProjects/PokerBotGame/Sprites/dark-cards/BACK.png"
        if showing_card:
            self.sprite = pygame.image.load(card_path)

        else:
            self.sprite = pygame.image.load(card_back_path)

        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

    def _set_position(self, x, y, rotation = 0):
        self.pos = (x,y)
        self.rotate = rotation

    def _set_scale(self, width, height):
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.width = width
        self.height = height

    def draw(self, screen):
        self._set_scale(self.width, self.height)
       # self._load_sprite(self.is_showing_card)
        if self.rotate != 0:
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotate)
            screen.blit(rotated_sprite, self.pos)

        else:
            screen.blit(self.sprite,self.pos)

    def __str__(self):
        return f"{self.TYPE[self.type]} of {self.SUITS[self.suit]}"

    def __repr__(self):
        return f"Cards({self.type}, {self.suit})"

    #draw card function maybe this could be in player, function for card facing, innit and final position of cards