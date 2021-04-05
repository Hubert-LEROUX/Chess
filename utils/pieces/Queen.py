from utils.varglob import WHITE, BLACK, IMAGE_SIZE
from utils.board import Board
from utils.svgsurf import load_svg
from utils.settings import settings
import pygame
import os

from utils.pieces import Piece

class Queen(Piece):
    """
    Classe pour la reine
    TODO Legal moves
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "D"
        self.valeur = 9
        super().changeNotation()

        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}q.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}q.svg"))

        # Contient tous les décalages 
        for i in range(-7,8):
            self.decalages.append((0,i))
            self.decalages.append((i,0))
            self.decalages.append((i,i))
            self.decalages.append((i,-i))
    
    def getLegalMoves(self, board, opponent, nbCoups):
        """
        Retourne une liste de mouvements légaux
        """
        possibleMoves = []
        for dx in (-1, 0, 1) :
            for dy in (-1, 0, 1) :
                if dx != 0 or dy != 0 :
                    possibleMoves += self.moveLegal(board, dx, dy, opponent)
        return possibleMoves

    def getControls(self, board, opponent):
        """
        Retourne une liste de mouvements légaux
        """
        possibleMoves = []
        for dx in (-1, 0, 1) :
            for dy in (-1, 0, 1) :
                if dx != 0 or dy != 0 :
                    possibleMoves += self.moveTheoric(board, dx, dy, opponent)
        return possibleMoves