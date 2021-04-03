WHITE = "WHITE"
BLACK = "BLACK"

SIZE = 8
IMAGE_SIZE = 100

from enum import Enum
class Color(Enum):
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    BROWN = (150, 75, 0)
    DARK_BROWN = (66, 33, 0)