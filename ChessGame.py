import pygame
import math
import copy
import numpy as np
from Board import *
import random
import threading

screensize = (600, 600)
filelocation = "C:\Users\Chris\Documents\Shallow Blue"
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
Turn = 0



class Board():
    def __init__(self, a=None, b=None):
        self.whitePieces = []
        self.blackPieces = []
        self.score = 0
        self.a = a
        self.b = b
        self.MoveCount = 0

    def GetAllPieces(self):
        return self.whitePieces + self.blackPieces

    def Length(self):
        return len(self.GetAllPieces())

    def Represent(self):
        rep = np.zeros((8,8))
        pieces = self.GetAllPieces()
        for p in pieces:
            if p.color == "W":
                rep[p.position[1]][p.position[0]] = p.value
            else:
                rep[p.position[1]][p.position[0]] = -p.value
        print (rep)
        print("-----")

    def Clear(self):
        self.whitePieces = []
        self.blackPieces = []
        self.allPieces = []
        self.score = 0

    def GetScore(self):
        rep = np.zeros((8, 8))
        pieces = self.GetAllPieces()
        for p in pieces:
            if p.color == "W":
                rep[p.position[1]][p.position[0]] = p.value
            else:
                rep[p.position[1]][p.position[0]] = -p.value
        self.score = rep.sum()
        return rep.sum()

    def CopyState(self,board):
        self.Clear()
        for p in board.whitePieces:
            self.whitePieces.append(copy.deepcopy(p))
        for p in board.blackPieces:
            self.blackPieces.append(copy.deepcopy(p))

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
    def CanTake(self, pos):
        for p in self.board.GetAllPieces():
            if tuple(p.position) == tuple(pos) and p.color != self.color:
                if self.moves(self.board) != None:
                    if tuple(pos) in self.moves(self.board):
                        return True

    def MoveTo(self,board, (x, y)):
        global MoveCount
        if self.moves(self.board) != None:
            if (x, y) in self.moves(board):
                if not self.board.IsOccupied((x, y)):
                    self.position = (x, y)
                    board.MoveCount += 1
                    self.movecount += 1
                else:
                    self.Take((x,y))
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

    def Take(self, (x, y)):
        global MoveCount
        if self.board.IsOccupied((x, y)):
            if self.type == "p":
                if self.CanTake((x, y)):
                    self.board.Occupier((x, y)).Delete()
                    self.position = ((x, y))
                    self.board.MoveCount += 1
                    self.movecount += 1

            else:
                if self.CanTake((x, y)):
                    self.board.Occupier((x, y)).Delete()
                    self.position = ((x, y))
                    self.board.MoveCount += 1
                    self.movecount += 1



class King(Piece):

    def __init__(self, pos, color, board):
        Piece.__init__(self, pos, color, board)
        self.type = "ki"
        self.imagefile = "/" + str((self.color) + keydict[self.type] + ".png")
        self.value = 1000
        self.coord = [self.position[0] * (screensize[0] / 8.0), self.position[1] * (screensize[1] / 8.0)]
        self.board = board
        if self.color == "B" :
            self.board.blackPieces.append(self)
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
        for mv in legalmoves:
            if not InBoard(mv):
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
        self.board = board
        if self.color == "B":
            self.board.blackPieces.append(self)
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
        for mv in legalmoves:
            if not InBoard(mv):
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
        self.board = board
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
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
        for mv in legalmoves:
            if not InBoard(mv):
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
        self.board = board
        if self.color == "B":
            self.board.blackPieces.append(self)
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

        for mv in legalmoves:
            if board.IsOccupied((mv)):
                if board.Occupier(mv).color == self.color:
                    delmoves.append(mv)
        for mv in legalmoves:
            if not InBoard(mv):
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
        self.board = board
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
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
        for mv in legalmoves:
            if not InBoard(mv):
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
        self.board = board
        if self.color == "B":
            self.board.blackPieces.append(self)
        if self.color == "W":
            self.board.whitePieces.append(self)
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
                    if self.board.IsOccupied(mv) == False:
                        delmoves.append(mv)
                    elif self.board.Occupier(mv).color == self.color:
                        delmoves.append(mv)
                else:
                    if self.board.IsOccupied(mv) == True:
                        delmoves.append(mv)
        for mv in legalmoves:
            if not InBoard(mv):
                delmoves.append(mv)

        moves = (set(legalmoves) - set(delmoves))
        self.movelist = moves
        return moves
