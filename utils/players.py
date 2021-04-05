import pygame
from utils.varglob import WHITE, BLACK, Color
from utils.pieces import Pawn, King, Piece, Queen, Bishop, Tower, Knight


class Player():
    def __init__(self, board, color) -> None:
        # Positionnement des pièces
        self.pieces = []
        self.captured = []
        self.color = color

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

    def waitPickPiece(self, board, opponent, window):
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

    def waitMovePiece(self, board, opponent, window):
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
        
    def captureTerritoire(self, x, y, opponent, board) :
        """
        # S'occupe de la capture terrritoire
        Retourne une croix s'il y a capture
        """
        if board.grid[y][x] is not None:
            self.captured.append(board.grid[y][x])
            opponent.pieces.remove(board.grid[y][x])
            board.grid[y][x] = None
            return "x" # Pour la notation
        return ""

    def moveSinglePiece(self, piece, newX, newY, board, opponent, window, nbCoups):
        """
        Bouge une pièce
        Gère la promotion également
        """
        board.grid[piece.y][piece.x] = None # On efface la pièce du jeu
        
        # On regarde si une pièce ennemi a été capturée
        suffix = self.captureTerritoire(newX, newY, opponent, board)

        # On dépose notre pièce
        piece.x = newX
        piece.y = newY
        piece.alreadyMoved = True
        piece.lastMove = nbCoups
        piece.nbFoisMoved += 1
        
        # On regarde s'il y a promotion
        if isinstance(piece, Pawn) and piece.y == piece.promotionLine: # On fait une promotion
            pieceDemandee = self.askPromotionPiece(window, piece.x, piece.y)

            self.pieces.remove(piece)
            self.pieces.append(pieceDemandee)

            # pieceDemandee.x = piece.x
            # pieceDemandee.y = piece.y
            board.grid[newY][newX] = pieceDemandee
        else:
            board.grid[newY][newX] = piece
        return suffix
        

    def turn(self, board, opponent, window, nbCoups, register):
        """
        Simule le tour de player
        """
        # print("CKECKING if check mate")
        etat = self.isCheckedMated(board, opponent, nbCoups)
        if etat < 2:
            return etat

        # print("NOT CHECK MATE")
        pieceSelectionne = False
        possibleMoves = None
        done = False
       

        posDep = posArr = None
        piece = None

        special = None
        suffix = ""
        # TODO gérer l'intéraction avec le joueur pour récupérer la case sélectionnée
        # On reagarde si le joueur a cliqué sur une pièc
        while not done:
            if not pieceSelectionne: # On a pas encore choisi de pièce
                piece = self.waitPickPiece(board, opponent, window)
                posDep = (piece.x, piece.y)
                pieceSelectionne =  True # On a une pièce
                possibleMoves = piece.getLegalMoves(board, opponent, nbCoups) # On regarde ses moves possibles
                board.markCases(possibleMoves, window) # On marque les positions possibles

            # On regarde quelle position il choisit
            posArr = self.waitMovePiece(board, opponent, window)
            if posArr in possibleMoves: # On a trouvé le coup
                done = True

            elif posArr is not None: # On a touché à côté, i.e. on annule le coup
                pieceSelectionne = False
                board.updateGraphicalInterface(window, [self, opponent])
            
            
        # On a la position de départ et celle d'arrivée
        # *On effectue le mouvement
        xDep,yDep = posDep
        newX, newY = posArr
        suffix += self.moveSinglePiece(piece, newX, newY, board, opponent, window, nbCoups)

        #* On regarde si l'on a fait en passant :)
        if isinstance(piece, Pawn) and piece.y == (piece.enPassantLine + piece.direction): # Si on est un pion et qu'on vient de dépasser la ligne "en passant"
            # On regarde si en-dessous, il y a un pion vulnérable
            # print("HELLO")
            if piece.isPawnVulnerableForEnPassant(piece.x, piece.enPassantLine, board, opponent, nbCoups):
                # print("HELLO") # pour le debug
                suffix += self.captureTerritoire(piece.x, piece.enPassantLine, opponent, board)

        #* Si l'on a fait un rock ?
        if isinstance(piece, King) and abs(piece.x-xDep)==2: #Si c'est un roi et qu'on a fait un déplacement de deux alors c'est un rock
            if piece.x == 2: # Grand rock
                special = "0-0-0"
                self.moveSinglePiece(board.grid[piece.y][0], 3, piece.y, board, opponent, window, nbCoups)
            else: # Petit rock
                special = "0-0"
                self.moveSinglePiece(board.grid[piece.y][7], 5, piece.y, board, opponent, window, nbCoups)

        if opponent.isCheckedMated(board, self, nbCoups)==0:
            suffix += "#" # Notation pour l'échec et mat
        elif opponent.isChecked(board, self):
            suffix += "+"


        register.addMove(piece, suffix, special)
        register.save()
        board.updateGraphicalInterface(window, [self, opponent])
        
        return etat

    def askPromotionPiece(self, window, x,y):
        """
        Demande quelle pièce il veut choisir
        Retourne une instance de la pièce choisie
        """
        # On forme une image au-dessus ou en-dessous du terrain en fonction de qui promote
       
        
        pygame.draw.rect(window, Color.WHITE.value, (400,400,200,200))
        # On affiche les images
        # En haut à gauche
        q = Queen(self.color, x, y, self)
        window.blit(q.IMAGE, (400,400))
        # En haut à droite
        t = Tower(self.color, x, y, self)
        window.blit(t.IMAGE, (400,500))
        # En bas à gauche
        c = Knight(self.color, x, y, self)
        window.blit(c.IMAGE, (500, 400))
        # En bas à droite
        b = Bishop(self.color, x, y, self)
        window.blit(b.IMAGE, (500, 500))
        pygame.display.update()

        # ON regarde ou l'utilisateur clique
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # On a choisi une piece ?
                    mousePosition = pygame.mouse.get_pos() # On récupère la position
                    x = mousePosition[0]//100 - 4
                    y = mousePosition[1]//100 - 4
                    if x==0:
                        if y==0:
                            return q
                        else :
                            return t
                    else : # knight or bishop
                        if y == 0 :
                            return c
                        else :
                            return b
            pygame.time.delay(100) # On attend un peu pour ne pas trop surmener l'ordi
        return None

    def isChecked(self, board, opponent):
        return self.king.isChecked(board, opponent)

    def isCheckedMated(self, board, opponent, nbCoups):
        """
        Fonction déterminant si le joueur est mort ou non
        Renvoie un nombre :
        0 -> défaite
        1 -> nulle
        2 -> peut encore jouer
        """
        if self.king not in self.pieces:
            return 0
        for i,piece in enumerate(self.pieces):
            # print(i, piece)

            if len(piece.getLegalMoves(board, opponent, nbCoups))>0: # On a au moins un move possible
                return 2
        
        if self.isChecked(board, opponent): # On est en échec
            return 0
        return 1 # on n'est pas en échec mais aucune position accessible