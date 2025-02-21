import pygame
from classes.game import Game
from classes.start_screen import StartScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Minnesota Whist")
    
    while True:
        start_screen = StartScreen(screen)
        choice = start_screen.run()
        if choice == 2:  # Exit
            break
        elif choice == 0:  # Start Game
            game = Game(screen)
            result = game.run()
            if result == 'QUIT':
                break
            elif result == 'TITLE':
                continue  # Return to title screen
        elif choice == 1:  # Settings
            print("Settings selected")  # Placeholder for future settings
    pygame.quit()

if __name__ == "__main__":
    main()