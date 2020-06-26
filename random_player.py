from numpy import random
import numpy as np

##einfach einen zufälligen Zug machen.

class RandomPlayer():
    def __init__(self):
        pass

    def place(self, board, player):
        moves = np.arange(board.BOARD_WIDTH)
        random.shuffle(moves)
        for move in moves:
            if board.place(move, player):##gibt true zurück, wenn es erlaubt ist, hier was zu setzen. 
                return move
        return None
