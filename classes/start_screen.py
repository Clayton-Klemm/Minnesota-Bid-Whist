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
        # Store rectangles for hover and click detection
        self.option_rects = []

    def draw(self):
        self.screen.fill(self.background_color)
        title_surface = self.font.render("Minnesota Whist!", True, self.text_color)
        title_rect = title_surface.get_rect(center=(400, 200))
        self.screen.blit(title_surface, title_rect)
        
        # Reset option_rects for this frame
        self.option_rects = []
        
        for index, option in enumerate(self.options):
            # Render the text surface
            option_surface = self.small_font.render(option, True, self.text_color)
            option_rect = option_surface.get_rect(center=(400, 300 + index * 50))
            
            # Create a slightly larger hitbox for hover/click detection
            hitbox_rect = pygame.Rect(200, 300 + index * 50 - 20, 400, 50)
            self.option_rects.append(hitbox_rect)
            
            if index == self.selected_option:
                # Draw highlighted background
                pygame.draw.rect(self.screen, self.highlight_color, hitbox_rect)
            
            # Draw the option text
            self.screen.blit(option_surface, option_rect)
        
        pygame.display.flip()

    def update_selection(self, pos):
        """Update selected_option based on mouse position."""
        for index, rect in enumerate(self.option_rects):
            if rect.collidepoint(pos):
                self.selected_option = index
                return
        # Optional: If mouse is not over any option, keep current selection
        # Alternatively, set to -1 or None if you want no selection when not hovering

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 2  # Exit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.selected_option  # Return 0 for Start Game, 1 for Settings, 2 for Exit
                elif event.type == pygame.MOUSEMOTION:
                    # Update selection based on hover
                    self.update_selection(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a click occurred on the selected option
                    pos = event.pos
                    for index, rect in enumerate(self.option_rects):
                        if rect.collidepoint(pos):
                            return index  # Return the clicked option

            self.draw()
        return None  # Fallback, though unlikely to be reached