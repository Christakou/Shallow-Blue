from pieces import King,Queen,Rook,Bishop,Knight,Pawn
import numpy as np
import copy


class Board():
    def __init__(self):
        self.whitePieces = []
        self.blackPieces = []
        self.move_count = 0
        self.depth = 0
        self.children = []
        self.parent = None
        self.last_move = []

    def all_pieces(self):
        return self.whitePieces + self.blackPieces

    def remove_piece(self, piece):
        if piece.color == 'W':
            self.whitePieces.remove(piece)
        if piece.color == 'B':
            self.blackPieces.remove(piece)

    def __str__(self):
        np.set_printoptions(precision=1)
        np.set_printoptions(suppress=True)
        rep = np.zeros((8,8))
        pieces = self.all_pieces()
        for p in pieces:
            if p.color == "W":
                rep[p.position[1]][p.position[0]] = p.value
            else:
                rep[p.position[1]][p.position[0]] = -p.value
        return str(rep)

    def clear(self):
        self.whitePieces = []
        self.blackPieces = []
        self.allPieces = []
        self.score = 0
        self.move_count = 0

    def get_score(self):
        rep = np.zeros((8, 8))
        pieces = self.all_pieces()
        for p in pieces:
            if p.color == "W":
                rep[p.position[1]][p.position[0]] = p.value
            else:
                rep[p.position[1]][p.position[0]] = -p.value
        self.score = rep.sum()
        return rep.sum()

    def copy_state(self,board):
        self.clear()
        for p in board.whitePieces:
            copied_piece = copy.copy(p)
            copied_piece.board = self
            self.whitePieces.append(copied_piece)
        for p in board.blackPieces:
            copied_piece = copy.copy(p)
            copied_piece.board = self
            self.blackPieces.append(copied_piece)
        self.move_count = int(board.move_count)
        board.children.append(self)
        self.parent = board
        self.depth = board.depth+1


    def is_occupied(self,pos):
        for p in self.all_pieces():
            if tuple(p.position) == tuple(pos):
                return True
        else:
            return False


    def occupier(self,pos):
        for p in self.all_pieces():
            if tuple(p.position) == tuple(pos):
                return p

    def initialize(self):
        self.move_count = 0
        King((4, 7), "W", self)
        King((4, 0), "B", self)
        Queen((3, 7), "W", self)
        Queen((3, 0), "B", self)
        Bishop((2, 7), "W", self)
        Bishop((5, 7), "W", self)
        Bishop((2, 0), "B", self)
        Bishop((5, 0), "B", self)
        Knight((1, 7), "W", self)
        Knight((6, 7), "W", self)
        Knight((6, 0), "B", self)
        Knight((1, 0), "B", self)
        Rook((0, 7), "W", self)
        Rook((7, 7), "W", self)
        Rook((0, 0), "B", self)
        Rook((7, 0), "B", self)
        for a in range(8):
            Pawn((a, 1), "B", self)
            Pawn((a, 6), "W", self)
