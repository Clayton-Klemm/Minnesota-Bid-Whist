# ml_agent.py
import random
from .bot import Bot  # Inherit from Bot so that isinstance(..., Bot) returns True
from classes.data_logger import log_decision

class MLAgent(Bot):
    def __init__(self, name):
        super().__init__(name)
        # Remove per-agent played cards; we will log the global played cards.
        # Optionally, you can still track what you personally played.
        self.seen_cards = []   # Cards revealed during bidding.
        self.my_played_cards = []  # Cards that this agent has played.

    def bid_selected_card(self, global_played=None, tricks_played=None, dealer_index=None):
        # Default values if not provided.
        if global_played is None:
            global_played = []
        if tricks_played is None:
            tricks_played = 0
        if dealer_index is None:
            dealer_index = -1

        bid_choice = random.choice(['high', 'low'])
        if bid_choice == 'high':
            black_cards = [card for card in self.hand if card.color == 'black']
            if black_cards:
                bid_card = random.choice(black_cards)
            else:
                red_cards = [card for card in self.hand if card.color == 'red']
                bid_card = random.choice(red_cards)
        else:
            red_cards = [card for card in self.hand if card.color == 'red']
            if red_cards:
                bid_card = random.choice(red_cards)
            else:
                black_cards = [card for card in self.hand if card.color == 'black']
                bid_card = random.choice(black_cards)
        
        self.selected_card = bid_card
        self.selected_card_index = self.hand.index(bid_card)
        
        # Record this card as seen (revealed) for bidding.
        self.seen_cards.append(bid_card)
        
        decision_data = {
            "agent": self.name,
            "phase": "bidding",
            "hand": ";".join(str(card) for card in self.hand),
            "bid_choice": bid_choice,
            "selected_card": str(bid_card),
            "seen_cards": ";".join(str(card) for card in self.seen_cards),
            "global_played_cards": ";".join(global_played),
            "tricks_played": tricks_played,
            "dealer_index": dealer_index
        }
        log_decision(decision_data)
        return bid_card

    def play_card(self, current_trick, game_mode, global_played=None, tricks_played=None):
        if global_played is None:
            global_played = []
        if tricks_played is None:
            tricks_played = 0

        if self.hand:
            if current_trick:
                lead_suit = current_trick[0][1].suit
                cards_in_suit = [card for card in self.hand if card.suit == lead_suit]
                if cards_in_suit:
                    if game_mode == 'HIGH':
                        card_played = max(cards_in_suit, key=lambda c: c.rank_value())
                    else:
                        card_played = min(cards_in_suit, key=lambda c: c.rank_value())
                else:
                    if game_mode == 'HIGH':
                        card_played = max(self.hand, key=lambda c: c.rank_value())
                    else:
                        card_played = min(self.hand, key=lambda c: c.rank_value())
            else:
                if game_mode == 'HIGH':
                    card_played = max(self.hand, key=lambda c: c.rank_value())
                else:
                    card_played = min(self.hand, key=lambda c: c.rank_value())
            self.hand.remove(card_played)
            
            self.my_played_cards.append(card_played)
            
            decision_data = {
                "agent": self.name,
                "phase": "playing",
                "hand": ";".join(str(card) for card in self.hand),
                "current_trick": ";".join(f"{idx}:{str(card)}" for idx, card in current_trick),
                "game_mode": game_mode,
                "selected_card": str(card_played),
                "my_played_cards": ";".join(str(card) for card in self.my_played_cards),
                "global_played_cards": ";".join(global_played),
                "tricks_played": tricks_played
            }
            log_decision(decision_data)
            
            return card_played
        return None
