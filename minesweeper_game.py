import pygame

import minesweeper_map as mm

pygame.init()

class minesweeper_tile():
    def __init__(self, v, f=False, h=True):
        self.value = v
        self.flag = f
        self.hidden = h

    def set_value(self, v):
        self.value = v

    def set_flag(self):
        self.flag = not self.flag

    def set_hidden(self):
        self.hidden = not self.hidden

class minesweeper_game():

    TILE_SIZE = 20
    LEFT_MOUSE_BUTTON, RIGHT_MOUSE_BUTTON = 1, 3

    game_over = False
    win = False

    img = pygame.image.load('minesweeper_icons.png')
    images = []
    for i in range(12):
        images.append(img.subsurface(TILE_SIZE*i, 0, TILE_SIZE, TILE_SIZE))

    def __init__(self, size, bombs):
        self.mmap = mm.minesweeper_map(size, bombs)
        self.board_size = self.mmap.get_board_size()
        self.create_tile_board()
        self.create_window(self.board_size, bombs)
        self.run_game()

    def create_tile_board(self):
        self.tile_board = [[minesweeper_tile(0) for _ in range(self.mmap.get_board_size())]
                           for _ in range(self.mmap.get_board_size())]
        for r in range(len(self.mmap.get_board())):
            for c in range(len(self.mmap.get_board()[r])):
                self.tile_board[r][c].value = self.mmap.get_board()[r][c]

    def create_window(self, size, bombs):
        self.window = pygame.display.set_mode((size*self.TILE_SIZE, size*self.TILE_SIZE))
        pygame.display.set_caption('%s Bombs Total' % (bombs))

    def run_game(self):
        running = True
        while running:
            pygame.time.delay(int(1000/60))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_interaction(e)
            self.draw_window()
            if self.game_over:
                pygame.display.set_caption('Game Over')
                pygame.time.delay(1000)
                running = False
            if self.win:
                pygame.display.set_caption('You\'ve Won!')
                pygame.time.delay(1000)
                running = False
        pygame.quit()

    def handle_mouse_interaction(self, e):
        x, y = int(pygame.mouse.get_pos()[0]/self.TILE_SIZE), int(pygame.mouse.get_pos()[1]/self.TILE_SIZE)
        corr_tile = self.tile_board[x][y]
        if corr_tile.hidden:
            if e.button == self.LEFT_MOUSE_BUTTON:
                self.handle_hidden(x, y)
                if self.get_win():
                    self.win = True
            elif e.button == self.RIGHT_MOUSE_BUTTON:
                self.tile_board[x][y].set_flag()
        if corr_tile.value == mm.minesweeper_map.BOMB:
            if e.button == self.LEFT_MOUSE_BUTTON:
                self.game_over = True

    def get_win(self):
        for row in self.tile_board:
            for cell in row:
                if cell.hidden and cell.value is not self.mmap.BOMB:
                    return False
        return True

    def handle_hidden(self, x, y):
        self.tile_board[x][y].set_hidden()
        if mm.is_valid_place(self.board_size, self.mmap.get_board(), x-1, y):
            if self.tile_board[x-1][y].hidden and self.tile_board[x][y].value is 0:
                self.handle_hidden(x-1, y)
        if mm.is_valid_place(self.board_size, self.mmap.get_board(), x+1, y):
            if self.tile_board[x+1][y].hidden and self.tile_board[x][y].value is 0:
                self.handle_hidden(x+1, y)
        if mm.is_valid_place(self.board_size, self.mmap.get_board(), x, y-1):
            if self.tile_board[x][y-1].hidden and self.tile_board[x][y].value is 0:
                self.handle_hidden(x, y-1)
        if mm.is_valid_place(self.board_size, self.mmap.get_board(), x, y+1):
            if self.tile_board[x][y+1].hidden and self.tile_board[x][y].value is 0:
                self.handle_hidden(x, y+1)

    def draw_window(self):
        for r in range(len(self.tile_board)):
            for c in range(len(self.tile_board[r])):
               c_tile = self.tile_board[r][c]
               if c_tile.flag:
                   self.window.blit(self.images[11], (r*self.TILE_SIZE, c*self.TILE_SIZE))
               elif c_tile.hidden:
                   self.window.blit(self.images[10], (r*self.TILE_SIZE, c*self.TILE_SIZE))
               else:
                   self.window.blit(self.images[self.tile_board[r][c].value], (r*self.TILE_SIZE, c*self.TILE_SIZE))
        pygame.display.update()