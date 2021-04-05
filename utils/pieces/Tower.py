from utils.varglob import WHITE, BLACK, IMAGE_SIZE
from utils.board import Board
from utils.svgsurf import load_svg
from utils.settings import settings
import pygame
import os

from utils.pieces import Piece

class Tower(Piece):
    """
    Classe tower
    TODO movements
    """
    def __init__ (self, color, x, y, player) :
        super().__init__(color, x, y, player)
        self.notation = "T"
        self.valeur = 5
        super().changeNotation()
        # self.IMAGE = load_svg(pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}r.svg")))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}r.svg"))

    
    def getLegalMoves(self, board, opponent, nbCoups) :
        return self.moveLegal(board, 1, 0, opponent) + self.moveLegal(board, -1, 0, opponent) + self.moveLegal(board, 0, 1, opponent) + self.moveLegal(board, 0, -1, opponent)
    
    def getControls(self, board, opponent):
        """
        Renvoie les cases controlées
        """
        return self.moveTheoric(board, 1, 0, opponent) + self.moveTheoric(board, -1, 0, opponent) + self.moveTheoric(board, 0, 1, opponent) + self.moveTheoric(board, 0, -1, opponent)

    def whereDoSheRockate(self):
        if self.x == 0: #*Great Rock
            return (3, self.y)
        #* Little Rock
        return (5, self.y)

