import numpy as np
import copy
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
