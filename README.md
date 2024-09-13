# Minnesota Whist Card Game

Welcome to the **Minnesota Whist** card game project! Inspired by the old-school look of early computing systems, this game focuses on simplicity and strategy.


![Minnesota Whist start screen](https://github.com/user-attachments/assets/66ad2418-6ec5-42a6-8dd9-bc9c1c97fc4b)
![Playing screen](https://github.com/user-attachments/assets/01cfaa6a-6118-4c6e-b19a-2dd25a4d92e2)

## Features

- **Bidding Phase**: Players bid on whether they will go "high" or "low" based on their cards.
- **Game Mode**: Depending on the bidding, the game is played in either "HIGH" or "LOW" mode.
- **Trick-taking mechanics**: Players take turns playing cards, and the game follows standard trick-taking rules, where players must follow suit and the highest-ranked card wins the trick.
- **AI Bot Players**: Three bots controlled by the computer will automatically play their turns and handle the bidding process.
- **Endgame Scoring**: The game calculates and displays the score at the end of each round.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Clayton-Klemm/Minnesota-Bid-Whist.git
    cd Minnesota-Bid-Whist
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the game:
    ```bash
    python main.py
    ```

## How to Play

1. **Start the Game**: Begin at the start screen and enter the bidding phase.
2. **Bidding**: Choose a card to place your bid, determining if you’ll aim for "HIGH" (trick-winning) or "LOW" (avoiding tricks).
3. **Playing**: During play, follow suit and make strategic card choices.
4. **Winning**: Teams compete to meet the bidding goals by winning or avoiding tricks. Once all tricks are played, points are awarded, and the winning team is declared.
5. **New Round**: After each game, start a new round and rotate the dealer.

## Controls

- **Arrow Keys**: Navigate through your hand of cards.
- **Enter**: Select a card to bid or play.
- **Mouse Click**: Click to select cards or interact with the interface.

---

Thanks for checking out Minnesota Whist! I designed this project to feel like a blast from the past back when computer usage was a bit more direct and intentional. Enjoy!

## Future Plans

This game is still a work in progress, and I plan to continue refining it and addressing any quirks. Additionally, I aim to use this project for research into incomplete information games (IIGs). I may also explore the possibility of running the game on a Hercules emulator using the JCL compiler.
