import pygame
import math
import numpy as np

screensize = (600, 600)
filelocation = "C:/Users/Christiano/Desktop/Shallow Blue"
pygame.init()
screen = pygame.display.set_mode(screensize)
done = False
boardimage = pygame.image.load(filelocation + "/chessboard.png")
boardimage = pygame.transform.scale(boardimage, screensize)
selected_image = pygame.image.load(filelocation + "/Selected.png")
legalmove_image = pygame.image.load(filelocation + "/LegalMove.png")
selected_pos = [8, 8]

IsPieceSelected = False

SelectedPiece = []
MoveCount = 0



class Board():
    def __init__(self, a=None, b=None):
        self.whitePieces = []
        self.blackPieces = []
        self.score = 0

    def GetAllPieces(self):
        return self.whitePieces + self.blackPieces

    def Clear(self):
        self.whitePieces = []
        self.blackPieces = []
        self.allPieces = []
        self.score = 0

    def GetScore(self):
        Score = 0
        for p in self.whitePieces:
            Score += p.value
        for p in self.blackPieces:
            Score -= p.value
        return Score

    def CopyState(self,board):
        state = board.GetAllPieces()
        self.clear()
        for p in board.whitePieces:
            self.whitePieces.append(p)
        for p in board.blackPieces:
            self.blackPieces.append(p)

    def IsOccupied(self,pos):
        for p in self.GetAllPieces():
            if tuple(p.position) == tuple(pos):
                return True
        else:
            return False


    def Occupier(self,pos):
        for p in self.GetAllPieces():
            if tuple(p.position) == tuple(pos):
                return p


def Update():
    screen.blit(boardimage, (0, 0))
    suggestedmvs = []
    for Piece in MainBoard.GetAllPieces():
        Piece.coord = (Piece.position[0] * (screensize[0] / 8.0), Piece.position[1] * (screensize[1] / 8.0))
        screen.blit(pygame.image.load(filelocation + Piece.imagefile), Piece.coord)
        if Piece.selected:
            screen.blit(selected_image, Piece.coord)
            if Piece.moves(MainBoard)!= None:
                for a in Piece.moves(MainBoard): suggestedmvs.append(a)
    for legalmove in suggestedmvs:
        screen.blit(legalmove_image, (legalmove[0] * (screensize[0] / 8.0), legalmove[1] * (screensize[1] / 8.0)))


class Piece(Board):
    global keydict, activePieces, MoveCount

    keydict = {"ki": "King", "kn": "Knight", "r": "Rook", "q": "Queen", "b": "Bishop", "p": "Pawn"}

    def __init__(self, pos, color, board):
        self.position = pos
        self.color = color
        self.selected = False
        self.movecount = 0
        self.movelist = []
        self.board = board
    def CanTake(self, (x, y)):
        for p in self.board.GetAllPieces():
            if tuple(p.position) == tuple((x, y)) and p.color != self.color:
                if self.moves(self.board) != None:
                    if tuple((x, y)) in self.moves(self.board):
                        return True

    def MoveTo(self,board, (x, y)):
        global MoveCount
        if self.moves(self.board) != None:
            if (x, y) in self.moves(board):
                if not self.board.IsOccupied((x, y)):
                    self.position = (x, y)
                    MoveCount += 1
                    self.movecount += 1
                    print(MoveCount)
            else:
                pass

    def Delete(self):
        try:
            self.board.whitePieces.remove(self)
            self.board.blackPieces.remove(self)
        except:
            pass

    def Take(self, (x, y)):
        global MoveCount
        if self.board.IsOccupied((x, y)):
            if self.type == "p":
                if self.CanTake((x, y)):
                    self.board.Occupier((x, y)).Delete()
                    self.position = ((x, y))

            else:
                if self.CanTake((x, y)):
                    self.board.Occupier((x, y)).Delete()
                    self.position = ((x, y))



