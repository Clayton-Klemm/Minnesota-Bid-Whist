import pygame
import random
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, USE_ML_AGENTS
from classes.deck import Deck
from classes.player import Player
from classes.bot import Bot
from classes.renderer import Renderer
from utils import load_card_art

# Conditionally import MLAgent if needed
if USE_ML_AGENTS:
    from classes.ml_agent import MLAgent

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.next_action = None # For tracking user's end-game choice
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_played_cards = [] # A global record of all cards played during this hand
        if USE_ML_AGENTS:
            self.players = [
                Player("You"),
                MLAgent("ML Agent 1"),
                MLAgent("ML Agent 2"),
                MLAgent("ML Agent 3")
            ]
        else:
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
        return self.next_action # Return the user's choice after the loop ends

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
            elif event.type == pygame.MOUSEMOTION:
                if not isinstance(self.players[self.active_player], Bot):
                    self.handle_mouse_motion(event.pos)

    def handle_bidding_events(self):
        self.process_events(self.handle_bidding_keydown, self.handle_bidding_click)
        current_player = self.players[self.active_player]
        if isinstance(current_player, Bot):
            bidding_order = [(self.dealer_index + 1 + i) % 4 for i in range(4)]
            current_index = bidding_order.index(self.active_player)
            previous_bids = [(bidding_order[j], self.bids[bidding_order[j]]) for j in range(current_index) if self.bids[bidding_order[j]] is not None]
            bid_card = current_player.bid_selected_card(
                global_played=self.all_played_cards,
                tricks_played=self.tricks_played,
                dealer_index=self.dealer_index,
                previous_bids=previous_bids
            )
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
            pygame.time.delay(500)

    def handle_mouse_motion(self, pos):
        if self.game_state in ['BIDDING', 'PLAYING']:
            self.players[self.active_player].select_card(pos, self.renderer)

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
            card_played = current_player.play_card(
            self.current_trick,
            self.game_mode,
            self.bids,
            self.all_played_cards,
            self.tricks_played,
            self.tricks_won
        )
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
                    self.next_action = 'QUIT'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.waiting_for == 'PLAYING':
                        if self.renderer.is_continue_button_clicked(pos):
                            self.game_state = 'PLAYING'
                            self.waiting_for = None
                    elif self.waiting_for == 'NEW_ROUND':
                        option = self.renderer.get_clicked_option(pos)
                        if option is not None:
                            if option == 0:  # Play Another Round
                                self.dealer_index = (self.dealer_index + 1) % 4
                                self.initialize_game()
                                self.game_state = 'BIDDING'
                                self.waiting_for = None
                            elif option == 1:  # Return to Title Screen
                                self.running = False
                                self.next_action = 'TITLE'
                            elif option == 2:  # Quit Game
                                self.running = False
                                self.next_action = 'QUIT'

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

    def handle_click(self, pos):
        if self.players[self.active_player].select_card(pos, self.renderer):
            self.play_selected_card()

    def handle_bidding_click(self, pos):
        if self.players[self.active_player].select_card(pos, self.renderer):
            self.bid_selected_card()

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
            # Append the trick's cards to the global list:
            for _, card in self.current_trick:
                self.all_played_cards.append(str(card))
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

        if self.game_mode == 'HIGH':
            # Existing high game scoring logic...
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
        else:  # game_mode == 'LOW'
            # Determine the bidding team. In a low game, the bidding team is the player
            # immediately left of the dealer and their partner.
            bidder_index = (self.dealer_index + 1) % 4
            bidding_team = [bidder_index, (bidder_index + 2) % 4]
            opponent_team = [(bidder_index + 1) % 4, (bidder_index + 3) % 4]
            
            bidding_team_tricks = self.tricks_won[bidding_team[0]] + self.tricks_won[bidding_team[1]]
            
            if bidding_team_tricks <= 6:
                score = 6 - bidding_team_tricks
                print(f"Bidding team ({self.players[bidding_team[0]].name} and {self.players[bidding_team[1]].name}) make their contract and score {score} point(s)")
            else:
                score = 2 * (bidding_team_tricks - 6)
                print(f"Bidding team ({self.players[bidding_team[0]].name} and {self.players[bidding_team[1]].name}) went set. Opponents ({self.players[opponent_team[0]].name} and {self.players[opponent_team[1]].name}) score {score} point(s)")


    def draw(self):
        # Clear the screen with black background
        self.screen.fill((0, 0, 0))

        # Determine lead_suit based on game state (used for rendering the hand)
        if self.game_state == 'PLAYING' and self.current_trick:
            lead_suit = self.current_trick[0][1].suit
        else:
            lead_suit = None

        # Always draw the human player's hand (assuming index 0 is the human player)
        human_player = self.players[0]
        self.renderer.draw_hand(human_player.hand, human_player.selected_card, lead_suit)

        # Draw game state-specific elements
        if self.game_state == 'BIDDING':
            self.renderer.draw_game_state_and_player_turn_status(
                self.game_state, self.players[self.active_player].name
            )
            self.renderer.draw_selected_card_info(self.players[self.active_player].selected_card)
            self.renderer.draw_bids(self.bids, self.players)
        elif self.game_state == 'PLAYING':
            self.renderer.draw_game_state_and_player_turn_status(
                self.game_state, self.players[self.active_player].name
            )
            self.renderer.draw_selected_card_info(self.players[self.active_player].selected_card)
            self.renderer.draw_current_trick(self.current_trick, self.players)
            self.renderer.draw_tricks_won(self.tricks_won, self.players)
            self.renderer.draw_players_names(self.players)
        elif self.game_state == 'WAITING':
            if self.waiting_for == 'PLAYING':
                self.renderer.draw_game_state_and_player_turn_status('Bidding Complete', '')
                self.renderer.draw_bids(self.bids, self.players)
                self.renderer.draw_players_names(self.players)
                self.renderer.draw_continue_button()
            elif self.waiting_for == 'NEW_ROUND':
                self.renderer.draw_game_result(self.tricks_won, self.players, self.game_mode, self.granded_player)
                self.renderer.draw_end_game_options()
        # Update the display (batch all drawing operations)
        pygame.display.flip()

    def draw_players_hands(self):
        if len(self.players) != 4:
            print("Error: incorrect number of players")
            return
        # self.renderer.draw_hand(self.players[self.active_player].hand, self.players[self.active_player].selected_card)
        
        human_player = self.players[0]  # Assuming the human player is always at index 0
        self.renderer.draw_hand(human_player.hand, human_player.selected_card)
