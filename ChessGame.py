import pygame
import math
import numpy as np

screensize = (600, 600)
filelocation = "C:/Users/Username/Desktop/Shallow Blue" # Change to filelocation
pygame.init()
screen = pygame.display.set_mode(screensize)
done = False
boardimage = pygame.image.load(filelocation + "/chessboard.png")
boardimage = pygame.transform.scale(boardimage, screensize)
selected_image = pygame.image.load(filelocation + "/Selected.png")
legalmove_image = pygame.image.load(filelocation + "/LegalMove.png")
selected_pos = [8, 8]
activePieces = []

IsPieceSelected = False

SelectedPiece = []
MoveCount = 0


def Initialize():
    global MoveCount
    MoveCount = 0
    King((4, 7), "W")
    Queen((3, 7), "W")
    Bishop((2, 7), "W")
    Bishop((5, 7), "W")
    Bishop((2, 0), "B")
    Bishop((5, 0), "B")
    Knight((6, 0), "B")
    Knight((1, 0), "B")
    Knight((1, 7), "W")
    Knight((6, 7), "W")
    Queen((3, 0), "B")
    King((4, 0), "B")
    Rook((0, 7), "W")
    Rook((7, 7), "W")
    Rook((0, 0), "B")
    Rook((7, 0), "B")
    for a in range(8):
        Pawn((a, 1), "B")
        Pawn((a, 6), "W")
    Update()


def IsOccupied(pos):
    for p in activePieces:
        if tuple(p.position) == tuple(pos):
            return True
    else:
        return False


def Occupier(pos):
    for p in activePieces:
        if tuple(p.position) == tuple(pos):
            return p


def Update():
    screen.blit(boardimage, (0, 0))
    suggestedmvs = []
    for Piece in activePieces:
        Piece.coord = (Piece.position[0] * (screensize[0] / 8.0), Piece.position[1] * (screensize[1] / 8.0))
        screen.blit(pygame.image.load(filelocation + Piece.imagefile), Piece.coord)
        if Piece.selected:
            screen.blit(selected_image, Piece.coord)
            if Piece.moves() != None:
                for a in Piece.moves(): suggestedmvs.append(a)
    for legalmove in suggestedmvs:
        screen.blit(legalmove_image, (legalmove[0] * (screensize[0] / 8.0), legalmove[1] * (screensize[1] / 8.0)))


class Piece:
    global keydict, activePieces, MoveCount

    keydict = {"ki": "King", "kn": "Knight", "r": "Rook", "q": "Queen", "b": "Bishop", "p": "Pawn"}

    def __init__(self, pos, color):
        self.position = pos
        self.color = color
        self.selected = False
        self.movecount = 0
        self.movelist = []

    def CanTake(self, (x, y)):
        for p in activePieces:
            if tuple(p.position) == tuple((x, y)) and p.color != self.color:
                if self.moves != None:
                    if (tuple((x, y)) in self.moves()):
                        return True

    def MoveTo(self, (x, y)):
        global MoveCount
        if self.moves() != None:
            if (x, y) in self.moves():
                if not IsOccupied((x, y)):
                    self.position = (x, y)
                    MoveCount += 1
                    self.movecount += 1
                    print(MoveCount)
            else:
                pass

    def Delete(self):
        activePieces.remove(self)

    def Take(self, (x, y)):
        if IsOccupied((x, y)):
            if self.type == "p":
                if self.CanTake((x, y)):
                    Occupier((x, y)).Delete()
                    self.position = ((x, y))

            else:
                if self.CanTake((x, y)):
                    Occupier((x, y)).Delete()
                    self.MoveTo((x, y))



class King(Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        self.type = "ki"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 10000
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        activePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self):
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
            if IsOccupied(mv):
                if Occupier(mv).color == self.color:
                    delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        return legalmoves


class Queen(Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        self.type = "q"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 9
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        activePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y + i))
            if IsOccupied((x + i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y - i))
            if IsOccupied((x + i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y - i))
            if IsOccupied((x - i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y + i))
            if IsOccupied((x - i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y))
            if IsOccupied((x + i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y))
            if IsOccupied((x - i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y + i))
            if IsOccupied((x, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y - i))
            if IsOccupied((x, y - i)):
                break
            else:
                pass
        for mv in legalmoves:
            if IsOccupied(mv):
                if Occupier(mv).color == self.color:
                    delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Rook(Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        self.type = "r"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 5
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        activePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y))
            if IsOccupied((x + i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y))
            if IsOccupied((x - i, y)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y + i))
            if IsOccupied((x, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x, y - i))
            if IsOccupied((x, y - i)):
                break
            else:
                pass
        for mv in legalmoves:
            if IsOccupied(mv):
                if Occupier(mv).color == self.color:
                    delmoves.append(mv)
        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Bishop(Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        self.type = "b"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 3
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        activePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self):
        x, y = self.position[0], self.position[1]
        legalmoves = []
        delmoves = []
        for i in range(1, 8):
            legalmoves.append((x + i, y + i))
            if IsOccupied((x + i, y + i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x + i, y - i))
            if IsOccupied((x + i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y - i))
            if IsOccupied((x - i, y - i)):
                break
            else:
                pass
        for i in range(1, 8):
            legalmoves.append((x - i, y + i))
            if IsOccupied((x - i, y + i)):
                break
            else:
                pass

        for mv in legalmoves:
            if IsOccupied((mv)):
                if Occupier(mv).color == self.color:
                    delmoves.append(mv)

        legalmoves = set(legalmoves) - set(delmoves)
        self.movelist = legalmoves
        return legalmoves


