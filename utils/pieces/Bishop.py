from utils.varglob import WHITE, BLACK, IMAGE_SIZE
from utils.board import Board
from utils.svgsurf import load_svg
from utils.settings import settings
import pygame
import os

from utils.pieces import Piece


class Bishop(Piece):
    """
    Classe fou
    TODO movements
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "F"
        self.valeur = 3
        super().changeNotation()
        
        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}b.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}b.svg"))
    
    def getLegalMoves(self, board, opponent, nbCoups) :
        return self.moveLegal(board, 1, 1, opponent) + self.moveLegal(board, -1, 1, opponent) + self.moveLegal(board, -1, -1, opponent) + self.moveLegal(board, 1, -1, opponent)
    
    def getControls(self, board, opponent) :
        """
        Renvoie les cases contrôlées
        """
        return self.moveTheoric(board, 1, 1, opponent) + self.moveTheoric(board, 1, -1, opponent) + self.moveTheoric(board, -1, 1, opponent) + self.moveTheoric(board, -1, -1, opponent)