import brute_force
#import numpy as np
from numpy import random


class PerfectLookup():
    def __init__(self):
        _, solved_boards = brute_force.load()##Lade die gelösten Bretter. 
        self.solved_boards = solved_boards

    def place(self, board, player):
        best_result_moves = []
        best_result = -1  # loss
        for move in range(board.BOARD_WIDTH):
            if board.place(move, player):
                h = board.hash()
                if h in self.solved_boards:
                    r = self.solved_boards[h]
                    if player == board.BLACK:##Kehre Resultat um, wenn ich schwarz bin.
                        r = -r
##Speichere alle Züge ab, die zum besten Ergebnis führen. 
                    if r == -1 & best_result == -1:
                        best_result_moves.append(move)
                    elif r == 0 & best_result <= 0:
                        if best_result < r:
                            best_result_moves.clear()##Schmeiße alle Züge weg, die zu einem schlechteren Ergebnis führen. 
                            best_result = r
                        best_result_moves.append(move)
                    elif r == 1:
                        if best_result < r:
                            best_result_moves.clear()
                            best_result = r
                        best_result_moves.append(move)
#Wenn der Mensch unperfekt spielt, dann treten Situationen auf, die nicht bei den gelösten Brettern dabei sind. Behandle den aktuellen Zug als Untenschieden.
                elif best_result < 1:
                    if best_result == -1:
                        best_result = 0
                        best_result_moves.clear()
                    best_result_moves.append(move)
                board.undo(move)
        if len(best_result_moves) > 0:##Wenn ich einen besten Zug gefunden hab, dann mache einen der besten Züge zufällig. 
            random.shuffle(best_result_moves)
            move = best_result_moves[0]
            board.place(move, player)
            return move
        else:
            return None
