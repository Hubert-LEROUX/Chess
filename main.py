import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.font.init()


from utils.pieces import Piece, King, Tower, Bishop, Knight, Queen
from utils.board import Board
from utils.players import Player
from utils.register import Register
from utils.varglob import WHITE, BLACK, Color
from utils.settings import settings

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

    #* Register
    register = Register(settings["whereToSave"], settings["whoPlaysWhite"], settings["whoPlaysBlack"])

    def endGame(whoWins):
        """
        Affiche la fin de la game si victoire de l'un
        """
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

    def endGameNulle() :
        """
        Affiche la fin d'une partie en cas de pat (match nul)
        """
        textsurface = end_game_font.render(f'NULLE', True, Color.BLUE.value)
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
        nbCoups+=1 # On incrémente le nombre de coups


        etat = playerWhite.turn(board, playerBlack, WIN, nbCoups, register) # Tour des blancs
        if etat == 0:
            # Les blancs ont perdu
            endGame('BLACK')
        elif etat == 1:
            endGameNulle()

        # print()
        # print("\n".join([str(x) for x in playerBlack.king.casesInaccessiblesPourLeRoi(board, playerWhite)]))
        # print()

        nbCoups+=1 #  on incrémente de coups
        etat = playerBlack.turn(board, playerWhite, WIN, nbCoups, register) # Tour des noirs
        if etat == 0:
            # Les noirs ont perdu
            endGame('WHITE')

        elif etat == 1:
            endGameNulle()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    

if __name__ == '__main__':
    launchGame()