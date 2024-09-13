class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.color = 'red' if suit in 'HD' else 'black'

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def rank_value(self):
        rank_order = {'2': 2, '3': 3, '4':4, '5':5, '6':6, '7':7, '8':8,
                      '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
        return rank_order[self.rank]
