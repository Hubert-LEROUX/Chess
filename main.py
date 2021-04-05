import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.font.init()


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
    end_game_font = pygame.font.SysFont("comicsans", 75)

    board = Board()
    playerWhite = Player(board, WHITE)
    playerBlack = Player(board, BLACK)

    def endGame(whoWins):
        textsurface = end_game_font.render(f'{whoWins} WINS', True, Color.BLUE.value)
        WIN.blit(textsurface, (400,400))
        pygame.display.update()
        duration = 0
        while duration < 10000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.time.delay(50)
            duration += 50
        exit()

    nbCoups = 0
    while True:
        board.updateGraphicalInterface(WIN, [playerBlack, playerWhite])
        # print(board)
        nbCoups+=1


        if not playerWhite.turn(board, playerBlack, WIN, nbCoups): # Tour des blancs
            # Les blancs ont perdu
            endGame('BLACK')

        # print()
        # print("\n".join([str(x) for x in playerBlack.king.casesInaccessiblesPourLeRoi(board, playerWhite)]))
        # print()

        if not playerBlack.turn(board, playerWhite, WIN, nbCoups): # Tour des noirs
            # Les noirs ont perdu
            endGame('WHITE')
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    

if __name__ == '__main__':
    launchGame()