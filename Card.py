from Constants import SUITS, RANKS

class Card:

    def __init__(self, suit: str, rank: str):

        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank

        else:
            self.suit = None
            self.rank = None
            print (f"Invalid card: {rank}{suit}")

    def __str__(self):
        return  self.rank + self.suit
        