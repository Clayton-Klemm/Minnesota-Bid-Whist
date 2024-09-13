import os

def load_card_art():
    card_art = {}
    card_dir = os.path.join(os.path.dirname(__file__), 'assets', 'cards')
    for filename in os.listdir(card_dir):
        if filename.endswith('.txt'):
            card_name = filename.replace('.txt', '')
            with open(os.path.join(card_dir, filename), 'r', encoding='utf-8') as file:
                card_art[card_name] = file.read()
    return card_art
