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
        self.lastMove = None # On retient le tour auquel la pièce a bougé la dernière fois
        self.notation = "" # Conserve la notation de la pièce
        self.assets_folder = os.path.join("res", settings["piecesFolder"])
        self.x = x
        self.y = y

    def changeNotation(self):
        self.notation= self.notation.lower() if self.color == WHITE else self.notation.upper()

    def moveLegal (self, board, dx, dy, opponent) :
        r = []
        nx, ny = self.x+dx, self.y+dy # on fait directement le premier mouvement
        while self.isEmpty(nx, ny, board) :
            if self.moveAvoidCheck((nx, ny),board, opponent):
                r.append((nx, ny))
            nx += dx
            ny += dy
        if self.isOpponentPiece(nx, ny, board) :
            if self.moveAvoidCheck((nx, ny),board, opponent):
                r.append((nx, ny))
        return r


    def moveTheoric (self, board, dx, dy, opponent) :
        r = []
        nx, ny = self.x+dx, self.y+dy # on fait directement le premier mouvement

        while self.isEmpty(nx, ny, board) :
            r.append((nx, ny))
            nx += dx
            ny += dy
        # Soit on est sorti, soit on est tombé sur une pièce
        if 0<=nx<8 and 0<=ny<8:
            r.append((nx, ny))
        return r



    def isEmpty(self, x, y, board):
        return 0<=x<8 and 0<=y<8 and (board.grid[y][x] is None)
    
    def isFriend(self, x, y, board):
        return not self.isEmptyOrOpponentPiece(x,y, board)

    def isOpponentPiece(self, x, y, board):
        return 0<=x<8 and 0<=y<8 and (board.grid[y][x] is not None) and board.grid[y][x].player != self.player
    
    def isEmptyOrOpponentPiece(self, x,y, board):
        return self.isEmpty(x,y,board) or self.isOpponentPiece(x,y, board)

    def __repr__(self) -> str:
        return self.notation

    def moveAvoidCheck(self, newPosition, board, opponent):
        """
        Retourne True si le mouvement empêche un échec
        """
        # On fait comme si le mouvement avait lieu et on regarde si le player est toujours en échec
        # print("1",board)
        newX, newY = newPosition # On récupère les coordonnées de la nouvelle position
        # Coordonnées de l'ancienne
        firstX = self.x
        firstY = self.y
        caseArrivee = board.grid[newY][newX] # On récupère ce qui est dans la case d'arrivée, pour pouvoir le remettre après


        # On fait le move (pour tester s'il permet d'éviter un échec)
        self.x = newX
        self.y = newY
        board.grid[firstY][firstX] = None # On efface la case de départ 
        board.grid[newY][newX] = self # On remplit la case d'arrivée
        # print("2",board)

        # On regarde si on est toujours en échec (si le mouvement empêche un échec)
        result = self.player.isChecked(board, opponent)

        # On remet tout à sa place 
        self.x = firstX
        self.y = firstY
        board.grid[firstY][firstX] = self # On fait revenir la case
        board.grid[newY][newX] = caseArrivee
        # print("3",board)
        return not result

    
