import pygame
from utils.varglob import WHITE, BLACK
from utils.pieces import Pawn, King, Piece, Queen, Bishop, Tower, Knight

class Player():
    def __init__(self, board, color) -> None:
        # Positionnement des pièces
        self.pieces = []
        self.captured = []

        if color == WHITE: # On place les pièces en bas
            yPawns = 6
            yGreatPieces = 7
        else:
            yPawns = 1
            yGreatPieces = 0

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

    def pickPiece(self, board, opponent, window):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # On a choisi une piece ?
                    mousePosition = pygame.mouse.get_pos() # On récupère la position

                    # Il faut la convertir en coordonnées du board.
                    posBoard = board.convertMousePosition2boardPosition(mousePosition)
                    x,y = posBoard
                    # On regarde ce que c'est
                    if 0<=x<8 and 0<=y<8 and board.grid[y][x] is not None and board.grid[y][x].player == self: # C'est une pièce à nous
                        return board.grid[y][x]

            pygame.time.delay(100) # On attend un peu pour ne pas trop surmener l'ordi
        return None

    def movePiece(self, board, opponent, window):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # On a choisi une piece ?
                    mousePosition = pygame.mouse.get_pos() # On récupère la position

                    # Il faut la convertir en coordonnées du board.
                    posBoard = board.convertMousePosition2boardPosition(mousePosition)
                    x,y = posBoard
                    # On regarde ce que c'est
                    if 0<=x<8 and 0<=y<8: 
                        return (x,y)

            pygame.time.delay(100) # On attend un peu pour ne pas trop surmener l'ordi
        return None

    def turn(self, board, opponent, window, nbCoups=0):
        """
        Simule le tour de player
        """
        # print("CKECKING if check mate")

        if self.isCheckedMated(board, opponent):
            return False

        # print("NOT CHECK MATE")
        pieceSelectionne = False
        possibleMoves = None
        done = False
       

        posDep = posArr = None
        piece = None
        # TODO gérer l'intéraction avec le joueur pour récupérer la case sélectionnée
        # On reagarde si le joueur a cliqué sur une pièc
        while not done:
            if not pieceSelectionne: # On a pas encore choisi de pièce
                piece = self.pickPiece(board, opponent, window)
                posDep = (piece.x, piece.y)
                pieceSelectionne =  True # On a une pièce
                possibleMoves = piece.getLegalMoves(board, opponent) # On regarde ses moves possibles
                board.markCases(possibleMoves, window) # On marque les positions possibles

            # On regarde quelle position il choisit
            posArr = self.movePiece(board, opponent, window)
            if posArr in possibleMoves: # On a trouvé le coup
                done = True

            elif posArr is not None: # On a touché à côté, i.e. on annule le coup
                pieceSelectionne = False
                board.updateGraphicalInterface(window, [self, opponent])
            
            
        # On a la position de départ et celle d'arrivée
        # *On effectue le mouvement
        xDep,yDep = posDep
        newX, newY = posArr

        board.grid[yDep][xDep] = None # On efface la pièce du jeu
        
        # On regarde si une pièce ennemi a été capturée
        if board.grid[newY][newX] is not None:
            self.captured.append(board.grid[newY][newX])
            opponent.pieces.remove(board.grid[newY][newX])

        # On dépose notre pièce
        piece.x = newX
        piece.y = newY
        piece.alreadyMoved = True
        piece.lastMove = nbCoups
        board.grid[newY][newX] = piece

        board.updateGraphicalInterface(window, [self, opponent])
        
        return True

    def isChecked(self, board, opponent):
        return self.king.isChecked(board, opponent)

    def isCheckedMated(self, board, opponent):
        """
        Fonction déterminant si le joueur est mort ou non
        """
        if self.king not in self.pieces:
            return True
        for i,piece in enumerate(self.pieces):
            # print(i, piece)

            if len(piece.getLegalMoves(board, opponent))>0: # On a au moins un move possible
                return False

        return True