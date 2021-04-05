from utils.varglob import WHITE, BLACK, IMAGE_SIZE
from utils.board import Board
from utils.svgsurf import load_svg
from utils.settings import settings
from utils.pieces.Piece import Piece
import pygame
import os

class Pawn(Piece):
    """
    TODO - En passant move
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "P"
        self.valeur = 1
        super().changeNotation()
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}p.svg"))

        if self.color == WHITE:
            self.promotionLine = 0
            self.direction = -1
            self.enPassantLine = 3
        else: 
            self.promotionLine = 7
            self.direction = +1
            self.enPassantLine = 4

    def getLegalMoves(self, board, opponent, nbCoups):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = []

        # On teste si on peut avancer de 1
        new_y = self.y + self.direction
        #i.e. que la case suivante est vide
        if self.isEmpty(self.x, new_y, board): 
            if self.moveAvoidCheck((self.x, new_y),board, opponent):
                legalMoves.append((self.x, new_y))
        # On teste à gauche et à droite

        #* Diagonales gauche puis droite
        new_x = self.x-1
        # On regarde à gauche
        if self.isOpponentPiece(new_x, new_y, board) or (self.isPawnVulnerableForEnPassant(new_x, self.y, board,opponent, nbCoups)): 
            if self.moveAvoidCheck((new_x, new_y),board, opponent):
                legalMoves.append((new_x, new_y))
        # On regarde à droite
        new_x = self.x+1
        if self.isOpponentPiece(new_x, new_y, board) or (self.isPawnVulnerableForEnPassant(new_x, self.y, board,opponent, nbCoups)): 
            if self.moveAvoidCheck((new_x, new_y),board, opponent):
                legalMoves.append((new_x, new_y))

        #* Mouvement de deux cases
        # On peut avencer de deux cases
        new_y = self.y + 2*self.direction
        if not self.alreadyMoved and self.isEmpty(self.x, new_y, board): 
            if self.moveAvoidCheck((self.x, new_y),board, opponent):
                legalMoves.append((self.x, new_y))

        return legalMoves

    def isPawnVulnerableForEnPassant(self, x, y, board, opponent, nbCoups) :
        """
        Renvoie True si le pion sur la case en question est possiblement pris en "en passant"
        Le pion est vulnérable s'il vient de bouger au coup juste avant
        x, y : positions de la pièce où il devrait y avoir un en passant (donc là ou la pièce adverse est prise)
        """
        if self.isOpponentPiece(x,y,board):
            piece = board.grid[y][x]
            # print(f"diff coups == 1 : {abs(nbCoups-piece.lastMove)==1}")
            # print(f"nombre de mouvements vaut 1 : {piece.nbFoisMoved==1}")
            # print(f"bonne ligne pour en passant : {y == self.enPassantLine}")
            if isinstance(piece, Pawn) and abs(nbCoups-piece.lastMove)==1 and piece.nbFoisMoved==1 and y == self.enPassantLine:
                return True
        return False


    def getControls(self, board, opponent):
        """
        Retourne une liste des cases controlées
        """
        controls = [] 
        new_y = self.y + self.direction
        new_x = self.x-1
        # On regarde à gauche
        controls.append((new_x, new_y))
        # On regarde à droite
        new_x = self.x+1
        controls.append((new_x, new_y))
        return controls