
class Board():
    def __init__(self):
        self.size = 8
        self.grid = [[None]*8 for _ in range (8)]

        self.gridRepr = [[" "]*8 for _ in range (8)]

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