class King(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "ki"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 10000
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        if self.color == "B" :
            self.board.whitePieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

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
            if self.board.IsOccupied(mv):
                if self.board.Occupier(mv).color == self.color:
                    delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        return legalmoves


class Queen(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "q"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 9
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        if self.color == "B":
            self.board.whitePieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y + i))
            if board.IsOccupied((x + i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y - i))
            if board.IsOccupied((x + i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y - i))
            if board.IsOccupied((x - i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y + i))
            if board.IsOccupied((x - i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y))
            if board.IsOccupied((x + i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y))
            if board.IsOccupied((x - i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y + i))
            if board.IsOccupied((x, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y - i))
            if board.IsOccupied((x, y - i)):
                break
            else:
                pass
        for mv in legalmoves:
            if board.IsOccupied(mv):
                if board.Occupier(mv).color == self.color:
                    delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Rook(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "r"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 5
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        if self.color == "B":
            board.whitePieces.append(self)
        if self.color == "W":
            board.whitePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y))
            if board.IsOccupied((x + i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y))
            if board.IsOccupied((x - i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y + i))
            if board.IsOccupied((x, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y - i))
            if board.IsOccupied((x, y - i)):
                break
            else:
                pass
        for mv in legalmoves:
            if board.IsOccupied(mv):
                if board.Occupier(mv).color == self.color:
                    delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Bishop(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "b"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 3
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        if self.color == "B":
            board.whitePieces.append(self)
        if self.color == "W":
            board.whitePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y + i))
            if board.IsOccupied((x + i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y - i))
            if board.IsOccupied((x + i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y - i))
            if board.IsOccupied((x - i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y + i))
            if board.IsOccupied((x - i, y + i)):
                break
            else:
                pass

        for mv in legalmoves:
            if board.IsOccupied((mv)):
                if board.Occupier(mv).color == self.color:
                    delmoves.append(mv)

        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Knight(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "kn"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 3
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        if self.color == "B":
            board.whitePieces.append(self)
        if self.color == "W":
            board.whitePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self,board):
        x, y = self.position[0], self.position[1]
        legalmoves = [(x + 2, y + 1), (x - 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x + 1, y - 2), (x - 1, y - 2),
                      (x - 2, y - 1), (x + 2, y - 1)]
        delmoves1 = []
        for mv in legalmoves:
            if (mv[0] > 7) or (mv[0] < 0) or (mv[1] > 7) or (mv[1] < 0):
                delmoves1.append(mv)
        for mv in legalmoves:
            if board.IsOccupied((mv)):
                if board.Occupier(mv).color == self.color:
                    delmoves1.append(mv)
        moves = (set(legalmoves) - set(delmoves1))
        self.movelist = moves
        return moves


class Pawn(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "p"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 1
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        if self.color == "B":
            board.whitePieces.append(self)
        if self.color == "W":
            board.whitePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self,board):
        legalmoves = []
        delmoves = []
        x, y = self.position[0], self.position[1]
        if self.color == "B":
            if self.movecount == 0 and (board.IsOccupied((x, y + 1)) == False):
                legalmoves.append((x, y + 2))
            legalmoves.append((x, y + 1))
            legalmoves.append((x + 1, y + 1))
            legalmoves.append((x - 1, y + 1))
        if self.color == "W":
            if self.movecount == 0 and (board.IsOccupied((x, y - 1)) == False):
                legalmoves.append((x, y - 2))
            legalmoves.append((x, y - 1))
            legalmoves.append((x + 1, y - 1))
            legalmoves.append((x - 1, y - 1))

        for mv in legalmoves:
            if mv != None:
                if mv[0] != self.position[0]:
                    if board.IsOccupied(mv) == False:
                        delmoves.append(mv)
                else:
                    if board.IsOccupied(mv) == True:
                        delmoves.append(mv)

        moves = (set(legalmoves) - set(delmoves))
        print(mv)
        self.movelist = moves
        return moves


def Initialize():
    global MainBoard
    MainBoard = Board()
    MoveCount = 0
    King((4, 7), "W", MainBoard)
    Queen((3, 7), "W", MainBoard)
    Bishop((2, 7), "W", MainBoard)
    Bishop((5, 7), "W", MainBoard)
    Bishop((2, 0), "B", MainBoard)
    Bishop((5, 0), "B", MainBoard)
    Knight((6, 0), "B", MainBoard)
    Knight((1, 0), "B", MainBoard)
    Knight((1, 7), "W", MainBoard)
    Knight((6, 7), "W", MainBoard)
    Queen((3, 0), "B", MainBoard)
    King((4, 0), "B", MainBoard)
    Rook((0, 7), "W", MainBoard)
    Rook((7, 7), "W", MainBoard)
    Rook((0, 0), "B", MainBoard)
    Rook((7, 0), "B", MainBoard)
    for a in range(8):
        Pawn((a, 1), "B", MainBoard)
        Pawn((a, 6), "W", MainBoard)
        Update()


Initialize()

while not done:

    global selected_pos, Piece
    takes = [0]
    taken = [0]
    ANYSELECTED = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            selected_pos = [int(math.floor((event.pos[0] * 8.0 / screensize[0]))),
                            int(math.floor(event.pos[1] * 8.0 / screensize[1]))]
            for p in MainBoard.GetAllPieces():
                if p.selected is True:
                    ANYSELECTED.append(True)
                else:
#
                    ANYSELECTED.append(False)

                if any(ANYSELECTED):
                    if p.selected is True:
                        if tuple(p.position) == tuple(selected_pos):
                            p.selected = False
                        elif p.position != selected_pos:
                            if MainBoard.IsOccupied(selected_pos) and p.CanTake(selected_pos):
                                taken[0] = tuple(selected_pos)
                                takes[0] = p
                                ANYSELECTED = []
                                p.selected = False
                            else:
                                p.MoveTo(MainBoard,selected_pos)
                                p.selected = False
                                ANYSELECTED = []
                else:
                    if tuple(p.position) == tuple(selected_pos):
                        if MoveCount % 2 == 1 and p.color == "B":
                            p.selected = True
                        if MoveCount % 2 == 0 and p.color == "W":
                            p.selected = True

            #try:
            if (takes[0] != 0) and (taken[0] != 0):
                print(taken)
                print(takes)
                takes[0].Take(taken[0])
                print("Hey")
                MoveCount += 1
            #except:
            #    pass
            #
            Update()
    pygame.display.flip()
