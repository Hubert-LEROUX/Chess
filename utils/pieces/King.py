from utils.varglob import WHITE, BLACK, IMAGE_SIZE
from utils.board import Board
from utils.svgsurf import load_svg
from utils.settings import settings
import pygame
import os

from utils.pieces import Piece

class King(Piece):
    """
    Classe pour le roi
    TODO Great Rock
    TODO Little Rock
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "R"
        
        super().changeNotation()
        
        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}k.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}k.svg"))

        # Contient tous les décalages possibles (ex : (-1, 1), (0, 1),...)
        for dx in [0, -1, 1]:
            for dy in [0, -1, 1] :
                if dx or dy : # si on ne reste pas sur place
                    self.decalages.append((dx, dy))

    def canGreatRock(self, board):
        """
        Il faut reagarder si le roi et la tour n'ont jamais bougé et que les cases entre les deux soient libres
        """
        pass

    def canLittleRock(self, board):
        """
        Il faut reagarder si le roi et la tour n'ont jamais bougé et que les cases entre les deux soient libres
        """
        pass

    def isChecked(self, board, opponent):
        """
        Regarde si le roi est en échec ou non
        """
        isAccessible = self.casesInaccessiblesPourLeRoi(board, opponent)
        return not isAccessible[self.y][self.x] # retourne si la case du roi est accessible ou non

    def casesInaccessiblesPourLeRoi(self, board, opponent):
        """
        Met à jour un tableau avec True si la case est safe et False sinon
        """
        isAccessible = [[True]*8 for _ in range(8)] # On part du principe que tout est accessible

        # Pour toutes les cases
        for x in range(8):
            for y in range(8):
                
                if board.grid[y][x] is not None: # Si on tombe sur une pièce
                    piece = board.grid[y][x]

                    if piece.player == self.player and not isinstance(piece, King): # Si c une pièce alliée différente du roi
                        isAccessible[y][x] = False

                    elif piece.player != self.player: # Piece ennemie
                        cases = piece.getControls(board, self.player)
                        # Pour chaque case accessible par ladite pièce adverse
                        for (X,Y) in cases: # Pour chaque case sous contrôle de l'ennemi
                            if 0<=X<8 and 0<=Y<8 and isAccessible[Y][X] == True: #Si elle n'est pas envore marquée, on la marque
                                isAccessible[Y][X] = False

        return isAccessible

    def getLegalMoves(self, board, opponent, nbCoups):
        """
        Retourne une liste de mouvements légaux
        """
        isAccessible = self.casesInaccessiblesPourLeRoi(board, opponent)
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0<=new_x<8 and 0<=new_y<8 and isAccessible[new_y][new_x]:
                if self.moveAvoidCheck((new_x, new_y), board, opponent):
                    legalMoves.append((new_x, new_y))
        return legalMoves

    def getControls(self, board, opponent):
        return [(self.x+dec_x, self.y+dec_y) for (dec_x, dec_y) in self.decalages]