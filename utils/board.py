import pygame
from utils.varglob import WHITE, BLACK, IMAGE_SIZE, Color
import os




class Board():
    
    def __init__(self):
        self.size = 8
        self.grid = [[None]*8 for _ in range (8)]
        self.gridRepr = [[" "]*8 for _ in range (8)]

        # =================== Load images ==================
        assets_folder = "res/wood"
        self.WOOD = dict()

        # print(os.getcwd())
        self.BG_color = Color.WHITE.value
        # print(self.BG_color)
        self.BLACK_COLOR = Color.BLACK.value

        self.WOOD[WHITE] = pygame.transform.scale(pygame.image.load(os.path.join(assets_folder, "square_light.jpg")),(IMAGE_SIZE, IMAGE_SIZE))
        self.WOOD[BLACK] = pygame.transform.scale(pygame.image.load(os.path.join(assets_folder, "square_dark.jpg")),(IMAGE_SIZE, IMAGE_SIZE))

    def addPiece(self, piece):
        self.grid[piece.y][piece.x] = piece
        self.gridRepr[piece.y][piece.x] = piece.notation

    def __repr__(self)->str:
        """
        Retourne une chaîne de caractères
        avec un espace si None
        Ou repr de la piece si != None
        """
        return "\n".join(" ".join(i) for i in self.gridRepr)

    def updateGraphicalInterface(self, WIN):
        """
        update la graphical interface
        """
        # On affiche l'échiquier (le fond blanc)
        WIN.fill(self.BG_color)
        # on fait chaque case noire
        for i in range(100, 900, 100):
            if i%200: # On commence avec blanc
                for j in range(100,900, 200):
                    WIN.blit(self.WOOD[WHITE], (i,j)) # cases blanches en bois
                for j in range(200,900, 200):
                    WIN.blit(self.WOOD[BLACK], (i, j)) # cases noires en bois
            else: # On commence avec noir
                for j in range(100,900, 200):
                    WIN.blit(self.WOOD[BLACK], (i,j))
                for j in range(200,900, 200):
                    WIN.blit(self.WOOD[WHITE], (i,j))
        # Puis on affiche les pièces
        origin = (100,100)
        for i,line in enumerate(self.grid):
            for j,piece in enumerate(line):
                if piece is not None:
                    WIN.blit(piece.IMAGE, (origin[0]+j*100, origin[1]+i*100))
        pygame.display.update()

    def markCases(self, cases):
        """
        Marque certaines cases
        """
        pass