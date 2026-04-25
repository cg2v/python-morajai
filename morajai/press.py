
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

def _orthogonal_neighbors(x: int, y: int):
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            yield (nx, ny)

def press_white(data: board.BoardBase, coord: tuple[int, int]) -> board.BoardBase:
    """Turns itself and orthogonally-linked white tiles grey; grey tiles orthogonally-adjacent to those become white."""
    pressed_color = data.get_space(*coord)
    # BFS flood-fill to collect all orthogonally-linked tiles of the same color
    group: set[tuple[int, int]] = set()
    queue = [coord]
    while queue:
        cur = queue.pop()
        if cur in group:
            continue
        if data.get_space(*cur) == pressed_color:
            group.add(cur)
            for neighbor in _orthogonal_neighbors(*cur):
                if neighbor not in group:
                    queue.append(neighbor)
    # Collect orthogonal gray neighbors of the group (from original board)
    gray_neighbors: set[tuple[int, int]] = set()
    for tile in group:
        for neighbor in _orthogonal_neighbors(*tile):
            if neighbor not in group and data.get_space(*neighbor) == board.BoardSpaceColors.GRAY:
                gray_neighbors.add(neighbor)
    new_board = data.copy()
    for tile in group:
        new_board.set_space(*tile, board.BoardSpaceColors.GRAY)
    for tile in gray_neighbors:
        new_board.set_space(*tile, pressed_color)
    return new_board

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
