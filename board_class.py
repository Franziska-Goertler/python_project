import numpy as np

#Hier wird das Spielfeld definiert. 

class Board:
	##Spielgröße, zwei Spieler...
    # constants
    BOARD_WIDTH = 5
    BOARD_HEIGHT = 3
    BLACK = -1
    WHITE = 1

    def __init__(self):
        self.board = np.zeros((self.BOARD_WIDTH, self.BOARD_HEIGHT),  dtype='i1')##füttere das Spielfeld mit nullern. Nur ein Byte groß.
        self.move_count = 0

##Brett wird jetzt als Zahl dargestellt. Drei Zustände pro Feld, schwarz, weiß oder leer. 
    def hash(self):
        hash = int(0)
        power = 1
        for row_index in range(self.BOARD_HEIGHT):
            for column_index in range(self.BOARD_WIDTH):
                value = int(self.board[column_index, row_index])
                hash += int((value+1)*power)
                power *= 3
        return hash

##Macht das gleiche wie Hash, nur Brett links und rechts gespiegelt. Braucht man in Brute force. Weil da die perfekte Lösung gesucht werd, hier werden alle Spielzüge durchgegangen und damit spaart man sich einiges. 
    def hash_flipped(self):
        hash = int(0)
        power = 1
        for row_index in range(self.BOARD_HEIGHT):
            for column_index in range(self.BOARD_WIDTH).__reversed__():
                value = int(self.board[column_index, row_index])
                hash += int((value+1)*power)
                power *= 3
        return hash

##Macht aus den gespeicherten Zahlen wieder ein Spielfeld, das man anschauen kann. 
    def unhash(self, h):
        moves = 0
        for row_index in range(self.BOARD_HEIGHT):
            for column_index in range(self.BOARD_WIDTH):
                h, remainder = divmod(h, 3)
                self.board[column_index, row_index] = remainder-1
                moves += remainder != 1
        self.move_count = moves

##Prüfe, ob schon ein Spieler gewonnen hat. Dies muss waagrecht, senkrecht und die zwei Diagonalen geprüft werden.
    def check_winner(self, player):
        WW = 3
        # check columns
        # print("columns")
        for column_index in range(self.BOARD_WIDTH):
            d = self.board[column_index, :]
            for start_row in range(self.BOARD_HEIGHT-WW+1):
                a = d[start_row:start_row+WW]
                #print((column_index, start_row, a))
                if all(a == player):
                    return True
        # check rows
        # print("rows")
        for row_index in range(self.BOARD_HEIGHT):
            row = self.board[:, row_index]
            for start_column in range(self.BOARD_WIDTH-WW+1):
                a = row[start_column:start_column+WW]
                #print((row_index, start_column, a))
                if all(a == player):
                    return True

        # check lower_left to upper_right
        #print("lower_left to upper_right")
        for column_index in range(-self.BOARD_WIDTH+WW+1, self.BOARD_WIDTH-WW+1):
            d = np.diagonal(self.board, -column_index)
            #print((column_index, len(d), list(d)))
            for start_row in range(len(d)-WW+1):
                a = d[start_row:start_row+WW]
                #print((column_index, start_row, list(a)))
                if all(a == player):
                    return True

        # check upper_left to lower_right
        #print("check upper_left to lower_right")
        __b = np.fliplr(self.board)
        for column_index in range(-self.BOARD_WIDTH+WW+1, self.BOARD_WIDTH-WW+1):
            d = np.diagonal(__b, -column_index)
            #print((column_index, len(d), list(d)))
            for start_row in range(len(d)-WW+1):
                a = d[start_row:start_row+WW]
                #print((column_index, start_row, list(a)))
                if all(a == player):
                    return True

        return False

    def place(self, column_index, player):
        for row_index in range(self.BOARD_HEIGHT):
            if self.board[column_index, row_index] == 0:
                self.move_count += 1
                self.board[column_index, row_index] = player
                return True
        return False

##alten Zug entfernen.
    def undo(self, column_index):
        self.move_count -= 1
        column = self.board[column_index, :]
        index = next((idx for idx, val in np.ndenumerate(column) if val == 0), None)
        if index == None:
            index = self.BOARD_HEIGHT
        else:
            index = index[0]
        self.board[column_index, index-1] = 0

##Spielsymbol belegen.
    def get_symbol(self, value):
        if value == self.BLACK:
            return 'X'
        elif value == self.WHITE:
            return 'O'
        else:
            return '.'

##Ausgabe des Spielfelds.
    def __str__(self):
        s = ""
        s += "Moves: " + str(self.move_count) + '\n'
        for row_index in range(self.BOARD_HEIGHT).__reversed__():
            row = self.board[:, row_index]
            row = map(lambda x: self.get_symbol(x), row)
            s += str(row_index) + ': ' + ' | '.join(row) + '\n'
        c = range(self.BOARD_WIDTH)
        c = map(str, c)
        c = '   ' + ' | '.join(c)

        s += c
        return s
