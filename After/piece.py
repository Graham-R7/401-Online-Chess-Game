import pygame
import os

# Named constants
BOARD_X = 113
BOARD_Y = 113
BOARD_WIDTH = 525
BOARD_HEIGHT = 525
NUM_CELLS = 8
DRAW_OFFSET_X = 4
DRAW_OFFSET_Y = 3

# Load and scale images for pieces
b_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
b_king = pygame.image.load(os.path.join("img", "black_king.png"))
b_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("img", "black_rook.png"))

w_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("img", "white_king.png"))
w_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

B = [pygame.transform.scale(img, (55, 55)) for img in b]
W = [pygame.transform.scale(img, (55, 55)) for img in w]

class Piece:
    img = -1
    rect = (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT)
    startX = BOARD_X
    startY = BOARD_Y

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False

    def isSelected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def draw(self, win, color):
        drawThis = W[self.img] if self.color == "w" else B[self.img]
        x = (DRAW_OFFSET_X - self.col) + round(self.startX + (self.col * self.rect[2] / NUM_CELLS))
        y = DRAW_OFFSET_Y + round(self.startY + (self.row * self.rect[3] / NUM_CELLS))
        if self.selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)
        win.blit(drawThis, (x, y))

    def change_pos(self, pos):
        self.row, self.col = pos

    def __str__(self):
        return f"{self.col} {self.row}"

class Bishop(Piece):
    img = 0
    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []
        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < NUM_CELLS:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break
            djL += 1
        for di in range(i - 1, -1, -1):
            if djR >= 0:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break
            djR -= 1
        # BOTTOM RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, NUM_CELLS):
            if djL < NUM_CELLS:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break
            djL += 1
        for di in range(i + 1, NUM_CELLS):
            if djR >= 0:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break
            djR -= 1
        return moves

class King(Piece):
    img = 1
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True
    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []
        if i > 0:
            if j > 0:
                p = board[i - 1][j - 1]
                if p == 0 or p.color != self.color:
                    moves.append((j - 1, i - 1))
            p = board[i - 1][j]
            if p == 0 or p.color != self.color:
                moves.append((j, i - 1))
            if j < NUM_CELLS - 1:
                p = board[i - 1][j + 1]
                if p == 0 or p.color != self.color:
                    moves.append((j + 1, i - 1))
        if i < NUM_CELLS - 1:
            if j > 0:
                p = board[i + 1][j - 1]
                if p == 0 or p.color != self.color:
                    moves.append((j - 1, i + 1))
            p = board[i + 1][j]
            if p == 0 or p.color != self.color:
                moves.append((j, i + 1))
            if j < NUM_CELLS - 1:
                p = board[i + 1][j + 1]
                if p == 0 or p.color != self.color:
                    moves.append((j + 1, i + 1))
        if j > 0:
            p = board[i][j - 1]
            if p == 0 or p.color != self.color:
                moves.append((j - 1, i))
        if j < NUM_CELLS - 1:
            p = board[i][j + 1]
            if p == 0 or p.color != self.color:
                moves.append((j + 1, i))
        return moves

class Knight(Piece):
    img = 2
    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []
        if i < NUM_CELLS - 2 and j > 0:
            p = board[i + 2][j - 1]
            if p == 0 or p.color != self.color:
                moves.append((j - 1, i + 2))
        if i > 1 and j > 0:
            p = board[i - 2][j - 1]
            if p == 0 or p.color != self.color:
                moves.append((j - 1, i - 2))
        if i < NUM_CELLS - 2 and j < NUM_CELLS - 1:
            p = board[i + 2][j + 1]
            if p == 0 or p.color != self.color:
                moves.append((j + 1, i + 2))
        if i > 1 and j < NUM_CELLS - 1:
            p = board[i - 2][j + 1]
            if p == 0 or p.color != self.color:
                moves.append((j + 1, i - 2))
        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            if p == 0 or p.color != self.color:
                moves.append((j - 2, i - 1))
        if i > 0 and j < NUM_CELLS - 2:
            p = board[i - 1][j + 2]
            if p == 0 or p.color != self.color:
                moves.append((j + 2, i - 1))
        if i < NUM_CELLS - 1 and j > 1:
            p = board[i + 1][j - 2]
            if p == 0 or p.color != self.color:
                moves.append((j - 2, i + 1))
        if i < NUM_CELLS - 1 and j < NUM_CELLS - 2:
            p = board[i + 1][j + 2]
            if p == 0 or p.color != self.color:
                moves.append((j + 2, i + 1))
        return moves

class Pawn(Piece):
    img = 3
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.queen = False
        self.pawn = True
    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []
        try:
            if self.color == "b":
                if i < NUM_CELLS - 1:
                    p = board[i + 1][j]
                    if p == 0:
                        moves.append((j, i + 1))
                    if j < NUM_CELLS - 1:
                        p = board[i + 1][j + 1]
                        if p != 0 and p.color != self.color:
                            moves.append((j + 1, i + 1))
                    if j > 0:
                        p = board[i + 1][j - 1]
                        if p != 0 and p.color != self.color:
                            moves.append((j - 1, i + 1))
                if self.first and i < NUM_CELLS - 2:
                    p = board[i + 2][j]
                    if p == 0 and board[i + 1][j] == 0:
                        moves.append((j, i + 2))
                    elif p != 0 and p.color != self.color:
                        moves.append((j, i + 2))
            else:
                if i > 0:
                    p = board[i - 1][j]
                    if p == 0:
                        moves.append((j, i - 1))
                    if j < NUM_CELLS - 1:
                        p = board[i - 1][j + 1]
                        if p != 0 and p.color != self.color:
                            moves.append((j + 1, i - 1))
                    if j > 0:
                        p = board[i - 1][j - 1]
                        if p != 0 and p.color != self.color:
                            moves.append((j - 1, i - 1))
                if self.first and i > 1:
                    p = board[i - 2][j]
                    if p == 0 and board[i - 1][j] == 0:
                        moves.append((j, i - 2))
                    elif p != 0 and p.color != self.color:
                        moves.append((j, i - 2))
        except Exception:
            pass
        return moves

class Queen(Piece):
    img = 4
    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < NUM_CELLS:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    djL = NUM_CELLS + 1
            djL += 1
        for di in range(i - 1, -1, -1):
            if djR >= 0:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    djR = -1
            djR -= 1
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, NUM_CELLS):
            if djL < NUM_CELLS:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    djL = NUM_CELLS + 1
            djL += 1
        for di in range(i + 1, NUM_CELLS):
            if djR >= 0:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    djR = -1
            djR -= 1
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        for x in range(i + 1, NUM_CELLS):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        for x in range(j + 1, NUM_CELLS):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        return moves

class Rook(Piece):
    img = 5
    def valid_moves(self, board):
        i, j = self.row, self.col
        moves = []
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        for x in range(i + 1, NUM_CELLS):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        for x in range(j + 1, NUM_CELLS):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        return moves
