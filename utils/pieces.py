from utils.varglob import WHITE, BLACK
from utils.board import Board

class Piece():
    """
    Classe contenant les pièces
    """
    def __init__(self, color, x, y, player):
        self.color = color # Conserve la couleur de la pièce
        self.decalages = [] # Conserve les décalages _théoriques_ que peut faire la pièce
        self.player = player # Conserve le joueur qui détient la pièce
        self.alreadyMoved = False # Indique si la pièce a déjà bougé
        self.notation = "" # Conserve la notation de la pièce
        self.x = x 
        self.y = y

    def changeNotation(self):
        self.notation= self.notation.lower() if self.color == WHITE else self.notation.upper()

    def leftUp (self, board) :
        r = []
        nx, ny = self.x, self.y
        ny -= 1
        nx -= 1
        while self.isEmpty(nx, ny) :
            r.append((nx, ny))
            ny -= 1
            nx -= 1
        if self.isOpponentPiece(nx, ny):
            r.append((nx, ny))
        return r

    def leftDown (self, board) :
        r = []
        nx, ny = self.x, self.y
        ny += 1
        nx -= 1
        while self.isEmpty(nx, ny) :
            r.append((nx, ny))
            ny += 1
            nx -= 1
        if self.isOpponentPiece(nx, ny):
            r.append((nx, ny))
        return r

    def rightUp (self, board) :
        r = []
        nx, ny = self.x, self.y
        ny -= 1
        nx += 1
        while self.isEmpty(nx, ny) :
            r.append((nx, ny))
            ny -= 1
            nx += 1
        if self.isOpponentPiece(nx, ny):
            r.append((nx, ny))
        return r
    
    def rightDown (self, board) :
        r = []
        nx, ny = self.x, self.y
        ny += 1
        nx += 1
        while self.isEmpty(nx, ny) :
            r.append((nx, ny))
            ny += 1
            nx += 1
        if self.isOpponentPiece(nx, ny):
            r.append((nx, ny))
        return r
        
    def down (self, board) :
        r = []
        nx, ny = self.x, self.y
        ny += 1 # pas ajouter la position initiale
        while self.isEmpty(nx, ny) :
            r.append((nx, ny))
            ny += 1
        if self.isOpponentPiece(nx, ny):
            r.append((nx, ny))
        return r

    def up (self, board) :
        r = []
        nx, ny = self.x, self.y
        ny -= 1
        while self.isEmpty(nx, ny) :
            r.append((nx, ny))
            ny -= 1
        if self.isOpponentPiece(nx, ny):
            r.append((nx, ny))
        return r

    def right (self, board) :
        r = []
        nx, ny = self.x, self.y
        nx += 1
        while self.isEmpty(nx, ny) :
            r.append((nx, ny))
            nx += 1
        if self.isOpponentPiece(nx, ny):
            r.append((nx, ny))
        return r

    def left (self, board) :
        r = []
        nx, ny = self.x, self.y
        nx -= 1
        while self.isEmpty(nx, ny) :
            r.append((nx, ny))
            nx -= 1
        if self.isOpponentPiece(nx, ny):
            r.append((nx, ny))
        return r

    def isEmpty(self, board, x, y):
        return 0<=x<8 and 0<=y<8 and (board.grid[y][x] is None)

    def isOpponentPiece(self, board, x, y):
        return 0<=x<8 and 0<=y<8 and (board.grid[y][x] is not None) and  board.grid[y][x].player != self.player
    
    def isEmptyOrOpponentPiece(self, board, x,y):
        return self.isEmpty(board, x, y) or self.isOpponentPiece(self, board, x, y)

    def __repr__(self) -> str:
        return self.notation

    
class King(Piece):
    """
    Classe pour le roi
    TODO Great Rock
    TODO Little Rock
    """
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

    def isChecked(self, board, opponent):
        self.casesInaccessiblesPourLeRoi(board, opponent)
        if self.isAccessible[self.y][self.x] == False:
            return True # On est en échec
        return False # On est pas en échec

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

    def getLegalMoves(self, board, opponent):
        """
        Retourne une liste de mouvements légaux
        """
        self.casesInaccessiblesPourLeRoi(board, opponent)
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0<=new_x<8 and 0<=new_y<8 and self.isAccessible[new_y][new_x]:
                legalMoves.append((new_x, new_y))
        return legalMoves

    

class Queen(Piece):
    """
    Classe pour la reine
    TODO Legal moves
    """
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
        diagonals = self.leftDown(board) + self.leftUp(board) + self.rightDown(board) + self.rightUp(board)
        lines = self.down(board) + self.right(board) + self.up(board) + self.left(board)
        return diagonals + lines

        
class Pawn(Piece):
    """
    TODO - En passant move
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "P"
        super().changeNotation()

        self.tourAuMomentOuElleAvanceDeDeuxCases = None # Pour gérer en Passant

        if self.color == WHITE:
            self.direction = 1
        else: 
            direction = -1

    def getLegalMoves(self, board):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] 

        # On teste si on peut avancer de 1
        new_y = self.y + self.direction
        #i.e. que la case suivante est vide
        if self.isEmpty(self.x, new_y, board): 
            legalMoves.append((self.x, new_y))
        # On teste à gauche et à droite

        new_x = self.x-1
        # On regarde à gauche
        if self.isOpponentPiece(new_x, new_y, board): 
            legalMoves.append((new_x, new_y))
        # On regarde à droite
        new_x = self.x+1
        if self.isOpponentPiece(new_x, new_y, board): 
            legalMoves.append((new_x, new_y))

        # On peut avencer de deux cases
        new_y = self.y + 2*self.direction
        if not self.alreadyMoved and self.isEmpty(self.x, new_y, board): 
            legalMoves.append((self.x, new_y))
   
        
        
class Tower(Piece):
    """
    Classe tower
    TODO movements
    """
    def __init__ (self, color, x, y, player) :
        super().__init__(color, x, y, player)
        self.notation = "T"
        super().changeNotation()
    
    def getLegalMoves(self, board) :
        return self.left(board) + self.right(board) + self.down(board) + self.up(board)
        
        
class Bishop(Piece):
    """
    Classe fou
    TODO movements
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "F"
        super().changeNotation()

        # Mouvements 
        for i in range(-7,8):
            if i!=0:
                self.decalages.append((i,i))
                self.decalages.append((i,-i))

    def getLegalMoves(self, board, opponent):
        return self.leftDown(board) + self.leftUp(board) + self.rightDown(board) + self.rightUp(board)
        
class Knight(Piece):
    """
    Classe cavalier
    TODO -
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "C"
        super().changeNotation()

        # Mouvements 
        for i in [-2,-1,1,2]:
            for j in [-2,-1,1,2]:
                if abs(i)!=abs(j):
                    self.decalages.append((i,j))

    def getLegalMoves(self, board, opponent):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0 <= new_x < 8 and 0<= new_y < 8:
                if board.grid[new_y][new_x] == None: # Case vide
                    legalMoves.append((new_x, new_y))
                elif board.grid[new_y][new_x].player == opponent: # Case appartenant à l'adversaire
                    legalMoves.append((new_x, new_y))
        return legalMoves
        

if __name__ == "__main__":
    k = King(BLACK, 4,0,None)
    print(k)
        