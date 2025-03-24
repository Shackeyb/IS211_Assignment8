import random
import argparse
import time

class Die:
    """Represents a six-sided die."""
    def __init__(self, seed=0):
        random.seed(seed)

    def roll(self):
        return random.randint(1, 6)

class Player:
    """Represents a human player."""
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_to_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

class ComputerPlayer(Player):
    """Represents a computer player with a basic strategy."""
    def __init__(self, name="Computer"):
        super().__init__(name)

    def decide(self, turn_total):
        """Computer strategy: hold at min(25, 100 - score) or roll otherwise."""
        if turn_total >= min(25, 100 - self.score):
            return 'h'  # Hold
        return 'r'  # Roll

class PlayerFactory:
    """Factory to create Player instances."""
    @staticmethod
    def create_player(player_type, name):
        if player_type.lower() == "computer":
            return ComputerPlayer(name)
        elif player_type.lower() == "human":
            return Player(name)
        else:
            raise ValueError("Invalid player type. Choose 'human' or 'computer'.")

class Game:
    """Represents the Pig game logic."""
    def __init__(self, player1_type, player2_type):
        self.players = [
            PlayerFactory.create_player(player1_type, "Player 1"),
            PlayerFactory.create_player(player2_type, "Player 2"),
        ]
        self.die = Die()
        self.current_player_index = 0

    def switch_turn(self):
        """Switch to the next player's turn."""
        self.current_player_index = 1 - self.current_player_index

    def play_turn(self, player):
        """Handles a single player's turn."""
        turn_total = 0
        print(f"\n{player.name}'s turn!")

        while True:
            roll = self.die.roll()
            print(f"{player.name} rolled a {roll}.")

            if roll == 1:
                print("Rolled a 1! No points earned this turn.")
                break
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}, Current score: {player.score}")

                # Handle computer decision-making
                if isinstance(player, ComputerPlayer):
                    decision = player.decide(turn_total)
                    print(f"{player.name} chooses to {'Hold' if decision == 'h' else 'Roll'}.")
                else:
                    decision = input("Roll again (r) or Hold (h)? ").strip().lower()

                if decision == 'h':
                    player.add_to_score(turn_total)
                    break

    def check_winner(self):
        """Check if any player has won the game."""
        for player in self.players:
            if player.score >= 100:
                print(f"\n{player.name} wins with {player.score} points!")
                return True
        return False

    def start(self):
        """Starts the game loop."""
        print("Welcome to Pig!")
        while True:
            current_player = self.players[self.current_player_index]
            self.play_turn(current_player)

            if self.check_winner():
                break

            self.switch_turn()

class TimedGameProxy(Game):
    """Proxy that enforces a one-minute time limit."""
    def __init__(self, player1_type, player2_type):
        super().__init__(player1_type, player2_type)
        self.start_time = time.time()

    def start(self):
        """Starts the game loop with a time limit."""
        print("Welcome to Timed Pig! You have 1 minute to win.")

        while True:
            if time.time() - self.start_time >= 60:
                self.declare_winner()
                break

            current_player = self.players[self.current_player_index]
            self.play_turn(current_player)

            if self.check_winner():
                break

            self.switch_turn()

    def declare_winner(self):
        """Determines the winner if time runs out."""
        player1, player2 = self.players
        if player1.score > player2.score:
            print(f"\nTime's up! {player1.name} wins with {player1.score} points!")
        elif player2.score > player1.score:
            print(f"\nTime's up! {player2.name} wins with {player2.score} points!")
        else:
            print("\nTime's up! It's a tie!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the game of Pig.")
    parser.add_argument("--player1", choices=["human", "computer"], required=True, help="Type of Player 1 (human/computer)")
    parser.add_argument("--player2", choices=["human", "computer"], required=True, help="Type of Player 2 (human/computer)")
    parser.add_argument("--timed", action="store_true", help="Enable timed mode")

    args = parser.parse_args()

    if args.timed:
        game = TimedGameProxy(args.player1, args.player2)
    else:
        game = Game(args.player1, args.player2)

    game.start()