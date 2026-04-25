
from typing import Callable, Sequence
from collections import Counter

from . import board

PRESS = Callable[[board.BoardBase, tuple[int, int]], board.BoardBase]

def press_gray(data: board.BoardBase, _: tuple[int, int]) -> board.BoardBase:
    return data.copy()


def press_black(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """Rotate row to the right."""
    new_board = data.copy()
    _, y = coord
    if 0 <= y < 3:
        row = [data.get_space(i, y) for i in range(3)]
        row = [row[-1]] + row[:-1]  # Rotate right
        for j in range(3):
            new_board.set_space(j, y, row[j])
    return new_board

def press_green(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """Swap with opposite spaces"""
    new_board = data.copy()
    x, y = coord
    if 0 <= x < 3 and 0 <= y < 3:
        temp = data.get_space(x, y)
        new_board.set_space(x, y, data.get_space(2 - x, 2 - y))
        new_board.set_space(2 - x, 2 - y, temp)
    return new_board

def press_pink(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """Rotate spaces clockwise"""
    new_board = data.copy()
    spaces = data.get_surrounding_spaces(coord)
    spaces = [spaces[-1]] + spaces[:-1]  # Rotate clockwise
    new_board.set_surrounding_spaces(coord, spaces)
    return new_board

def press_yellow(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """swap yellow tile with tile above, no effect at (x, 2)"""
    new_board = data.copy()
    x, y = coord
    if 0 <= x < 3 and 0 <= y < 2:
        temp = data.get_space(x, y)
        new_board.set_space(x, y, data.get_space(x, y + 1))
        new_board.set_space(x, y + 1, temp)
    return new_board

def press_violet(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """swap violet tile with tile below, no effect at (x, 0)"""
    new_board = data.copy()
    x, y = coord
    if 0 <= x < 3 and 0 < y < 3:
        temp = data.get_space(x, y)
        new_board.set_space(x, y, data.get_space(x, y - 1))
        new_board.set_space(x, y - 1, temp)
    return new_board

def press_white(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """Sets all surrounding gray tiles to white. If there are none, sets itself to gray"""
    data = data.copy()
    adjacent = data.get_surrounding_spaces(coord)
    for i, color in enumerate(adjacent):
        if color == board.BoardSpaceColors.GRAY:
            adjacent[i] = board.BoardSpaceColors.WHITE
    data.set_surrounding_spaces(coord, adjacent)
    if all(color != board.BoardSpaceColors.WHITE for color in adjacent):
        data.set_space(*coord, board.BoardSpaceColors.GRAY)
    return data

def press_red(data: board.BoardBase, _: tuple[int, int]) -> board.BoardBase:
    new_board = data.copy()
    for i in range(3):
        for j in range(3):
            current = data.get_space(i, j)
            if current == board.BoardSpaceColors.WHITE:
                new_board.set_space(i, j, board.BoardSpaceColors.BLACK)
            elif current == board.BoardSpaceColors.BLACK:
                new_board.set_space(i, j, board.BoardSpaceColors.RED)
    return new_board

def press_orange(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """Set orange tile to most common adjacent color if it is a majority"""
    data = data.copy()
    num_adjacent = data.get_num_surrounding_spaces(coord)
    counts = Counter(data.get_surrounding_spaces(coord))
    most_common = counts.most_common(1)
    if most_common:
        color, count = most_common[0]
        if count > num_adjacent // 2:
            data.set_space(*coord, color)
    return data

EVOLUTIONS : Sequence[PRESS] = [
    press_gray,
    press_black,
    press_green,
    press_pink,
    press_yellow,
    press_violet,
    press_white,
    press_red,
    press_orange
]

def press_blue(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """Copies the function of the center tile"""
    center = data.get_space(1, 1)
    if center == board.BoardSpaceColors.BLUE:
        return data.copy()
    function = EVOLUTIONS[center.value]
    data = function(data, coord)
    return data

def press(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    x, y = coord
    piece = data.get_space(x, y)
    if piece == board.BoardSpaceColors.BLUE:
        return press_blue(data, coord)
    function = EVOLUTIONS[piece.value]
    data = function(data, coord)
    return data
