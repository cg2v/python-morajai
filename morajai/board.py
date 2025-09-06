from abc import ABC, abstractmethod
from enum import Enum
from collections.abc import Sequence

class BoardSpaceColors(Enum):
    GRAY = 0
    BLACK = 1
    GREEN = 2
    PINK = 3
    YELLOW = 4
    VIOLET = 5
    WHITE = 6
    RED = 7
    ORANGE = 8
    BLUE = 9

    @property
    def abbrev(self) -> str:
        if self == BoardSpaceColors.GRAY:
            return "E"
        if self == BoardSpaceColors.BLACK:
            return "K"
        return self.name[0].upper()

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7

class CoordinateError(ValueError, IndexError):
    pass

def get_clockwise_coordinate(ref: tuple[int, int]) -> Sequence[tuple[int, int]]:
    match (ref):
        case (0, 0):
            return ((0, 1), (1,1), (1,0))
        case (0, 1):
            return ((0, 2), (1,2), (1,1), (1, 0), (0, 0))
        case (0, 2):
            return ((1, 2), (1,1), (0, 1))
        case (1, 0):
            return ((0, 0), (0, 1), (1, 1), (2, 1), (2, 0))
        case (1, 1):
            return ((1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2))
        case (1, 2):
            return ((2, 2), (2, 1), (1, 1), (0, 1), (0, 2))
        case (2, 0):
            return ((1, 0), (1, 1), (2, 1))
        case (2, 1):
            return ((2, 0), (1, 0), (1, 1), (1, 2), (2, 2))
        case (2, 2):
            return ((2, 1), (1, 1), (1, 2))
        case _:
            return ()


class BoardBase(ABC):
    @abstractmethod
    def get_space(self, x: int, y: int) -> BoardSpaceColors:
        pass

    def __repr__(self):
        rows = []
        for row in reversed(range(3)):
            rowtext = ""
            for col in range(3):
                rowtext += self.get_space(col, row).abbrev + " "
            rows.append(rowtext.strip())
        return "\n".join(rows)

    def get_num_surrounding_spaces(self, coord: tuple[int, int]) -> int:
        if any(map(lambda c: c < 0 or c > 2, coord)):
            raise CoordinateError("Invalid board coordinates")
        if all(map(lambda c: c != 1, coord)):
            return 3
        if any(map(lambda c: c != 1, coord)):
            return 5
        return 8
 
    def get_surrounding_spaces(self, coord: tuple[int, int]) -> list[BoardSpaceColors]:
        if any(map(lambda c: c < 0 or c > 2, coord)):
            raise CoordinateError("Invalid board coordinates")
        coords = get_clockwise_coordinate(coord)
        return [self.get_space(x, y) for (x, y) in coords]

    def copy(self) -> "Board":
        new_board = Board()
        for x in range(3):
            for y in range(3):
                new_board.set_space(x, y, self.get_space(x, y))
        return new_board

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoardBase):
            return NotImplemented
        for row in range(3):
            for col in range(3):
                if self.get_space(row, col) != other.get_space(row, col):
                    return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, BoardBase):
            return NotImplemented
        return not self == other
    
    def __hash__(self) -> int:
        return hash(tuple(self.get_space(row, col) for row in range(3) for col in range(3)))

class CompactBoard(BoardBase):
    spaces: tuple[int, ...]
    def __init__(self, board: BoardBase):
        self.spaces = tuple(board.get_space(x, y).value for x in range(3) for y in range(3))

    def get_space(self, x: int, y: int) -> BoardSpaceColors:
        if 0 <= x < 3 and 0 <= y < 3:
            return BoardSpaceColors(self.spaces[x * 3 + y])
        raise CoordinateError("Invalid board coordinates")
        

class Board(BoardBase):
    spaces: list[list[BoardSpaceColors]]
    def __init__(self):
        self.spaces = [[BoardSpaceColors.GRAY for _ in range(3)] for _ in range(3)]


    def set_space(self, x: int, y: int, color: BoardSpaceColors):
        if not isinstance(color, BoardSpaceColors):
            if isinstance(color, int):
                color = BoardSpaceColors(color)
            else:
                raise TypeError("Invalid color type")
        if 0 <= x < 3 and 0 <= y < 3:
            self.spaces[x][y] = color
        else:
            raise CoordinateError("Invalid board coordinates")

    def get_space(self, x: int, y: int) -> BoardSpaceColors:
        if 0 <= x < 3 and 0 <= y < 3:
            return self.spaces[x][y]
        raise CoordinateError("Invalid board coordinates")



    def set_surrounding_spaces(self, coord: tuple[int, int], colors: list[BoardSpaceColors]):
        coords = get_clockwise_coordinate(coord)
        if len(colors) != len(coords):
            raise ValueError("Colors list length does not match number of surrounding spaces")
        for (x, y), color in zip(coords, colors):
            self.set_space(x, y, color)

