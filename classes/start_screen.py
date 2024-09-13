import pygame
import sys

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 56)
        self.small_font = pygame.font.Font(None, 50)
        self.background_color = (0, 0, 0)  # Black background
        self.text_color = (0, 255, 0)  # Green text
        self.highlight_color = (0, 50, 0)  # Dim green for highlighted buttons
        self.options = ["Start Game", "Settings", "Exit"]
        self.selected_option = 0

    def draw(self):
        self.screen.fill(self.background_color)
        title_surface = self.font.render("Minnesota Whist!", True, self.text_color)
        title_rect = title_surface.get_rect(center=(400, 200))
        self.screen.blit(title_surface, title_rect)
        
        for index, option in enumerate(self.options):
            if index == self.selected_option:
                # Draw highlighted background
                highlight_rect = pygame.Rect(200, 300 + index * 50 - 20, 400, 50)
                pygame.draw.rect(self.screen, self.highlight_color, highlight_rect)
                option_surface = self.small_font.render(option, True, self.text_color)
            else:
                option_surface = self.small_font.render(option, True, self.text_color)
            option_rect = option_surface.get_rect(center=(400, 300 + index * 50))
            self.screen.blit(option_surface, option_rect)
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Start Game
                            running = False
                        elif self.selected_option == 1:  # Settings
                            print("Settings selected")
                        elif self.selected_option == 2:  # Exit
                            pygame.quit()
                            sys.exit()

            self.draw()
