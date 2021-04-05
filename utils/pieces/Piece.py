from utils.varglob import WHITE, BLACK, IMAGE_SIZE
from utils.board import Board
from utils.svgsurf import load_svg
from utils.settings import settings
import pygame
import os


class Piece():
    """
    Classe contenant les pièces
    """
    def __init__(self, color, x, y, player):
        self.color = color # Conserve la couleur de la pièce
        self.decalages = [] # Conserve les décalages _théoriques_ que peut faire la pièce
        self.player = player # Conserve le joueur qui détient la pièce
        self.alreadyMoved = False # Indique si la pièce a déjà bougé
        self.nbFoisMoved = 0 
        self.lastMove = None # On retient le tour auquel la pièce a bougé la dernière fois
        self.notation = "" # Conserve la notation de la pièce
        self.assets_folder = os.path.join("res", settings["piecesFolder"])
        self.x = x
        self.y = y

    def changeNotation(self):
        self.notation= self.notation.lower() if self.color == WHITE else self.notation.upper()

    def moveLegal (self, board, dx, dy, opponent) :
        r = []
        nx, ny = self.x+dx, self.y+dy # on fait directement le premier mouvement
        while self.isEmpty(nx, ny, board) :
            if self.moveAvoidCheck((nx, ny),board, opponent):
                r.append((nx, ny))
            nx += dx
            ny += dy
        if self.isOpponentPiece(nx, ny, board) :
            if self.moveAvoidCheck((nx, ny),board, opponent):
                r.append((nx, ny))
        return r


    def moveTheoric (self, board, dx, dy, opponent) :
        r = []
        nx, ny = self.x+dx, self.y+dy # on fait directement le premier mouvement

        while self.isEmpty(nx, ny, board) :
            r.append((nx, ny))
            nx += dx
            ny += dy
        # Soit on est sorti, soit on est tombé sur une pièce
        if 0<=nx<8 and 0<=ny<8:
            r.append((nx, ny))
        return r



    def isEmpty(self, x, y, board):
        return 0<=x<8 and 0<=y<8 and (board.grid[y][x] is None)
    
    def isFriend(self, x, y, board):
        return not self.isEmptyOrOpponentPiece(x,y, board)

    def isOpponentPiece(self, x, y, board):
        return 0<=x<8 and 0<=y<8 and (board.grid[y][x] is not None) and board.grid[y][x].player != self.player
    
    def isEmptyOrOpponentPiece(self, x,y, board):
        return self.isEmpty(x,y,board) or self.isOpponentPiece(x,y, board)

    def __repr__(self) -> str:
        return self.notation

    def moveAvoidCheck(self, newPosition, board, opponent):
        """
        Retourne True si le mouvement empêche un échec
        """
        # On fait comme si le mouvement avait lieu et on regarde si le player est toujours en échec
        # print("1",board)
        newX, newY = newPosition # On récupère les coordonnées de la nouvelle position
        # Coordonnées de l'ancienne
        firstX = self.x
        firstY = self.y
        caseArrivee = board.grid[newY][newX] # On récupère ce qui est dans la case d'arrivée, pour pouvoir le remettre après


        # On fait le move (pour tester s'il permet d'éviter un échec)
        self.x = newX
        self.y = newY
        board.grid[firstY][firstX] = None # On efface la case de départ 
        board.grid[newY][newX] = self # On remplit la case d'arrivée
        # print("2",board)

        # On regarde si on est toujours en échec (si le mouvement empêche un échec)
        result = self.player.isChecked(board, opponent)

        # On remet tout à sa place 
        self.x = firstX
        self.y = firstY
        board.grid[firstY][firstX] = self # On fait revenir la case
        board.grid[newY][newX] = caseArrivee
        # print("3",board)
        return not result