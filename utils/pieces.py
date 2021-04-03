from utils.varglob import WHITE, BLACK, IMAGE_SIZE
from utils.board import Board
from utils.svgsurf import load_svg
from utils.settings import settings
import pygame
import os


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
        self.assets_folder = os.path.join("res", settings["piecesFolder"])
        self.x = x
        self.y = y

    def changeNotation(self):
        self.notation= self.notation.lower() if self.color == WHITE else self.notation.upper()

    def move (self, board, dx, dy) :
        r = []
        nx, ny = self.x+dx, self.y+dy # on fait directement le premier mouvement
        while self.isEmpty(nx, ny, board) :
            r.append((nx, ny))
            nx += dx
            ny += dy
        if self.isOpponentPiece(nx, ny, board) :
            r.append((nx, ny))
        return r

    def isEmpty(self, x, y, board):
        return 0<=x<8 and 0<=y<8 and (board.grid[y][x] is None)

    def isOpponentPiece(self, x, y, board):
        return 0<=x<8 and 0<=y<8 and (board.grid[y][x] is not None) and board.grid[y][x].player != self.player
    
    def isEmptyOrOpponentPiece(self, x,y, board):
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
        
        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}k.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}k.svg"))

        # Contient tous les décalages possibles (ex : (-1, 1), (0, 1),...)
        for dx in [0, -1, 1]:
            for dy in [0, -1, 1] :
                if dx or dy : # si on ne reste pas sur place
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

        for p in opponent.pieces:
            # On récup les pièces à vérifier
            if isinstance(p, King):
                cases = [(p.x+dec_x, p.y+dec_y) for (dec_x, dec_y) in self.decalages]
            else:
                cases = p.getLegalMoves(board, opponent)
            
            # Pour chaque case accessible par ladite pièce adverse
            for (x,y) in cases:
                if 0<=x<8 and 0<=y<8 and self.isAccessible[y][x] == True:
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
        # for line in self.isAccessible:
        #     print(line)
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

        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}q.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}q.svg"))

        # Contient tous les décalages 
        for i in range(-7,8):
            self.decalages.append((0,i))
            self.decalages.append((i,0))
            self.decalages.append((i,i))
            self.decalages.append((i,-i))
    
    def getLegalMoves(self, board, opponent=None):
        """
        Retourne une liste de mouvements légaux
        """
        possibleMoves = []
        for dx in (-1, 0, 1) :
            for dy in (-1, 0, 1) :
                if dx != 0 or dy != 0 :
                    possibleMoves += self.move(board, dx, dy)
        return possibleMoves

        
class Pawn(Piece):
    """
    TODO - En passant move
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "P"
        super().changeNotation()

        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}p.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}p.svg"))


        self.tourAuMomentOuElleAvanceDeDeuxCases = None # Pour gérer en Passant

        if self.color == WHITE:
            self.direction = -1
        else: 
            self.direction = +1

    def getLegalMoves(self, board, opponent=None):
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

        return legalMoves
   
        
        
class Tower(Piece):
    """
    Classe tower
    TODO movements
    """
    def __init__ (self, color, x, y, player) :
        super().__init__(color, x, y, player)
        self.notation = "T"
        super().changeNotation()
        # self.IMAGE = load_svg(pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}r.svg")))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}r.svg"))

    
    def getLegalMoves(self, board, opponent=None) :
        return self.move(board, 1, 0) + self.move(board, -1, 0) + self.move(board, 0, 1) + self.move(board, 0, -1)
        
        
class Bishop(Piece):
    """
    Classe fou
    TODO movements
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "F"
        super().changeNotation()
        
        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}b.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}b.svg"))


        # Mouvements 
        for i in range(-7,8):
            if i!=0:
                self.decalages.append((i,i))
                self.decalages.append((i,-i))

    def getLegalMoves(self, board, opponent=None):
        return self.move(board, 1, 1) + self.move(board, 1, -1) + self.move(board,-1, 1) + self.move(board, -1, -1)
        
class Knight(Piece):
    """
    Classe cavalier
    TODO -
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "C"
        super().changeNotation()
        # self.IMAGE = load_svg(pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}n.svg")))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}n.svg"))


        # Mouvements 
        for i in [-2,-1,1,2]:
            for j in [-2,-1,1,2]:
                if abs(i)!=abs(j):
                    self.decalages.append((i,j))

    def getLegalMoves(self, board, opponent=None):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0 <= new_x < 8 and 0<= new_y < 8:
                if self.isEmpty(new_x, new_y, board): # Case vide
                    legalMoves.append((new_x, new_y))
                elif self.isOpponentPiece(new_x, new_y, board): # Case appartenant à l'adversaire
                    legalMoves.append((new_x, new_y))
        return legalMoves
                