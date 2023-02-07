from Card import Card
from Constants import VALUES

class Hand:

    def __init__(self):
        self.cards: list[Card] = []
        self.card_img: list[str]= []

    def __str__(self):
        representation_string: str = "Cards in hand: "

        for card in self.cards:
            representation_string = representation_string + str(card) + " "

        return representation_string

    def add_card(self, card: Card):
        self.cards.append(card)

    def get_value(self) -> int:
        value: int = 0
        is_ace_present: bool = False

        for card in self.cards:
            value = value + VALUES[card.rank]

            if VALUES[card.rank] == 1:
                is_ace_present = True

        if (is_ace_present) and ((value + 10) <= 21):
            value = value + 10

        return value

    def display_cards(self):
        for card in self.cards:
            if str(card) not in self.card_img:
                self.card_img.append(str(card))