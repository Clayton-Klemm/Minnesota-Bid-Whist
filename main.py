import pygame
from classes.game import Game
from classes.start_screen import StartScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Minnesota Whist")
    start_screen = StartScreen(screen)
    game = Game(screen)
    # Show the start screen
    start_screen.run()
    # If the start screen exits, start the main game
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
