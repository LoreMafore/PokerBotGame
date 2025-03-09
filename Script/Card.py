"""

Made By Conrad Mercer 3/3/2025

"""
#card creator
class Cards:
    SUITS = {0: "♠", 1: "♥", 2: "♣", 3: "♦"}
    TYPE = {0: "A", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7",
            7: "8", 8: "9", 9: "10", 10: "J", 11: "Q", 12: "K"}

    def __init__(self, type: int, suit: int):
        if type not in self.TYPE:
            raise ValueError("Value must be btwn 0-12")
        if suit not in self.SUITS:
            raise ValueError("Suit must be an integer between 0 - 3")

        self.type = type
        self.suit = suit

    def __str__(self):
        return f"{self.TYPE[self.type]}{self.SUITS[self.suit]}"

    def __repr__(self):
        return f"Cards({self.type}, {self.suit})"

    #draw card function maybe this could be in player, function for card facing, innit and final position of cards