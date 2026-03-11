from models.player import Player
from models.symbol import Symbol
from models.game_status import GameStatus
from game import Game
from observers.scoreboard import Scoreboard


def main():
    name1 = input("Enter Player 1 name (X): ")
    name2 = input("Enter Player 2 name (O): ")

    player1 = Player(name1, Symbol.X)
    player2 = Player(name2, Symbol.O)

    board_size = int(input("Enter board size (e.g. 3): "))

    game = Game(player1, player2, board_size)

    scoreboard = Scoreboard()
    game.add_observer(scoreboard)

    while game.status == GameStatus.IN_PROGRESS:
        game.board.print_board()
        print(f"\n{game.current_player.name}'s turn ({game.current_player.symbol.get_char()})")

        try:
            row = int(input("Enter row: "))
            col = int(input("Enter col: "))
        except ValueError:
            print("Invalid input. Enter numbers only.")
            continue

        result = game.make_move(row, col)
        if result is False:
            print("Invalid move. Try again.")
            continue

    game.board.print_board()

    if game.winner:
        print(f"\n{game.winner.name} wins!")
    else:
        print("\nIt's a draw!")

    scoreboard.print_scores()


if __name__ == "__main__":
    main()
