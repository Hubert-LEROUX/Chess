from utils.varglob import WHITE, BLACK, IMAGE_SIZE
from utils.board import Board
from utils.svgsurf import load_svg
from utils.settings import settings
import pygame
import os

from utils.pieces import Piece

class Knight(Piece):
    """
    Classe cavalier
    TODO -
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "C"
        self.valeur = 3
        super().changeNotation()
        # self.IMAGE = load_svg(pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}n.svg")))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}n.svg"))


        # Mouvements 
        for i in [-2,-1,1,2]:
            for j in [-2,-1,1,2]:
                if abs(i)!=abs(j):
                    self.decalages.append((i,j))

    def getLegalMoves(self, board, opponent, nbCoups):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0 <= new_x < 8 and 0<= new_y < 8:
                if self.isEmpty(new_x, new_y, board): # Case vide
                    if self.moveAvoidCheck((new_x, new_y), board, opponent):
                        legalMoves.append((new_x, new_y))
                elif self.isOpponentPiece(new_x, new_y, board): # Case appartenant à l'adversaire
                    if self.moveAvoidCheck((new_x, new_y), board, opponent):
                        legalMoves.append((new_x, new_y))
        return legalMoves

    def getControls(self, board, opponent):
        """
        Retourne une liste des cases contrôlées
        """
        controls = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0 <= new_x < 8 and 0<= new_y < 8:
                if self.isEmptyOrOpponentPiece(new_x, new_y, board):
                    controls.append((new_x, new_y))
               
        return controls