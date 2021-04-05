import pygame
from utils.varglob import WHITE, BLACK, IMAGE_SIZE, Color
import os
from math import ceil



class Board():
    
    def __init__(self):
        self.size = 8
        self.grid = [[None]*8 for _ in range (8)]
        # self.gridRepr = [[" "]*8 for _ in range (8)]

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
        # self.gridRepr[piece.y][piece.x] = piece.notation

    # def regenerateRepr(self):
        # self.gri

    def __repr__(self)->str:
        """
        Retourne une chaîne de caractères
        avec un espace si None
        Ou repr de la piece si != None
        """
        # self.regenerateRepr()
        return "\n".join(" ".join([i.notation if i is not None else " " for i in j]) for j in self.grid)

    def updateGraphicalInterface(self, window, players):
        """
        update la graphical interface
        status: finshed
        """
        # On affiche l'échiquier (le fond blanc)
        window.fill(self.BG_color)
        # on fait chaque case noire
        for i in range(100, 900, 100):
            if i%200: # On commence avec blanc
                for j in range(100,900, 200):
                    window.blit(self.WOOD[WHITE], (i,j)) # cases blanches en bois
                for j in range(200,900, 200):
                    window.blit(self.WOOD[BLACK], (i, j)) # cases noires en bois
            else: # On commence avec noir
                for j in range(100,900, 200):
                    window.blit(self.WOOD[BLACK], (i,j))
                for j in range(200,900, 200):
                    window.blit(self.WOOD[WHITE], (i,j))    

        # On met la case du roi en rouge s'il est en échec
        if players[0].isChecked(self, players[1]):
            pygame.draw.rect(window, Color.RED.value, (players[0].king.x*100+100, players[0].king.y*100+100, 100,100))
        if players[1].isChecked(self, players[0]):
            pygame.draw.rect(window, Color.RED.value, (players[1].king.x*100+100, players[1].king.y*100+100, 100,100))

        # Puis on affiche les pièces
        origin = (100,100)
        for i,line in enumerate(self.grid):
            for j,piece in enumerate(line):
                if piece is not None:
                    window.blit(piece.IMAGE, (origin[0]+j*100, origin[1]+i*100))
        pygame.display.update()

    def markCases(self, cases, window):
        """
        Marque certaines cases
        TODO - Marquage des cases
        """
        # On marque avec un disque les cases vides où la pièce peut aller
        # Avec un cercle les cases enemies qu'elle peut envahir
        for (x,y) in cases:
            if 0<=x<8 and 0<=y<8:
                center = (x*100+150, y*100+150)
                if self.grid[y][x] is None: # Case vide
                    pygame.draw.circle(window, Color.GRAY.value, center, 20, 0) # Un disque
                else: # Case ennemi
                    pygame.draw.circle(window, Color.GRAY.value, center, 50, 10) # Un cercle
        pygame.display.update()
    
    def convertMousePosition2boardPosition(self, mousePosition):
        boardX = (mousePosition[0] // 100)-1
        boardY = (mousePosition[1] // 100)-1
        boardPosition = (boardX, boardY)
        return boardPosition