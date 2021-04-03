import pygame
from utils.pieces import Piece, King, Tower, Bishop, Knight, Queen
from utils.board import Board
from utils.players import Player
from utils.varglob import WHITE, BLACK

def launchGame():
    board = Board()
    playerWhite = Player(board, WHITE)
    playerBlack = Player(board, BLACK)

    print(board)
    

if __name__ == '__main__':
    launchGame()