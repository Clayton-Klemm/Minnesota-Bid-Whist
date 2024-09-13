import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Renderer:
    def __init__(self, screen, font, card_art):
        self.screen = screen
        self.font = font
        self.card_art = card_art

    def draw_hand(self, hand, selected_card):
        num_cards = len(hand)
        if num_cards == 0:
            return
        max_width = SCREEN_WIDTH - 10  # total available width
        card_widths = [self.calculate_card_width(card) for card in hand]
        if not card_widths:
            return
        card_width = max(card_widths)
        overlap = 0  # initial overlap
        # Calculate the total width if the cards are placed side by side without any overlap
        total_cards_width = num_cards * card_width
        # Adjust overlap if the total width exceeds the screen width
        if total_cards_width > max_width:
            overlap = (total_cards_width - max_width) // (num_cards - 1)
            total_cards_width = card_width + (num_cards - 1) * (card_width - overlap)  # Adjust total width to include overlap
        # Calculate the starting x position to center the cards
        x_position = (SCREEN_WIDTH - total_cards_width) // 2
        y_position = SCREEN_HEIGHT - 120  # Adjust Y position slightly to fit within the screen
        selected_y_position = y_position - 40  # Raised Y position for selected card
        # Display each card
        for i, card in enumerate(hand):
            card_key = f"{card.rank}{card.suit}"
            card_art_piece = self.card_art.get(card_key, "")
            lines = card_art_piece.split('\n')
            card_color = (0, 255, 0) if card == selected_card else (255, 255, 255)
            # Use the raised Y position if the card is selected
            current_y_position = selected_y_position if card == selected_card else y_position
            for k, line in enumerate(lines):
                text_surface = self.font.render(line, True, card_color)
                text_rect = text_surface.get_rect(topleft=(x_position, current_y_position + k * 20))
                self.screen.blit(text_surface, text_rect)
            x_position += card_width - overlap  # Move to the next card position, adjusting for overlap

    def draw_game_state_and_player_turn_status(self, game_state, active_player):
        game_state_and_player_turn = f"{game_state}"
        text_surface = self.font.render(game_state_and_player_turn, True, (255, 165, 0))
        text_rect = text_surface.get_rect()
        self.screen.blit(text_surface, text_rect)

    def draw_selected_card_info(self, selected_card):
        if selected_card:
            # Render text showing which card is selected in the top-right corner
            selected_card_text = f"Selected Card: {selected_card.rank} of {selected_card.suit}"
            text_surface = self.font.render(selected_card_text, True, (255, 165, 0))
            padding_right = 10  # Adjust the padding as needed
            padding_top = 10
            text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - padding_right, padding_top))
            self.screen.blit(text_surface, text_rect)

    def draw_current_trick(self, current_trick, players):
        # Updated to display cards at player positions
        positions = {
            0: (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 270),  # Player at bottom center
            1: (200, SCREEN_HEIGHT // 2 - 50),  # Bot 1 further left
            2: (SCREEN_WIDTH // 2 - 50, 150),    # Bot 2 at the top middle
            3: (SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 - 50)  # Bot 3 moved slightly to the left
        }
        for player_index, card in current_trick:
            x, y = positions[player_index]
            card_key = f"{card.rank}{card.suit}"
            card_art_piece = self.card_art.get(card_key, "")
            lines = card_art_piece.split('\n')
            card_color = (255, 255, 255)
            for k, line in enumerate(lines):
                text_surface = self.font.render(line, True, card_color)
                text_rect = text_surface.get_rect(topleft=(x, y + k * 20))
                self.screen.blit(text_surface, text_rect)

    def calculate_card_width(self, card):
        card_key = f"{card.rank}{card.suit}"
        card_art_piece = self.card_art.get(card_key, "")
        lines = card_art_piece.split('\n')
        max_line_length = max(len(line) for line in lines)
        return self.font.size(' ' * max_line_length)[0]  # Calculate the pixel width of the longest line

    def draw_bids(self, bids, players):
        # Positions for the bots' bid cards
        positions = {
            0: (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 270),  # Player at bottom center
            1: (200, SCREEN_HEIGHT // 2 - 50),  # Bot 1 further left
            2: (SCREEN_WIDTH // 2 - 50, 150),    # Bot 2 at the top middle
            3: (SCREEN_WIDTH - 300, SCREEN_HEIGHT // 2 - 50)  # Bot 3 moved slightly to the left
        }

        for i in range(1, 4):
            bid_card = bids[i]
            if bid_card is not None:
                # Draw the bid card at the specified position
                x, y = positions[i]
                card_key = f"{bid_card.rank}{bid_card.suit}"
                card_art_piece = self.card_art.get(card_key, "")
                lines = card_art_piece.split('\n')
                card_color = (255, 255, 255)
                for k, line in enumerate(lines):
                    text_surface = self.font.render(line, True, card_color)
                    text_rect = text_surface.get_rect(topleft=(x, y + k * 20))
                    self.screen.blit(text_surface, text_rect)

    def draw_tricks_won(self, tricks_won, players):
        # Compute team tricks
        team1_tricks = tricks_won[0] + tricks_won[2]  # Players 0 and 2 are partners
        team2_tricks = tricks_won[1] + tricks_won[3]  # Players 1 and 3 are partners
        text = f"Team 1 ({players[0].name} & {players[2].name}): {team1_tricks} tricks"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(0, 15))
        self.screen.blit(text_surface, text_rect)
        text = f"Team 2 ({players[1].name} & {players[3].name}): {team2_tricks} tricks"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(0, 30))
        self.screen.blit(text_surface, text_rect)

    def draw_continue_button(self):
        button_text = "Continue"
        button_color = (0, 255, 0)
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 80, 100, 50)
        pygame.draw.rect(self.screen, button_color, button_rect)
        text_surface = self.font.render(button_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        # Store button_rect for click detection
        self.continue_button_rect = button_rect

    def is_continue_button_clicked(self, pos):
        if hasattr(self, 'continue_button_rect'):
            return self.continue_button_rect.collidepoint(pos)
        else:
            return False

    def draw_players_names(self, players):
        # Positions for the player names
        positions = {
            0: (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150),  # Player 'You' at bottom center
            1: (50, SCREEN_HEIGHT // 2),  # Bot 1 to the far left
            2: (SCREEN_WIDTH // 2, 50),    # Bot 2 at the top middle, adjusted slightly upwards
            3: (SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2)  # Bot 3 moved to the right
        }

        for i in range(4):
            x, y = positions[i]
            name_text = players[i].name
            text_surface = self.font.render(name_text, True, (255, 165, 0))
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)

    def draw_game_result(self, tricks_won, players, game_mode, granded_player):
        # Display "Game Over" and "Tricks won"
        y_position = 100
        title_surface = self.font.render("Game Over", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        self.screen.blit(title_surface, title_rect)
        y_position += 50
        tricks_text = "Tricks won:"
        tricks_surface = self.font.render(tricks_text, True, (255, 255, 255))
        tricks_rect = tricks_surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        self.screen.blit(tricks_surface, tricks_rect)
        y_position += 30
        for i, player in enumerate(players):
            text = f"{player.name}: {tricks_won[i]}"
            text_surface = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            self.screen.blit(text_surface, text_rect)
            y_position += 30
        # Display scores or other info as needed