def InBoard(t1):
    if t1[0] >= 0 and t1[0] <8:
        if t1[1] >= 0 and t1[1] < 8:
            return True
    else:
        return False

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

NodeList = []


#class MiniMaxNode():
    #    def __init__(self, maxdepth, state, root= None, currentdepth = 1):
#        global NodeList
#        NodeList.append(self)
#        self.state = state
#        self.depth = currentdepth
#        self.value = 0
#        self.root = root
#        self.maxdepth = maxdepth
#        self.currentdepth = currentdepth
#
#        if (self.depth <= self.maxdepth):
    #            if self.root != None:
    #                if self.depth % 2 == 1:
    #                    for p in root.state.whitePieces:
    #
#                        def GenerateNodes():
    #                            if p.moves(root.state) != set([]):
        #                                try:
#                                    for mv in p.moves(root.state):
    #                                        nextboard = Board(p.position, mv)
#                                        nextboard.CopyState(root.state)
#                                        nextboard.Occupier(p.position).MoveTo(nextboard, mv)
#                                        k = self.depth + 1
#                                        newnode = MiniMaxNode(self.maxdepth,nextboard,self, k)
#                                except:
#                                    pass
#
#                        t = threading.Thread(target=GenerateNodes())
#                        t.start()
#                if self.depth % 2 == 0:
    #                    for p in root.state.blackPieces:
    #
#                        def GenerateNodes():
    #                            if p.moves(root.state) != set([]):
        #                                try:
#                                    for mv in np.nditer(np.asanyarray(list(p.moves(root.state))),["refs_ok","zerosize_ok","common_dtype"]):
    #                                        nextboard = Board(p.position, mv)
#                                        nextboard.CopyState(root.state)
#                                        nextboard.Occupier(p.position).MoveTo(nextboard, mv)
#                                        k = self.depth + 1
#                                        newnode = MiniMaxNode(self.maxdepth,nextboard, self, k)
#                                except:
#                                    pass
#                            else:
#                                pass
#
#                        t = threading.Thread(target=GenerateNodes())
#                        t.start()
#            else:
#                if self.depth % 2 == 1:
    #                    for p in MainBoard.blackPieces:
    #
#                        def GenerateNodes():
    #                            if len(p.moves(MainBoard))!= 0:
        #                                for mv in p.moves(MainBoard):
        #                                    nextboard = Board(p.position, mv)
    #                                    nextboard.CopyState(MainBoard)
    #                                    nextboard.Occupier(p.position).MoveTo(nextboard, mv)
    #                                    newnode = MiniMaxNode(self.maxdepth, nextboard, self, (self.depth + 1))
    #
    #                        t = threading.Thread(target=GenerateNodes())
    #                        t.start()
    #    def __str__(self):
#        return(self.state.Represent())

#def Calculate(depth = 1):
#    global NodeList
#    NodeList = []
#    Node = MiniMaxNode(3, MainBoard)
#
#    #print(len(NodeList))
#
#    for a in range(10):
#           NodeList[-a].state.Represent()
#
#'#        #print(NodeList[a].depth)
#'#        #print("---------")
#'#
def Calculate(depth=1):

    for i in range(depth):
        nextBoards = []
        for p in MainBoard.blackPieces:
            for mv in p.moves(MainBoard):
                fakeboard = Board(p.position, mv)
                fakeboard.CopyState(MainBoard)
                fakeboard.Occupier(p.position).MoveTo(fakeboard,mv)
                nextBoards.append([fakeboard,p.position,mv])
        for k in nextBoards:#
            k[0].GetScore()

        tmp = random.shuffle(nextBoards)
        sortedBoards = sorted(nextBoards, key=lambda x: x[0].score, reverse=False)
        MainBoard.Occupier(sortedBoards[0][1]).MoveTo(MainBoard,sortedBoards[0][2])
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
                    for mv in p.moves(MainBoard):
                        print(mv)
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
                                print("Score is " + str(MainBoard.GetScore()))
                                p.MoveTo(MainBoard,selected_pos)
                                p.selected = False
                                ANYSELECTED = []
                else:
                    if tuple(p.position) == tuple(selected_pos):
                        if MainBoard.MoveCount % 2 == 0 and p.color == "W":
                            p.selected = True

            try:

                takes[0].Take(taken[0])


            except:
                pass
            #
            Update()
    if MainBoard.MoveCount % 2 == 1:
        Calculate()

    pygame.display.flip()
