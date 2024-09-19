import pygame
import random
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from classes.deck import Deck
from classes.player import Player
from classes.bot import Bot
from classes.renderer import Renderer
from utils import load_card_art

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.players = [
            Player("You"),
            Bot("Bot 1"),
            Bot("Bot 2"),
            Bot("Bot 3")
        ]
        self.deck = Deck()
        self.card_art = load_card_art()  # Ensure this is a dictionary
        self.font = pygame.font.Font(pygame.font.match_font('couriernew'), 16)  # Fixed-width font
        self.renderer = Renderer(self.screen, self.font, self.card_art)
        self.double_click_threshold = 250  # milliseconds required to play the card
        self.last_click_time = 0
        self.game_state = 'BIDDING'  # Initial game state
        self.bids = [None] * 4  # Store bids decisions of each player
        self.game_mode = None  # Will be set after bidding phase ('HIGH' or 'LOW')
        self.current_trick = []
        self.tricks_won = [0] * 4  # Tracks the number of tricks won by each player
        self.tricks_played = 0  # Number of tricks played so far
        self.trick_winner = None  # Index of the player who won the last trick
        self.granded_player = None  # The player who first bid black
        self.dealer_index = random.randint(0, 3)  # Random initial dealer
        self.waiting_for = None  # To manage the "Continue" button state
        self.initialize_game()

    def initialize_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = self.deck.deal(4, 13)
        for i, player in enumerate(self.players):
            player.hand = player.group_and_sort_hand(self.hands[i])
            player.selected_card = None  # Reset selected card
        self.tricks_won = [0] * 4
        self.tricks_played = 0
        self.current_trick = []
        self.bids = [None] * 4
        self.game_state = 'BIDDING'
        self.active_player = (self.dealer_index + 1) % 4  # Start bidding with player to the left of dealer
        self.game_mode = None
        self.granded_player = None
        self.waiting_for = None

    def run(self):
        while self.running:
            if self.game_state == 'BIDDING':
                self.handle_bidding_events()
            elif self.game_state == 'PLAYING':
                self.handle_playing_events()
            elif self.game_state == 'WAITING':
                self.handle_waiting_events()
            elif self.game_state == 'END':
                self.show_game_result()
                self.game_state = 'WAITING'
                self.waiting_for = 'NEW_ROUND'
            self.draw()
            self.clock.tick(FPS)

    def process_events(self, keydown_handler, click_handler):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_state = 'END'
            elif event.type == pygame.KEYDOWN:
                if not isinstance(self.players[self.active_player], Bot):
                    keydown_handler(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not isinstance(self.players[self.active_player], Bot):
                    click_handler(event.pos)

    def handle_bidding_events(self):
        self.process_events(self.handle_bidding_keydown, self.handle_bidding_click)
        current_player = self.players[self.active_player]
        if isinstance(current_player, Bot):
            bid_card = current_player.bid_selected_card()
            self.bids[self.active_player] = bid_card
            print(f"{current_player.name} bids {bid_card} (wishes to go {'high' if bid_card.color == 'black' else 'low'})!")
            if bid_card.color == 'black' and self.granded_player is None:
                self.granded_player = self.active_player
                self.game_mode = 'HIGH'
                print(f"Game Mode is {self.game_mode}")
                self.set_starting_player()
                self.game_state = 'WAITING'
                self.waiting_for = 'PLAYING'
            else:
                self.advance_bidding()
            self.draw()
            pygame.display.flip()
            pygame.time.delay(500)  # Wait 500 milliseconds

    def advance_bidding(self):
        self.active_player = (self.active_player + 1) % 4
        if self.granded_player is not None:
            pass
        elif self.active_player == (self.dealer_index + 1) % 4:
            self.game_mode = 'LOW'
            print(f"Game Mode is {self.game_mode}")
            self.set_starting_player()
            self.game_state = 'WAITING'
            self.waiting_for = 'PLAYING'

    def set_starting_player(self):
        if self.game_mode == 'HIGH':
            self.active_player = (self.granded_player - 1) % 4
            print(f"{self.players[self.active_player].name} will start the play.")
        else:
            self.active_player = (self.dealer_index + 1) % 4
            print(f"{self.players[self.active_player].name} will start the play.")

    def handle_playing_events(self):
        self.process_events(self.handle_keydown, self.handle_click)
        current_player = self.players[self.active_player]
        if isinstance(current_player, Bot):
            card_played = current_player.play_card(self.current_trick, self.game_mode)
            if card_played:
                self.current_trick.append((self.active_player, card_played))
                print(f"{current_player.name} plays {card_played}")
                self.draw()
                pygame.display.flip()
                pygame.time.delay(500)  # Wait 500 milliseconds
                self.next_player()

    def handle_waiting_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_state = 'END'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if self.renderer.is_continue_button_clicked(pos):
                    if self.waiting_for == 'PLAYING':
                        self.game_state = 'PLAYING'
                    elif self.waiting_for == 'NEW_ROUND':
                        self.dealer_index = (self.dealer_index + 1) % 4  # Move dealer to next player
                        self.initialize_game()
                        self.game_state = 'BIDDING'
                    self.waiting_for = None

    def handle_keydown_generic(self, key, action_function):
        if key == pygame.K_LEFT:
            self.players[self.active_player].select_previous_card()
        elif key == pygame.K_RIGHT:
            self.players[self.active_player].select_next_card()
        elif key == pygame.K_RETURN:
            action_function()

    def handle_keydown(self, key):
        self.handle_keydown_generic(key, self.play_selected_card)

    def handle_bidding_keydown(self, key):
        self.handle_keydown_generic(key, self.bid_selected_card)

    def handle_click_generic(self, pos, action_function):
        current_click_time = time.time()
        time_since_last_click = (current_click_time - self.last_click_time) * 1000  # Convert to milliseconds
        if time_since_last_click <= self.double_click_threshold:
            action_function()
        else:
            self.players[self.active_player].select_card(pos, self.renderer)
        self.last_click_time = current_click_time

    def handle_click(self, pos):
        self.handle_click_generic(pos, self.play_selected_card)

    def handle_bidding_click(self, pos):
        self.handle_click_generic(pos, self.bid_selected_card)

    def bid_selected_card(self):
        bid_card = self.players[self.active_player].bid_selected_card()
        if bid_card:
            self.bids[self.active_player] = bid_card
            print(f"{self.players[self.active_player].name} bids {bid_card} (wishes to go {'high' if bid_card.color == 'black' else 'low'})!")
            if bid_card.color == 'black' and self.granded_player is None:
                self.granded_player = self.active_player
                self.game_mode = 'HIGH'
                print(f"Game Mode is {self.game_mode}")
                self.set_starting_player()
                self.game_state = 'WAITING'
                self.waiting_for = 'PLAYING'
            else:
                self.advance_bidding()

    def play_selected_card(self):
        if self.players[self.active_player].selected_card:
            if self.is_valid_play(self.players[self.active_player], self.players[self.active_player].selected_card):
                card_played = self.players[self.active_player].play_selected_card()
                self.current_trick.append((self.active_player, card_played))
                print(f"{self.players[self.active_player].name} plays {card_played}")
                self.next_player()
            else:
                print("Invalid card played. You must follow suit.")
        else:
            print("No card selected.")

    def is_valid_play(self, player, card):
        if not self.current_trick:
            return True
        else:
            lead_suit = self.current_trick[0][1].suit
            if card.suit == lead_suit:
                return True
            else:
                for c in player.hand:
                    if c.suit == lead_suit:
                        return False  # Must follow suit
                return True  # No card of lead suit, can play any card

    def next_player(self):
        if len(self.current_trick) == 4:
            self.evaluate_trick()
            self.current_trick = []
            self.tricks_played += 1
            if self.tricks_played == 13:
                self.game_state = 'END'
            else:
                self.active_player = self.trick_winner
        else:
            self.active_player = (self.active_player + 1) % 4

    def evaluate_trick(self):
        lead_suit = self.current_trick[0][1].suit
        rank_order = {'2': 2, '3': 3, '4':4, '5':5, '6':6, '7':7, '8':8,
                      '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
        valid_cards = [(idx, card) for idx, card in self.current_trick if card.suit == lead_suit]
        winning_card = max(valid_cards, key=lambda x: rank_order[x[1].rank])
        self.trick_winner = winning_card[0]
        self.tricks_won[self.trick_winner] += 1
        print(f"{self.players[self.trick_winner].name} wins the trick with {winning_card[1]}")

    def show_game_result(self):
        print("Game Over")
        print("Tricks won:")
        for i, player in enumerate(self.players):
            print(f"{player.name}: {self.tricks_won[i]}")

        team1_tricks = self.tricks_won[0] + self.tricks_won[2]
        team2_tricks = self.tricks_won[1] + self.tricks_won[3]

        if self.game_mode == 'HIGH':
            granded_team = [self.granded_player, (self.granded_player + 2) % 4]
            granded_team_tricks = sum(self.tricks_won[i] for i in granded_team)
            other_team_tricks = 13 - granded_team_tricks

            if granded_team_tricks >= 7:
                score = granded_team_tricks - 6
                print(f"Granding team ({self.players[granded_team[0]].name} and {self.players[granded_team[1]].name}) score {score} point(s)")
            else:
                over_tricks = other_team_tricks - 6
                if over_tricks > 0:
                    score = over_tricks * 2
                    print(f"Other team ({self.players[(granded_team[0]+1)%4].name} and {self.players[(granded_team[0]+3)%4].name}) score {score} point(s)")
                else:
                    print(f"Other team does not score any points")
        else:
            if team1_tricks < 7:
                score = 7 - team1_tricks
                print(f"Team 1 ({self.players[0].name} and {self.players[2].name}) score {score} point(s)")
            else:
                print(f"Team 1 does not score any points")
            if team2_tricks < 7:
                score = 7 - team2_tricks
                print(f"Team 2 ({self.players[1].name} and {self.players[3].name}) score {score} point(s)")
            else:
                print(f"Team 2 does not score any points")

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.game_state == 'BIDDING':
            self.draw_players_hands()
            self.renderer.draw_game_state_and_player_turn_status(self.game_state, self.players[self.active_player].name)
            self.renderer.draw_selected_card_info(self.players[self.active_player].selected_card)
            self.renderer.draw_bids(self.bids, self.players)
        elif self.game_state == 'PLAYING':
            self.draw_players_hands()
            self.renderer.draw_game_state_and_player_turn_status(self.game_state, self.players[self.active_player].name)
            self.renderer.draw_selected_card_info(self.players[self.active_player].selected_card)
            self.renderer.draw_current_trick(self.current_trick, self.players)
            self.renderer.draw_tricks_won(self.tricks_won, self.players)
            self.renderer.draw_players_names(self.players)
        elif self.game_state == 'WAITING':
            if self.waiting_for == 'PLAYING':
                self.draw_players_hands()
                self.renderer.draw_game_state_and_player_turn_status('Bidding Complete', '')
                self.renderer.draw_bids(self.bids, self.players)
                self.renderer.draw_players_names(self.players)
            elif self.waiting_for == 'NEW_ROUND':
                self.renderer.draw_game_result(self.tricks_won, self.players, self.game_mode, self.granded_player)
            self.renderer.draw_continue_button()
        pygame.display.flip()

    def draw_players_hands(self):
        if len(self.players) != 4:
            print("Error: incorrect number of players")
            return
        # self.renderer.draw_hand(self.players[self.active_player].hand, self.players[self.active_player].selected_card)
        
        human_player = self.players[0]  # Assuming the human player is always at index 0
        self.renderer.draw_hand(human_player.hand, human_player.selected_card)
