from utils import KEYDICT, coordinates_to_board_position, in_board
import pygame

class Piece():
    def __init__(self, pos, color, board, type):
        self.type = type
        self.position = pos
        self.color = color
        self.selected = False
        self.move_count = 0
        self.movelist = []
        self.board = board
        self.coords = coordinates_to_board_position(self.position)
        self.image_path = "/" + str((self.color) + KEYDICT[self.type] + ".png")
    def __str__(self):
        return f'{self.color}{self.position}'
    def can_take(self, pos):
        for p in self.board.all_pieces():
            if tuple(p.position) == tuple(pos) and p.color != self.color:
                if self.moves(self.board) != None:
                    if tuple(pos) in self.moves(self.board):
                        return True
    def moves(self, board):
        pass

    def move_to(self, pos):
        if self.moves(self.board) != None:
            if tuple(pos) in self.moves(self.board):
                self.board.last_move = [self.position, pos]
                if not self.board.is_occupied(pos):
                    self.position = pos
                    self.board.move_count += 1
                    self.move_count += 1
                else:
                    self.take(pos)
                
    def delete(self):
        try:
            self.board.whitePieces.remove(self)
        except:
            print("Couldn't remove white piece")
        try:
            self.board.blackPieces.remove(self)
        except:
            print("Couldn't remove black piece")
        try:
            self.board.allPieces.remove(self)
        except:
            print("Couldn't remove piece")

    def take(self, pos):
        if self.board.is_occupied(pos):
            if self.type == "p":
                if self.can_take(pos):
                    self.board.occupier(pos).delete()
                    self.position = (pos)
                    self.board.move_count += 1
                    self.move_count += 1

            else:
                if self.can_take(pos):
                    self.board.occupier(pos).delete()
                    self.position = pos
                    self.board.move_count += 1
                    self.move_count += 1



class King(Piece):

    def __init__(self, pos, color, board, type="ki"):
        Piece.__init__(self, pos, color, board, type)
        self.value = 100000
        if self.color == "B" :
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.image_path)

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

    def __init__(self, pos, color, board, type="q"):
        Piece.__init__(self, pos, color, board, type)
        self.value = 9
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.image_path)

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

    def __init__(self, pos, color, board, type="r"):
        Piece.__init__(self, pos, color, board,type=type)
        self.value = 5
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.image_path)

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

    def __init__(self, pos, color, board, type="b"):
        Piece.__init__(self, pos, color, board, type)
        self.value = 3
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.image_path)

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

    def __init__(self, pos, color, board, type="kn"):
        Piece.__init__(self, pos, color, board, type=type)
        self.value = 3
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.image_path)

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

    def __init__(self, pos, color, board, type="p"):
        Piece.__init__(self, pos, color, board, type=type)
        self.value = 1
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load('./assets/' + self.image_path)

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