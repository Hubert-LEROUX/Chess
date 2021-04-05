import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.font.init()
# import time


from utils.pieces import Piece, King, Tower, Bishop, Knight, Queen
from utils.board import Board
from utils.players import Player
from utils.varglob import WHITE, BLACK, Color

def launchGame():
    pieceSize = 100 # taille de chaque pièce du jeu d'échecs
    pygame.init()
    #* ================== Window =====================
    WIDTH, HEIGHT = 1000, 1000 # Largeur et hauteur de la fenêtre
    WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Définir la fenêtre
    pygame.display.set_caption("Chess") # Titre de la fenêtre

   

    main_font = pygame.font.SysFont("comicsans", 50)
    end_game_font = pygame.font.SysFont("comicsans", 50)



    board = Board()
    playerWhite = Player(board, WHITE)
    playerBlack = Player(board, BLACK)

    while True:
        board.updateGraphicalInterface(WIN)
        print(board)

        # pygame.time.delay(100)

        if not playerWhite.turn(board, playerBlack, WIN): # Tour des blancs
            # Les blancs ont perdu
            textsurface = end_game_font.render('BLACKS WIN', False, Color.BLUE.value)
            WIN.blit(textsurface, (400,400))

        if not playerBlack.turn(board, playerWhite, WIN): # Tour des noirs
            # Les noirs ont perdu
            textsurface = end_game_font.render('WHITES WIN', False, Color.BLUE.value)
            WIN.blit(textsurface, (400,400))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    

if __name__ == '__main__':
    
    launchGame()