class King(Piece):
    """
    Classe pour le roi
    TODO Great Rock
    TODO Little Rock
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "R"
        
        super().changeNotation()
        
        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}k.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}k.svg"))

        # Contient tous les décalages possibles (ex : (-1, 1), (0, 1),...)
        for dx in [0, -1, 1]:
            for dy in [0, -1, 1] :
                if dx or dy : # si on ne reste pas sur place
                    self.decalages.append((dx, dy))

    def canGreatRock(self, board):
        """
        Il faut reagarder si le roi et la tour n'ont jamais bougé et que les cases entre les deux soient libres
        """
        pass

    def canLittleRock(self, board):
        """
        Il faut reagarder si le roi et la tour n'ont jamais bougé et que les cases entre les deux soient libres
        """
        pass

    def isChecked(self, board, opponent):
        """
        Regarde si le roi est en échec ou non
        """
        isAccessible = self.casesInaccessiblesPourLeRoi(board, opponent)
        return not isAccessible[self.y][self.x] # retourne si la case du roi est accessible ou non

    def casesInaccessiblesPourLeRoi(self, board, opponent):
        """
        Met à jour un tableau avec True si la case est safe et False sinon
        """
        isAccessible = [[True]*8 for _ in range(8)] # On part du principe que tout est accessible

        # Pour toutes les cases
        for x in range(8):
            for y in range(8):
                
                if board.grid[y][x] is not None: # Si on tombe sur une pièce
                    piece = board.grid[y][x]

                    if piece.player == self.player and not isinstance(piece, King): # Si c une pièce alliée différente du roi
                        isAccessible[y][x] = False

                    elif piece.player != self.player: # Piece ennemie
                        cases = piece.getControls(board, self.player)
                        # Pour chaque case accessible par ladite pièce adverse
                        for (X,Y) in cases: # Pour chaque case sous contrôle de l'ennemi
                            if 0<=X<8 and 0<=Y<8 and isAccessible[Y][X] == True: #Si elle n'est pas envore marquée, on la marque
                                isAccessible[Y][X] = False

        return isAccessible

    def getLegalMoves(self, board, opponent):
        """
        Retourne une liste de mouvements légaux
        """
        isAccessible = self.casesInaccessiblesPourLeRoi(board, opponent)
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0<=new_x<8 and 0<=new_y<8 and isAccessible[new_y][new_x]:
                if self.moveAvoidCheck((new_x, new_y), board, opponent):
                    legalMoves.append((new_x, new_y))
        return legalMoves

    def getControls(self, board, opponent):
        return [(self.x+dec_x, self.y+dec_y) for (dec_x, dec_y) in self.decalages]

    

class Queen(Piece):
    """
    Classe pour la reine
    TODO Legal moves
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "D"
        self.valeur = 9
        super().changeNotation()

        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}q.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}q.svg"))

        # Contient tous les décalages 
        for i in range(-7,8):
            self.decalages.append((0,i))
            self.decalages.append((i,0))
            self.decalages.append((i,i))
            self.decalages.append((i,-i))
    
    def getLegalMoves(self, board, opponent):
        """
        Retourne une liste de mouvements légaux
        """
        possibleMoves = []
        for dx in (-1, 0, 1) :
            for dy in (-1, 0, 1) :
                if dx != 0 or dy != 0 :
                    possibleMoves += self.moveLegal(board, dx, dy, opponent)
        return possibleMoves

    def getControls(self, board, opponent):
        """
        Retourne une liste de mouvements légaux
        """
        possibleMoves = []
        for dx in (-1, 0, 1) :
            for dy in (-1, 0, 1) :
                if dx != 0 or dy != 0 :
                    possibleMoves += self.moveTheoric(board, dx, dy, opponent)
        return possibleMoves

        
