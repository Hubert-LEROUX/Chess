from utils.varglob import WHITE, BLACK
# from utils.board import Board

class Piece():
    """
    Classe contenant les pièces
    """
    def __init__(self, color, x, y, player):
        self.color = color
        self.decalages = []
        self.player = player
        self.notation = ""
        self.x = x
        self.y = y

    def changeNotation(self):
        if self.color == WHITE:
            self.notation= self.notation.lower()
        else:
            self.notation = self.notation.upper()
    
    def isKingUncovered(self, board) :
        """
        Renvoie true si le roi est à découvert
        """
        pass
    
    def __repr__(self) -> str:
        return self.notation

    


class King(Piece):
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "R"
        self.isAccessible = [[True]*8 for _ in range(8)]
        super().changeNotation()
        # Contient tous les décalages possibles (ex : (-1, 1), (0, 1),...)
        for dx in (0, -1, 1) :
            for dy in (0, -1, 1) :
                if dx or dy :
                    self.decalages.append((dx, dy))

    def canGreatRock(self, board):
        pass

    def canLittleRock(self, board):
        pass

    def casesInaccessiblesPourLeRoi(self, board, opponent):
        self.isAccessible = [[True]*8 for _ in range(8)] #On part du principe que tout est accessible
        for x in range(8):
            for y in range(8):
                if board.grid[y][x] != None and board.grid[y][x].player == self.player: # Si c notre propre pièce, on ne  peut pas y aller
                    self.isAccessible[y][x] = False
        for pieces in opponent.liste:
            for (x,y) in pieces.getLegalMoves(board):
                if self.isAccessible[y][x] == True:
                    self.isAccessible[y][x] = False

    def getLegalMoves(self, board):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y

        return legalMoves

    

class Queen(Piece):
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "D"
        super().changeNotation()

        # Contient tous les décalages 
        for i in range(-7,8):
            self.decalages.append((0,i))
            self.decalages.append((i,0))
            self.decalages.append((i,i))
            self.decalages.append((i,-i))
    
    def getLegalMoves(self, board):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        new_x, new_y = self.x, self.y 
        while (0 <= new_x < 8 and 0 <= new_y < 8 and board.gridRepr is None) :
            new_x += 1
            new_y += 1
            legalMoves.append((new_x, new_y))

        
class Pawn(Piece):
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "P"
        super().changeNotation()

        # self.firstMove = True # Si True, alors il peut avancer de deux

        # Contient tous les décalages 
        self.decalages = [(0, 1), (0, 2)] # pour l'instant on n'implémente pas le mécanisme de pion qui prend
        # une autre pièce

    def canEnPassant(self, board):
        pass

    def canEat(self, board):
        pass

    def getLegalMoves(self, board):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
        return legalMoves
        
class Tower(Piece):
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "T"
        
        
class Bishop(Piece):
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "F"
        super().changeNotation()
        for i in range(-7, 8):
            self.decalages.append((i, i))
            self.decalages.append((i, -i))

    def getLegalMoves(self, board):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
        return legalMoves
        
class Knight(Piece):
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "C"
        super().changeNotation()

        # Mouvements 
        for i in [-2,-1,1,2]:

            if abs(new_x) < 8:
                            for j in [-2,-1,1,2]:
                if abs(i)!=abs(j):
                    self.decalages.append((i,j))

    def getLegalMoves(self, board):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
        return legalMoves
        

if __name__ == "__main__":
    k = King(BLACK, 4,0,None)
    print(k)
        