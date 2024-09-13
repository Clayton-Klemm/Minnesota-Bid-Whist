import random
from .card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in '23456789TJQKA' for suit in 'CDHS']
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
    
    def deal(self, num_players, cards_per_player):
        return [[self.draw() for _ in range(cards_per_player)] for _ in range(num_players)]

