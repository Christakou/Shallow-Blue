import pygame
import math
import copy
import numpy as np
import random
import threading
from pieces import King,Queen,Rook,Bishop,Knight,Pawn
from utils import KEYDICT, SCREENSIZE

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
done = False
boardimage = pygame.image.load("./assets/chessboard.png")
boardimage = pygame.transform.scale(boardimage, SCREENSIZE)
selected_image = pygame.image.load("./assets/Selected.png")
legalmove_image = pygame.image.load("./assets/LegalMove.png")


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
        self.move_count = 0

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

    def initialize(self):
        self.move_count = 0
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
        self.update()

    def update(self):
        screen.blit(boardimage, (0, 0))
        suggestedmvs = []
        for Piece in MainBoard.GetAllPieces():
            Piece.coord = (Piece.position[0] * (SCREENSIZE[0] / 8.0), Piece.position[1] * (SCREENSIZE[1] / 8.0))
            screen.blit(pygame.image.load('./assets/' + Piece.imagefile), Piece.coord)
            if Piece.selected:
                screen.blit(selected_image, Piece.coord)
                if Piece.moves(MainBoard)!= None:
                    for a in Piece.moves(MainBoard): suggestedmvs.append(a)
        for legalmove in suggestedmvs:
            screen.blit(legalmove_image, (legalmove[0] * (SCREENSIZE[0] / 8.0), legalmove[1] * (SCREENSIZE[1] / 8.0)))





MainBoard = Board()
MainBoard.initialize()
NodeList = []



def Update(Board):
    MainBoard = Board
    screen.blit(boardimage, (0, 0))
    suggestedmvs = []
    for Piece in MainBoard.GetAllPieces():
        Piece.coord = (Piece.position[0] * (SCREENSIZE[0] / 8.0), Piece.position[1] * (SCREENSIZE[1] / 8.0))
        screen.blit(pygame.image.load('./assets/' + Piece.imagefile), Piece.coord)
        if Piece.selected:
            screen.blit(selected_image, Piece.coord)
            if Piece.moves(MainBoard)!= None:
                for a in Piece.moves(MainBoard): suggestedmvs.append(a)
    for legalmove in suggestedmvs:
        screen.blit(legalmove_image, (legalmove[0] * (SCREENSIZE[0] / 8.0), legalmove[1] * (SCREENSIZE[1] / 8.0)))










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
        Update(MainBoard)


while not done:
    takes = [0]
    taken = [0]
    ANYSELECTED = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            selected_pos = [int(math.floor((event.pos[0] * 8.0 / SCREENSIZE[0]))),
                            int(math.floor(event.pos[1] * 8.0 / SCREENSIZE[1]))]
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
                        if MainBoard.move_count % 2 == 0 and p.color == "W":
                            p.selected = True

            try:

                takes[0].Take(taken[0])


            except:
                pass
            #
            Update(MainBoard)
    if MainBoard.move_count % 2 == 1:
        Calculate()

    pygame.display.flip()
