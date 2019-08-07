from random import choice

def is_valid_place(size, board, x, y):
    if x < 0 or x > size - 1:
        return False
    if y < 0 or y > size - 1:
        return False
    if board[x][y] == minesweeper_map.BOMB:
        return False
    return True

class minesweeper_map():

    EMPTY = 0
    BOMB = 9

    r_nums = [i for i in range(10)]

    def __init__(self, size, bombs):
        self.board_size = size
        self.board = self.get_blank_board(size)
        self.add_bombs_to_board(bombs)
        self.add_numbers_to_board()

    def __call__(self):
        self.print_board()

    def get_blank_board(self, size):
        return [[self.EMPTY for _ in range(size)] for _ in range(size)]

    def add_bombs_to_board(self, bombs):
        b_left = bombs
        while b_left > 0:
            for row in self.board:
                for i in range(len(row)):
                    if choice(self.r_nums) == 0:
                        row[i] = self.BOMB
                        b_left -= 1
                        if b_left == 0:
                            return

    def get_piece_at_position(self, x, y):
        return self.board[x][y]

    def place_on_board(self,x, y, p):
        self.board[x][y] = p

    def add_numbers_to_board(self):
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[row_index])):
                if self.get_piece_at_position(row_index, col_index) == self.BOMB:
                    for i in range(3):
                        for j in range(3):
                            if is_valid_place(self.board_size, self.board, row_index - 1 + i, col_index - 1 + j):
                                self.place_on_board(row_index - 1 + i, col_index - 1 + j,
                                                    self.get_piece_at_position(row_index - 1 + i, col_index - 1 + j) + 1)

    def print_board(self):
        for r in self.get_board():
            print(r)

    def get_board_size(self):
        return self.board_size

    def get_board(self):
        return self.board