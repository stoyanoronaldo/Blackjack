import random
from Card import Card, SUITS, RANKS

class Deck:

    def __init__(self):
        self.cards: list[Card] = []

        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        representation_string: str = "Cards in deck:\n"

        for card in self.cards:
            representation_string = representation_string + str(card) + "\n"

        return representation_string