class Knight(Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        self.type = "kn"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 3
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        activePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self):
        x, y = self.position[0], self.position[1]
        legalmoves = [(x + 2, y + 1), (x - 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x + 1, y - 2), (x - 1, y - 2),
                      (x - 2, y - 1), (x + 2, y - 1)]
        delmoves1 = []
        for mv in legalmoves:
            if (mv[0] > 7) or (mv[0] < 0) or (mv[1] > 7) or (mv[1] < 0):
                delmoves1.append(mv)
        for mv in legalmoves:
            if IsOccupied((mv)):
                if Occupier(mv).color == self.color:
                    delmoves1.append(mv)
        moves = (set(legalmoves) - set(delmoves1))
        self.movelist = moves
        return moves


class Pawn(Piece):

    def __init__(self, pos, color):
        Piece.__init__(self, pos, color)
        self.type = "p"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 1
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        activePieces.append(self)
        pygame.image.load(filelocation + self.imagefile)

    def moves(self):
        legalmoves = []
        delmoves = []
        x, y = self.position[0], self.position[1]
        if self.color == "B":
            if self.movecount == 0 and (IsOccupied((x, y + 1)) == False):
                legalmoves.append((x, y + 2))
            legalmoves.append((x, y + 1))
            legalmoves.append((x + 1, y + 1))
            legalmoves.append((x - 1, y + 1))
        if self.color == "W":
            if self.movecount == 0 and (IsOccupied((x, y - 1)) == False):
                legalmoves.append((x, y - 2))
            legalmoves.append((x, y - 1))
            legalmoves.append((x + 1, y - 1))
            legalmoves.append((x - 1, y - 1))

        for mv in legalmoves:
            if mv != None:
                if mv[0] != self.position[0]:
                    if IsOccupied(mv) == False:
                        delmoves.append(mv)
                else:
                    if IsOccupied(mv) == True:
                        delmoves.append(mv)

        moves = (set(legalmoves) - set(delmoves))
        print(mv)
        self.movelist = moves
        return moves


class Board():

    def __init__(self,a,b):
        self.whitePieces = []
        self.blackPieces = []
        self.GetCurrentState()
        self.score = 0
    def GetAllPieces(self):
        return self.whitePieces + self.blackPieces

    def Clear(self):
        self.whitePieces = []
        self.blackPieces = []
        self.allPieces = []
        self.score = 0

    def GetCurrentState(self):
        self.Clear()
        for p in activePieces:
            if p.color == "W":
                self.whitePieces.append(p)
            elif p.color == "B":
                self.blackPieces.append(p)
        if (a, b) != None:
            pass
    def BoardOccupied(self,pos):
        for p in GetAllPices(self):
            if p.position == pos:
                return True

    def GetScore(self):
        Score = 0
        for p in self.whitePieces:
            Score += p.value
        for p in self.blackPieces:
            Score -= p.value
        return Score

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
            for p in activePieces:
                if p.selected is True:
                    ANYSELECTED.append(True)
                else:

                    ANYSELECTED.append(False)

                if any(ANYSELECTED):
                    if p.selected is True:
                        if tuple(p.position) == tuple(selected_pos):
                            p.selected = False
                        elif p.position != selected_pos:
                            if IsOccupied(selected_pos) and p.CanTake(selected_pos):
                                taken[0] = tuple(selected_pos)
                                takes[0] = p
                                ANYSELECTED = []
                                p.selected = False
                            else:
                                p.MoveTo(selected_pos)
                                p.selected = False
                                ANYSELECTED = []
                else:
                    if tuple(p.position) == tuple(selected_pos):
                        if MoveCount % 2 == 1 and p.color == "B":
                            p.selected = True
                        if MoveCount % 2 == 0 and p.color == "W":
                            p.selected = True

            try:
                print(taken)
                print(takes)
                takes[0].Take(taken[0])
                print("Hey")
            except:
                pass
            #
            Update()
            board1 = Board()
            print(board1.GetScore())
    pygame.display.flip()