class Pawn(Piece):
    """
    TODO - En passant move
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "P"
        self.valeur = 1 
        super().changeNotation()

        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}p.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}p.svg"))


        # self.tourAuMomentOuElleAvanceDeDeuxCases = None # Pour gérer en Passant

        if self.color == WHITE:
            self.promotionLine = 0
            self.direction = -1
        else: 
            self.promotionLine = 7
            self.direction = +1

    def getLegalMoves(self, board, opponent):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = []

        # On teste si on peut avancer de 1
        new_y = self.y + self.direction
        #i.e. que la case suivante est vide
        if self.isEmpty(self.x, new_y, board): 
            if self.moveAvoidCheck((self.x, new_y),board, opponent):
                legalMoves.append((self.x, new_y))
        # On teste à gauche et à droite

        new_x = self.x-1
        # On regarde à gauche
        if self.isOpponentPiece(new_x, new_y, board): 
            if self.moveAvoidCheck((new_x, new_y),board, opponent):
                legalMoves.append((new_x, new_y))
        # On regarde à droite
        new_x = self.x+1
        if self.isOpponentPiece(new_x, new_y, board): 
            if self.moveAvoidCheck((new_x, new_y),board, opponent):
                legalMoves.append((new_x, new_y))

        # On peut avencer de deux cases
        new_y = self.y + 2*self.direction
        if not self.alreadyMoved and self.isEmpty(self.x, new_y, board): 
            if self.moveAvoidCheck((self.x, new_y),board, opponent):
                legalMoves.append((self.x, new_y))

        return legalMoves


    def getControls(self, board, opponent):
        """
        Retourne une liste des cases controlées
        """
        controls = [] 
        new_y = self.y + self.direction
        new_x = self.x-1
        # On regarde à gauche
        controls.append((new_x, new_y))
        # On regarde à droite
        new_x = self.x+1
        controls.append((new_x, new_y))
        return controls
   
        
        
class Tower(Piece):
    """
    Classe tower
    TODO movements
    """
    def __init__ (self, color, x, y, player) :
        super().__init__(color, x, y, player)
        self.notation = "T"
        self.valeur = 3 
        super().changeNotation()
        # self.IMAGE = load_svg(pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}r.svg")))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}r.svg"))

    
    def getLegalMoves(self, board, opponent) :
        return self.moveLegal(board, 1, 0, opponent) + self.moveLegal(board, -1, 0, opponent) + self.moveLegal(board, 0, 1, opponent) + self.moveLegal(board, 0, -1, opponent)
    
    def getControls(self, board, opponent):
        """
        Renvoie les cases controlées
        """
        return self.moveTheoric(board, 1, 0, opponent) + self.moveTheoric(board, -1, 0, opponent) + self.moveTheoric(board, 0, 1, opponent) + self.moveTheoric(board, 0, -1, opponent)
        
class Bishop(Piece):
    """
    Classe fou
    TODO movements
    """
    def __init__(self, color,x,y,player):
        super().__init__(color,x,y,player)
        self.notation = "F"
        self.valeur = 3
        super().changeNotation()
        
        # self.IMAGE = pygame.image.load(os.path.join(self.assets_folder, f"{color.lower()[0]}b.svg"))
        self.IMAGE = load_svg(os.path.join(self.assets_folder, f"{color.lower()[0]}b.svg"))
    
    def getLegalMoves(self, board, opponent) :
        return self.moveLegal(board, 1, 1, opponent) + self.moveLegal(board, -1, 1, opponent) + self.moveLegal(board, -1, -1, opponent) + self.moveLegal(board, 1, -1, opponent)
    
    def getControls(self, board, opponent) :
        """
        Renvoie les cases contrôlées
        """
        return self.moveTheoric(board, 1, 1, opponent) + self.moveTheoric(board, 1, -1, opponent) + self.moveTheoric(board, -1, 1, opponent) + self.moveTheoric(board, -1, -1, opponent)
        
        
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

    def getLegalMoves(self, board, opponent):
        """
        Retourne une liste de mouvements légaux
        """
        legalMoves = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0 <= new_x < 8 and 0<= new_y < 8:
                if self.isEmpty(new_x, new_y, board): # Case vide
                    if self.moveAvoidCheck((new_x, new_y), board, opponent):
                        legalMoves.append((new_x, new_y))
                elif self.isOpponentPiece(new_x, new_y, board): # Case appartenant à l'adversaire
                    if self.moveAvoidCheck((new_x, new_y), board, opponent):
                        legalMoves.append((new_x, new_y))
        return legalMoves

    def getControls(self, board, opponent):
        """
        Retourne une liste des cases contrôlées
        """

        controls = [] # couples de positions (x, y) possibles
        for dec_x, dec_y in self.decalages:
            new_x = self.x+dec_x
            new_y = self.y+dec_y
            if 0 <= new_x < 8 and 0<= new_y < 8:
                if self.isEmptyOrOpponentPiece(new_x, new_y, board):
                    controls.append((new_x, new_y))
               
        return controls
                