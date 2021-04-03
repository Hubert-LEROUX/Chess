from utils.varglob import WHITE, BLACK
from utils.pieces import Pawn,King, Tower

class Player():
    def __init__(self, board, color) -> None:
        # Positionnement des pièces
        self.pieces = []

        if color == WHITE: # On place les pièces en bas
            yPawns = 1
            yGreatPieces = 0
        else:
            yPawns = 6
            yGreatPieces = 7

        for i in range(8): # on ajoute les pions
            pion = Pawn(color, i, yPawns, self)
            self.pieces.append(pion)
            board.addPiece(pion)

        for i in [0,7]: # on ajoute les tours
            tour = Tower(color, i, yGreatPieces, self)
            self.pieces.append(tour)
            board.addPiece(tour)


        for i in [1,6]: # on ajoute les tours
            cavalch = Knight(color, i, yGreatPieces, self)
            self.pieces.append(cavalch)
            board.addPiece(cavalch)

            
        for i in [2,5]: # on ajoute les fous
            bishop = Bishop(color, i, yGreatPieces, self)
            self.pieces.append(bishop)
            board.addPiece(bishop)


        # Roi
        k = King(color, 4, yGreatPieces, self)
        self.pieces.append(k)
        board.addPiece(k)

        self.king = k

        # Dame
        q = Queen(color, 3, yGreatPieces, self)
        self.pieces.append(q)
        board.addPiece(q)





    