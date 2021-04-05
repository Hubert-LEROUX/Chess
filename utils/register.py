from datetime import date
import os

from utils.varglob import WHITE, BLACK, ALPHABET
from utils.pieces import Piece



class Register():
    """
    Un registre de la partie
    """

    def __init__(self, saveName=None, whiteName=None, blackName=None) -> None:
        self.date = date.today()
        self.whiteName = whiteName
        self.blackName = blackName
        self.moves = []
        self.name = saveName

    def addMove(self, piece, suffix="", special=None):
        if piece.color == BLACK: # On ajoute à la fin
            self.moves[-1] += " " + self.translateMove(piece, suffix, special)
        else:
            self.moves.append(self.translateMove(piece, suffix, special))

    def translateMove(self, piece, suffix="", special=None):
        if special is None:
            return piece.notation + ALPHABET[piece.x%8] + str(8-piece.y) + suffix
        return special


    def __repr__(self):
        rep = f"""Date : {self.date.strftime('%B %d, %Y')}
Number of moves : {len(self.moves)}
White Name : {self.whiteName}
Black Name : {self.blackName}
=== RESUME ===\n"""
        for i, move in enumerate(self.moves, 1):
            rep+= f"{i} {move}\n"
        return rep

    def save(self):
        if self.name is not None:
            folder = "games"
            path = os.path.join(folder, self.name)
            with open(path, "w") as file:
                file.write(str(self))


if __name__ == "__main__":
    register = Register()
    print(register)
