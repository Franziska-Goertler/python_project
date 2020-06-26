import brute_force
import neural_network
import random_player
import board_class
import perfect_lookup

#brute_force.solve_and_save()##Speichere die Ergebnisse der perfekten Lösungen.
#board, solved_boards = brute_force.load()
boards, results, shape = brute_force.load_and_reshape()
neural_network.fit_neural_network(boards, results, shape)

##Hier können verschiedene Spielmodi ausgewählt werden. Zufällig oder so, dass der Pc den besten Zug macht. 
#ai = random_player.RandomPlayer()
#ai = perfect_lookup.PerfectLookup()
board = board_class.Board()
ai = neural_network.NeuralNetworkPlayer((board.BOARD_WIDTH, board.BOARD_HEIGHT))

##Spielzüge werden gespeichert
last_player_move = []
last_ai_move = []

##Kommunikation zur Spielzugdurchführung. 
while (True):
    print(board)
    choice = input(
        "Input next move (e.g.: 0 for first column, 2 for third column) or u for undo or x for exit\n")
    if choice == 'x':
        break
    elif choice == 'u':
        if len(last_player_move) > 0:
            board.undo(last_ai_move.pop())
            board.undo(last_player_move.pop())
        else:
            print('Cannot undo - no previous moves')
    else:
        choice = int(choice)
        if board.place(choice, board.WHITE):
            last_player_move.append(choice)
            if board.check_winner(board.WHITE):
                print(board)
                print('Player wins')
                input("Press Enter to continue...")
            elif board.move_count == board.BOARD_HEIGHT*board.BOARD_WIDTH:
                print(board)
                print('Game ends in draw')
                input("Press Enter to continue...")
            ai_move = ai.place(board, board.BLACK)
            if ai_move == None:
                print('Computer does not know what to do - game cancelled')
                input("Press Enter to continue...")
            else:
                print('Computer move: ' + str(ai_move))
                last_ai_move.append(ai_move)
            if board.check_winner(board.BLACK):
                print(board)
                print('Computer wins')
                input("Press Enter to continue...")
        else:
            print('Move @ column ' + choice + ' is not allowed')

print('end')
