
from utils import KEYDICT, coordinates_to_board_position, in_board
import pygame

class Piece():
    def __init__(self, pos, color, board):
        self.position = pos
        self.color = color
        self.selected = False
        self.move_count = 0
        self.movelist = []
        self.board = board
        self.coords = coordinates_to_board_position(self.position)

    def CanTake(self, pos):
        for p in self.board.all_pieces():
            if tuple(p.position) == tuple(pos) and p.color != self.color:
                if self.moves(self.board) != None:
                    if tuple(pos) in self.moves(self.board):
                        return True

    def MoveTo(self,board, coords):
        if self.moves(self.board) != None:
            if tuple(coords) in self.moves(board):
                if not self.board.is_occupied(coords):
                    self.position = coords
                    board.move_count += 1
                    self.move_count += 1
                else:
                    self.Take(coords)
    def Delete(self):
        try:
            self.board.whitePieces.remove(self)
        except:
            print("Couldnt remove white piece")
        try:
            self.board.blackPieces.remove(self)
        except:
            print("Couldnt remove black piece")
        try:
            self.board.allPieces.remove(self)
        except:
            print("couldnt remove piece")

    def Take(self, coords):
        if self.board.is_occupied(coords):
            if self.type == "p":
                if self.CanTake(coords):
                    self.board.occupier(coords).Delete()
                    self.position = (coords)
                    self.board.move_count += 1
                    self.move_count += 1

            else:
                if self.CanTake(coords):
                    self.board.occupier(coords).Delete()
                    self.position = coords
                    self.board.move_count += 1
                    self.move_count += 1



class King(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "ki"
        self.imagefile = "/" + str((self.color) + KEYDICT[self.type] + ".png")
        self.value = 100000
        if self.color == "B" :
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/'+self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []

        legalmoves.append((x + 1, y + 1))
        legalmoves.append((x + 1, y - 1))
        legalmoves.append((x + 1, y))
        legalmoves.append((x - 1, y + 1))
        legalmoves.append((x - 1, y - 1))
        legalmoves.append((x - 1, y))
        legalmoves.append((x, y + 1))
        legalmoves.append((x, y - 1))
        legalmoves.append((x, y))
        for mv in legalmoves:
            if self.board.is_occupied(mv):
                if self.board.occupier(mv).color == self.color:
                    delmoves.append(mv)
        for mv in legalmoves:
            if not in_board(mv):
                delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        return legalmoves


class Queen(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "q"
        self.imagefile = "/" + str((self.color) + KEYDICT[self.type] + ".png")
        self.value = 9
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y + i))
            if board.is_occupied((x + i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y - i))
            if board.is_occupied((x + i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y - i))
            if board.is_occupied((x - i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y + i))
            if board.is_occupied((x - i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y))
            if board.is_occupied((x + i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y))
            if board.is_occupied((x - i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y + i))
            if board.is_occupied((x, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y - i))
            if board.is_occupied((x, y - i)):
                break
            else:
                pass
        for mv in legalmoves:
            if board.is_occupied(mv):
                if board.occupier(mv).color == self.color:
                    delmoves.append(mv)
        for mv in legalmoves:
            if not in_board(mv):
                delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Rook(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "r"
        self.imagefile = "/" + str((self.color) + KEYDICT[self.type] + ".png")
        self.value = 5
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y))
            if board.is_occupied((x + i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y))
            if board.is_occupied((x - i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y + i))
            if board.is_occupied((x, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y - i))
            if board.is_occupied((x, y - i)):
                break
            else:
                pass
        for mv in legalmoves:
            if board.is_occupied(mv):
                if board.occupier(mv).color == self.color:
                    delmoves.append(mv)
        for mv in legalmoves:
            if not in_board(mv):
                delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Bishop(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "b"
        self.imagefile = "/" + str((self.color) + KEYDICT[self.type] + ".png")
        self.value = 3
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y + i))
            if board.is_occupied((x + i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y - i))
            if board.is_occupied((x + i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y - i))
            if board.is_occupied((x - i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y + i))
            if board.is_occupied((x - i, y + i)):
                break
            else:
                pass

        for mv in legalmoves:
            if board.is_occupied((mv)):
                if board.occupier(mv).color == self.color:
                    delmoves.append(mv)
        for mv in legalmoves:
            if not in_board(mv):
                delmoves.append(mv)

        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Knight(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "kn"
        self.imagefile = "/" + str((self.color) + KEYDICT[self.type] + ".png")
        self.value = 3
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = [(x + 2, y + 1), (x - 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x + 1, y - 2), (x - 1, y - 2),
                      (x - 2, y - 1), (x + 2, y - 1)]
        delmoves1 = []
        for mv in legalmoves:
            if (mv[0] > 7) or (mv[0] < 0) or (mv[1] > 7) or (mv[1] < 0):
                delmoves1.append(mv)
        for mv in legalmoves:
            if board.is_occupied((mv)):
                if board.occupier(mv).color == self.color:
                    delmoves1.append(mv)
        for mv in legalmoves:
            if not in_board(mv):
                delmoves1.append(mv)
        moves = (set(legalmoves) - set(delmoves1))
        self.movelist = moves
        return moves


class Pawn(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "p"
        self.imagefile = "/" + str((self.color) + KEYDICT[self.type] + ".png")
        self.value = 1
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.imagefile)

    def moves(self,board):
        legalmoves = []
        delmoves = []
        x, y = self.position[0], self.position[1]
        if self.color == "B":
            if self.move_count == 0 and (board.is_occupied((x, y + 1)) == False):
                legalmoves.append((x, y + 2))
            legalmoves.append((x, y + 1))
            legalmoves.append((x + 1, y + 1))
            legalmoves.append((x - 1, y + 1))
        if self.color == "W":
            if self.move_count == 0 and (board.is_occupied((x, y - 1)) == False):
                legalmoves.append((x, y - 2))
            legalmoves.append((x, y - 1))
            legalmoves.append((x + 1, y - 1))
            legalmoves.append((x - 1, y - 1))

        for mv in legalmoves:
            if mv != None:
                if mv[0] != self.position[0]:
                    if self.board.is_occupied(mv) == False:
                        delmoves.append(mv)
                    elif self.board.occupier(mv).color == self.color:
                        delmoves.append(mv)
                else:
                    if self.board.is_occupied(mv) == True:
                        delmoves.append(mv)
        for mv in legalmoves:
            if not in_board(mv):
                delmoves.append(mv)

        moves = (set(legalmoves) - set(delmoves))
        self.movelist = moves
        return moves