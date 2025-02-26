import time
import pygame
from piece import Rook, Knight, Bishop, Queen, King, Pawn

# Named constants
BOARD_X = 113
BOARD_Y = 113
BOARD_WIDTH = 525
BOARD_HEIGHT = 525
NUM_CELLS = 8
DRAW_OFFSET_X = 4
DRAW_OFFSET_Y = 3
CIRCLE_OFFSET_X = 32
CIRCLE_OFFSET_Y = 30
CIRCLE_RADIUS = 34
CIRCLE_WIDTH = 4

class Board:
    rect = (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT)
    startX = BOARD_X
    startY = BOARD_Y

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.ready = False
        self.last = None
        self.copy = True
        self.board = [[0 for _ in range(NUM_CELLS)] for _ in range(rows)]
        
        self._setup_major_pieces(0, "b")
        self._setup_pawns(1, "b")
        self._setup_major_pieces(7, "w")
        self._setup_pawns(6, "w")

        self.p1Name = "Player 1"
        self.p2Name = "Player 2"
        self.turn = "w"
        self.time1 = 900
        self.time2 = 900
        self.storedTime1 = 0
        self.storedTime2 = 0
        self.winner = None
        self.startTime = time.time()

    def _setup_major_pieces(self, row, color):
        """Helper method to place major pieces on a given row."""
        major_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, PieceClass in enumerate(major_pieces):
            self.board[row][col] = PieceClass(row, col, color)

    def _setup_pawns(self, row, color):
        """Helper method to place pawns on a given row."""
        for col in range(NUM_CELLS):
            self.board[row][col] = Pawn(row, col, color)

    def update_moves(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)

    def draw(self, win, color):
        if self.last and color == self.turn:
            y, x = self.last[0]
            y1, x1 = self.last[1]
            xx = (DRAW_OFFSET_X - x) + round(self.startX + (x * BOARD_WIDTH / NUM_CELLS))
            yy = DRAW_OFFSET_Y + round(self.startY + (y * BOARD_HEIGHT / NUM_CELLS))
            pygame.draw.circle(win, (0, 0, 255), (xx + CIRCLE_OFFSET_X, yy + CIRCLE_OFFSET_Y), CIRCLE_RADIUS, CIRCLE_WIDTH)
            xx1 = (DRAW_OFFSET_X - x) + round(self.startX + (x1 * BOARD_WIDTH / NUM_CELLS))
            yy1 = DRAW_OFFSET_Y + round(self.startY + (y1 * BOARD_HEIGHT / NUM_CELLS))
            pygame.draw.circle(win, (0, 0, 255), (xx1 + CIRCLE_OFFSET_X, yy1 + CIRCLE_OFFSET_Y), CIRCLE_RADIUS, CIRCLE_WIDTH)

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win, color)

    def get_danger_moves(self, color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        danger_moves.extend(self.board[i][j].move_list)
        return danger_moves

    def is_checked(self, color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0 and self.board[i][j].king and self.board[i][j].color == color:
                    king_pos = (j, i)
        return king_pos in danger_moves

    def select(self, col, row, color):
        changed = False
        prev = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0 and self.board[i][j].selected:
                    prev = (i, j)

        if self.board[row][col] == 0 and prev != (-1, -1):
            moves = self.board[prev[0]][prev[1]].move_list
            if (col, row) in moves:
                changed = self.move(prev, (row, col), color)
        else:
            if prev == (-1, -1):
                self.reset_selected()
                if self.board[row][col] != 0:
                    self.board[row][col].selected = True
            else:
                if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                    moves = self.board[prev[0]][prev[1]].move_list
                    if (col, row) in moves:
                        changed = self.move(prev, (row, col), color)
                    if self.board[row][col].color == color:
                        self.board[row][col].selected = True
                else:
                    if self.board[row][col].color == color:
                        # Extract castling logic into helper method.
                        self.reset_selected()
                        if not self._attempt_castling(prev, row, col, color):
                            self.board[row][col].selected = True

        if changed:
            self.turn = "b" if self.turn == "w" else "w"
            self.reset_selected()

    def _attempt_castling(self, prev, row, col, color):
        """
        Helper method to handle castling logic.
        Returns True if the castling move is performed, otherwise False.
        """
        piece = self.board[prev[0]][prev[1]]
        if not (hasattr(piece, 'moved') and not piece.moved and getattr(piece, 'rook', False)
                and self.board[row][col].king and col != prev[1] and prev != (-1, -1)):
            return False

        castle = True
        if prev[1] < col:
            for j in range(prev[1] + 1, col):
                if self.board[row][j] != 0:
                    castle = False
                    break
            if castle:
                if self.move(prev, (row, 3), color):
                    return self.move((row, col), (row, 2), color)
        else:
            for j in range(col + 1, prev[1]):
                if self.board[row][j] != 0:
                    castle = False
                    break
            if castle:
                if self.move(prev, (row, 6), color):
                    return self.move((row, col), (row, 5), color)
        return False

    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_mate(self, color):
        return False

    def move(self, start, end, color):
        checkedBefore = self.is_checked(color)
        changed = True
        nBoard = self.board[:]
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False

        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard

        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            changed = False
            nBoard = self.board[:]
            if nBoard[end[0]][end[1]].pawn:
                nBoard[end[0]][end[1]].first = True
            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self.board = nBoard
        else:
            self.reset_selected()

        self.update_moves()
        if changed:
            self.last = [start, end]
            if self.turn == "w":
                self.storedTime1 += (time.time() - self.startTime)
            else:
                self.storedTime2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed
