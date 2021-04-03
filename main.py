import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.font.init()


from utils.pieces import Piece, King, Tower, Bishop, Knight, Queen
from utils.board import Board
from utils.players import Player
from utils.varglob import WHITE, BLACK

def launchGame():
    pieceSize = 100 # taille de chaque pièce du jeu d'échecs
    pygame.init()
    #* ================== Window =====================
    WIDTH, HEIGHT = 1000, 1000 # Largeur et hauteur de la fenêtre
    WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Définir la fenêtre
    pygame.display.set_caption("Chess") # Titre de la fenêtre

   

    main_font = pygame.font.SysFont("comicsans", 50)
    #* BG = pygame.transform.scale(pygame.image.load(os.path.join(assets_folder, "background-black.png")), (WIDTH, HEIGHT))


    board = Board()
    playerWhite = Player(board, WHITE)
    playerBlack = Player(board, BLACK)

    while True:
        board.updateGraphicalInterface(WIN)

        playerWhite.turn()
        playerBlack.turn()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    

if __name__ == '__main__':
    
    launchGame()