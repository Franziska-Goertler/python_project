import board_class
from enum import Enum
import pickle
import numpy


def load():
    board = board_class.Board()
    path = "solved_boards_width_" + \
        str(board.BOARD_WIDTH) + "_height_" + \
        str(board.BOARD_HEIGHT) + ".pickle"
    pickle_in = open(path, "rb")
    solved_boards = pickle.load(pickle_in)
    pickle_in.close()
    return (board, solved_boards)

##Wird benutzt für das neuronale Netz. Lerne aus der Perspektive des weißen Spielers.
def load_and_reshape():
    (board, solved_boards) = load()
    count = len(solved_boards)
    size = board.BOARD_WIDTH*board.BOARD_HEIGHT
    boards = numpy.zeros((count, size))
    results = numpy.zeros(count)
    #results = numpy.zeros((count, 3))
    for index, (h, player) in enumerate(solved_boards.items()):
        board.unhash(h)
        sign = 1 if board.move_count % 2 == 0 else -1
        # print(player)
        # print(board)
        results[index] = (player*sign+1)/2##Projeziere auf weiß, Ergebnis ist zwischen null und eins. 
        #results[index, player+1] = 1
        # print(results[:index+1])
        boards[index, :] = (board.board*sign).flatten()##Stelle Board als Spalte dar.
        #print(boards[:index+1, :])
    return (boards, results, (board.BOARD_WIDTH, board.BOARD_HEIGHT))

##Ruft solving auf und speichert das in eine Datei. Pickle ist eine Bibliothek wie Numpy. Speichert die Variablen.
def solve_and_save():
    board, solved_boards = solving()

    print("solved_boards: " + str(solved_boards.__len__()))
    path = "solved_boards_width_" + \
        str(board.BOARD_WIDTH) + "_height_" + \
        str(board.BOARD_HEIGHT) + ".pickle"
    pickle_out = open(path, "wb")
    pickle.dump(solved_boards, pickle_out)
    pickle_out.close()
    print('Saved to path "' + path + '"')

##Funktion ruft brute_force auf und probiert alle zweiten Züge aus, PC ist der zweite Spieler
def solving():
    solved_boards = {}
    board = board_class.Board()
    for column_index in range(board.BOARD_WIDTH):
        board2 = board_class.Board()
        board2.place(column_index, board2.WHITE)
        # print(board2)
        # print((column_index, board2.hash(), board2.hash_flipped(), board2.move_count))
        r = brute_force(board2, board2.BLACK, solved_boards)
        print("Column: " + str(column_index) +
              " - Winner: " + board2.get_symbol(r))
    return (board, solved_boards)


class BestResult(Enum):
    NoLegalMoveDetected = 0
    Loss = 1
    Draw = 2
    # Win = 3 actually never used since immediately returns

##Versuche, immer zu gewinnen. 
def brute_force(board, player, solved_boards):##habe aktuelle Position, bin der aktuelle Spieler, habe information über perfekte Lösungen.
    h = board.hash()##Wandle Brett in eine (große) Zahl um. 
    if h in solved_boards:##Schaue nach, wer gewinnt, wenn ich das schon gesehe habe. 
        return solved_boards[h]
    h2 = board.hash_flipped()
    # print(board)
    best_result = BestResult.NoLegalMoveDetected
    for column in range(board.BOARD_WIDTH):##Wenn ich die Lösung nicht weiß, probiere alle Züge aus. 
        if board.place(column, player):##Darf ich Zug mache, sonst nächster Zug. 
            hh = board.hash()
            hh2 = board.hash_flipped()
            # print(board)
            if board.check_winner(player):##Schaue, ob ich gewonnen habe. 
                # print("Winning player:" + board.get_symbol(player))
                # print(board)
                board.undo(column)##Wenn ich gewinne, mache Zug rückgängig und schreibe das in die Lösungen rein. 
                solved_boards[h] = player
                solved_boards[h2] = player
                solved_boards[hh] = player
                solved_boards[hh2] = player
                return player 
            else:
                result = brute_force(board, player*-1, solved_boards)##Rekursiver Aufruf. 
                solved_boards[hh] = result
                solved_boards[hh2] = result
                # print(board)
                board.undo(column)
                # print(board)
                # print("Winning player:" + board.get_symbol(result))
                if result == -player:
                    best_result = BestResult.Loss if best_result == BestResult.NoLegalMoveDetected else best_result ##Merke mir, was der beste Zug ist, weil unentschieden ist besser als verlieren. 
                    continue
                elif result == player:##Ich habe zwar keinen Gewinnzug direkt, aber der Gegner kann meinen Sieg nicht mehr verhindern, egal was er macht. 
                    solved_boards[h] = player
                    solved_boards[h2] = player
                    return player
                else:##Unenschieden
                    best_result = BestResult.Draw
                    continue

##Alle Züge sind jetzt ausprobiert. Habe keinen Gewinnzug gefunden. 
    p = None
    if best_result == BestResult.Loss: ##Gib aus, ob verlieren oder untentschieden das beste mögliche Ergebnis ist. (Wenn beide Spiele perfekt spielen)
        p = player*-1
    else:
        p = 0
    # print("Winning player:" + board.get_symbol(p))
    solved_boards[h] = p
    solved_boards[h2] = p
    # print(board)
    return p
