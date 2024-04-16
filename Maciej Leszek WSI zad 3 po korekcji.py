"""
testy:
dla obu współczynników > 6 tendencja do remisów
dla znacząco różnych współczyników np. 1:8 tendecja do wygranej dla tego o większym współczynniku
"""

import math
import random


class Player:
    def __init__(self, name, symbol, depth: int):
        self.name = name
        self.symbol = symbol
        self.depth = depth

    def minmax(self, state, depth: int, player, players):
        if state.is_the_end() or depth == 0:
            score = Game.count_empty_squares(state)*state.utility()
            return [score, None, None]

        best_score = -math.inf if player == players[0] else math.inf
        best_position_i = None
        best_position_j = None

        for i in range(3):
            for j in range(3):
                if state.board[i][j] == ' ':
                    state.board[i][j] = player.symbol
                    next_player = players[1] if player == players[0] else players[0]
                    next_depth = depth - 1  # our depth is lowering
                    simulation_score = self.minmax(State([row[:] for row in state.board], next_player), next_depth, next_player, players)  # copy of present state.board
                    state.board[i][j] = ' '  # clear current board move

                    if player == players[0]:
                        if simulation_score[0] > best_score:
                            best_score = simulation_score[0]
                            best_position_i = i
                            best_position_j = j
                    else:
                        if simulation_score[0] < best_score:
                            best_score = simulation_score[0]
                            best_position_i = i
                            best_position_j = j

        return [best_score, best_position_i, best_position_j]


class State:
    def __init__(self, board, player):
        self.board = board
        self.player = player  # next move player

    def is_the_end(self):  # is it the end of the game?
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        for row in self.board:
            if ' ' in row:
                return False
        return True # tie


    def utility(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                if self.board[i][0] == 'X':
                    return 1 # X win
                elif self.board[i][0] == 'O':
                    return -1 # O win
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                if self.board[0][i] == 'X':
                    return 1
                elif self.board[0][i] == 'O':
                    return -1
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == 'X':
                return 1
            elif self.board[0][0] == 'O':
                return -1
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == 'X':
                return 1
            elif self.board[0][2] == 'O':
                return -1
        return 0  # draw


class Game:
    def __init__(self, depth_max:int, depth_min:int):
        self.board = [[' ' for _ in range(3)] for _ in range(3)] # blank spaces in the board
        self.players = [Player("Computer MAX", 'X', depth_max), Player("Computer MIN", 'O', depth_min)]
        self.current_player = random.choice(self.players)

    def print_board(self):
        for row in self.board:
            print("|".join(row))
            print("-----")
        print(" ")

    def count_empty_squares(self) -> int:
        count = 0
        for row in self.board:
            count += row.count(' ')
        return count

    def play(self):
        while True:
            self.print_board()
            if self.current_player == self.players[0]:
                print(f"Computer MAX turn (Depth: {depth_max})")
                if self.count_empty_squares() != 9:
                    position_results = self.current_player.minmax(State(self.board, self.players[0]), depth_max, self.players[0], self.players)
                    row = position_results[1]
                    col = position_results[2]
                else:
                    row, col = random.choice([(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' '])
            else:
                print(f"Computer MIN turn (Depth: {depth_min})")
                if self.count_empty_squares() != 9:
                    position_results = self.current_player.minmax(State(self.board, self.players[1]), depth_min, self.players[1], self.players)
                    row = position_results[1]
                    col = position_results[2]
                else:
                    row, col = random.choice([(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' '])

            self.board[row][col] = self.current_player.symbol

            if State(self.board, self.players[0]).is_the_end():
                self.print_board()
                winner = State(self.board, self.players[0]).utility()
                if winner == 1:
                    print("Game over. Computer MAX wins!")
                elif winner == -1:
                    print("Game over. Computer MIN wins!")
                else:
                    print("Game over. It's a tie.")
                break

            self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]


if __name__ == "__main__":
    while True:
        try:
            depth_max = int(input("Enter the depth for Computer MAX: "))
            if depth_max > 0:
                break
            else:
                print("Depth must be a positive integer greater than 0. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            depth_min = int(input("Enter the depth for Computer MIN: "))
            if depth_min > 0:
                break
            else:
                print("Depth must be a positive integer greater than 0. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    game = Game(depth_max, depth_min)
    game.play()