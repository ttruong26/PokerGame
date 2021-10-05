from random import shuffle
from card import Card

# Creates a deck that acts as a list object
# Holds all 52 Card values that should be in a deck
class Deck(list):
    def __init__(self):
        super().__init__()
        suits = list(range(1, 5))
        ranks = list(range(2, 15))
        [[self.append(Card(i, j)) for j in suits] for i in ranks]

    def shuffle(self):
        shuffle(self)

    def deal(self):
        return self.pop(0)