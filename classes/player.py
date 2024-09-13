from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import pygame

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.selected_card = None
        self.selected_card_index = None

    def draw_card(self, deck):
        self.hand.append(deck.draw())

    def play_card(self, index):
        if self.hand:
            return self.hand.pop(index)
        return None

    def group_and_sort_hand(self, hand):
        suits = {'C': [], 'H': [], 'S': [], 'D': []}
        # Added rank_value method for easier comparisons
        for card in hand:
            suits[card.suit].append(card)
        # Sort cards within each suit
        for suit in suits:
            suits[suit].sort(key=lambda card: card.rank_value())
        # Flatten the sorted suits back into a list
        sorted_hand = []
        for suit in 'CHSD':
            sorted_hand.extend(suits[suit])
        return sorted_hand

    def select_previous_card(self):
        if len(self.hand) > 0:
            if self.selected_card_index is None:
                self.selected_card_index = 0
            else:
                self.selected_card_index = (self.selected_card_index - 1) % len(self.hand)
            self.selected_card = self.hand[self.selected_card_index]

    def select_next_card(self):
        if len(self.hand) > 0:
            if self.selected_card_index is None:
                self.selected_card_index = 0
            else:
                self.selected_card_index = (self.selected_card_index + 1) % len(self.hand)
            self.selected_card = self.hand[self.selected_card_index]

    def select_card(self, pos, renderer):
        num_cards = len(self.hand)
        if num_cards == 0:
            return
        max_width = SCREEN_WIDTH - 10  # total available width
        card_widths = [renderer.calculate_card_width(card) for card in self.hand]
        if not card_widths:
            return
        card_width = max(card_widths)

        # Adjust overlap if the total width exceeds the screen width
        total_cards_width = num_cards * card_width
        if total_cards_width > max_width:
            overlap = (total_cards_width - max_width) // (num_cards - 1)
            total_cards_width = card_width + (num_cards - 1) * (card_width - overlap)  # Adjust total width to include overlap
        else:
            overlap = 0  # no overlap if within screen width

        # Calculate the starting x position to center the cards
        x_position = (SCREEN_WIDTH - total_cards_width) // 2
        y_position = SCREEN_HEIGHT - 120

        # Hitbox detection for each card
        for i, card in enumerate(self.hand):
            card_rect = pygame.Rect(x_position, y_position, card_width - overlap, 100)  # Use adjusted card width
            if card_rect.collidepoint(pos):
                self.selected_card = card
                self.selected_card_index = i
                break
            x_position += card_width - overlap  # Move to the next card position

    def play_selected_card(self):
        if self.selected_card:
            print(f"{self.name} plays {self.selected_card}")
            card_played = self.selected_card
            self.hand.remove(self.selected_card)
            self.hand = self.group_and_sort_hand(self.hand)
            self.selected_card = None
            self.selected_card_index = None
            return card_played
        return None

    def bid_selected_card(self):
        if self.selected_card:
            bid_card = self.selected_card
            print(f"{self.name} bids {bid_card} (wishes to go {'high' if bid_card.color == 'black' else 'low'})!")
            self.selected_card = None
            self.selected_card_index = None
            return bid_card
        return None

