import random
from .player import Player

class Bot(Player):
    def __init__(self, name):
        super().__init__(name)

    def bid_selected_card(self):
        # Randomly decide to bid high or low
        bid_choice = random.choice(['high', 'low'])
        if bid_choice == 'high':
            # Attempt to select a random black card
            black_cards = [card for card in self.hand if card.color == 'black']
            if black_cards:
                bid_card = random.choice(black_cards)
            else:
                # No black cards, select a random red card
                red_cards = [card for card in self.hand if card.color == 'red']
                bid_card = random.choice(red_cards)
        else:
            # Attempt to select a random red card
            red_cards = [card for card in self.hand if card.color == 'red']
            if red_cards:
                bid_card = random.choice(red_cards)
            else:
                # No red cards, select a random black card
                black_cards = [card for card in self.hand if card.color == 'black']
                bid_card = random.choice(black_cards)
        # Set selected card (without removing it from hand)
        self.selected_card = bid_card
        self.selected_card_index = self.hand.index(bid_card)
        return bid_card

    def play_card(self, current_trick, game_mode):
        if self.hand:
            if current_trick:
                lead_suit = current_trick[0][1].suit
                cards_in_suit = [card for card in self.hand if card.suit == lead_suit]
                if cards_in_suit:
                    if game_mode == 'HIGH':
                        # Play highest card in the lead suit
                        card_played = max(cards_in_suit, key=lambda c: c.rank_value())
                    else:
                        # Play lowest card in the lead suit
                        card_played = min(cards_in_suit, key=lambda c: c.rank_value())
                else:
                    # No cards in the lead suit
                    if game_mode == 'HIGH':
                        # Play highest card from hand
                        card_played = max(self.hand, key=lambda c: c.rank_value())
                    else:
                        # Play lowest card from hand
                        card_played = min(self.hand, key=lambda c: c.rank_value())
            else:
                # Leading the trick
                if game_mode == 'HIGH':
                    # Lead with the highest card
                    card_played = max(self.hand, key=lambda c: c.rank_value())
                else:
                    # Lead with the lowest card
                    card_played = min(self.hand, key=lambda c: c.rank_value())
            self.hand.remove(card_played)
            return card_played
        return None