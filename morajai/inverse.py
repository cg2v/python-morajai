from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Iterator, Sequence

from . import board

# Returns all predecessor boards P such that forward_press(P, coord) == data.
INVERSE_PRESS = Callable[[board.BoardBase, tuple[int, int]], Sequence[board.BoardBase]]


def _single(result: board.BoardBase) -> Sequence[board.BoardBase]:
    return [result]


def inverse_press_gray(data: board.BoardBase, _: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Identity
    return _single(data.copy())


def inverse_press_black(data: board.BoardBase, coord: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Forward black rotates row right, so inverse is row-left rotation.
    new_board = data.copy()
    _, y = coord
    if 0 <= y < 3:
        row = [data.get_space(i, y) for i in range(3)]
        row = row[1:] + [row[0]]  # Rotate left
        for x in range(3):
            new_board.set_space(x, y, row[x])
    return _single(new_board)


def inverse_press_green(data: board.BoardBase, coord: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Swap with opposite is self-inverse.
    new_board = data.copy()
    x, y = coord
    if 0 <= x < 3 and 0 <= y < 3:
        other = (2 - x, 2 - y)
        tmp = data.get_space(x, y)
        new_board.set_space(x, y, data.get_space(*other))
        new_board.set_space(*other, tmp)
    return _single(new_board)


def inverse_press_pink(data: board.BoardBase, coord: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Forward pink rotates neighbors clockwise. Inverse is counter-clockwise.
    new_board = data.copy()
    spaces = data.get_surrounding_spaces(coord)
    if spaces:
        spaces = spaces[1:] + [spaces[0]]  # Rotate counter-clockwise
        new_board.set_surrounding_spaces(coord, spaces)
    return _single(new_board)


def inverse_press_yellow(data: board.BoardBase, coord: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Yellow swap is self-inverse.
    new_board = data.copy()
    x, y = coord
    if 0 <= x < 3 and 0 <= y < 2:
        tmp = data.get_space(x, y)
        new_board.set_space(x, y, data.get_space(x, y + 1))
        new_board.set_space(x, y + 1, tmp)
    return _single(new_board)


def inverse_press_violet(data: board.BoardBase, coord: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Violet swap is self-inverse.
    new_board = data.copy()
    x, y = coord
    if 0 <= x < 3 and 0 < y < 3:
        tmp = data.get_space(x, y)
        new_board.set_space(x, y, data.get_space(x, y - 1))
        new_board.set_space(x, y - 1, tmp)
    return _single(new_board)


def inverse_press_white(_: board.BoardBase, __: tuple[int, int]) -> Sequence[board.BoardBase]:
    # White is many-to-one with potentially large predecessor sets.
    # Keep explicit to avoid silently incorrect predecessor generation.
    raise NotImplementedError("inverse of white press is non-trivial and not uniquely defined")


def _inverse_red_cell_values(
    current: board.BoardSpaceColors,
) -> Sequence[board.BoardSpaceColors]:
    # Forward red: WHITE->BLACK, BLACK->RED, others unchanged.
    # So inverse per cell:
    #   RED   <- {RED, BLACK}
    #   BLACK <- {WHITE}
    #   WHITE <- {}
    #   other <- {other}
    C = board.BoardSpaceColors
    if current == C.RED:
        return (C.RED, C.BLACK)
    if current == C.BLACK:
        return (C.WHITE,)
    if current == C.WHITE:
        return ()
    return (current,)


def _iter_all_red_preimages(data: board.BoardBase) -> Iterator[board.BoardBase]:
    choices: list[tuple[int, int, Sequence[board.BoardSpaceColors]]] = []
    for x in range(3):
        for y in range(3):
            options = _inverse_red_cell_values(data.get_space(x, y))
            if not options:
                return
            choices.append((x, y, options))

    # At most 2^9 boards (where every cell is RED), manageable.
    boards = [board.Board()]
    for x, y, options in choices:
        next_boards: list[board.Board] = []
        for partial in boards:
            for color in options:
                b = partial.copy()
                b.set_space(x, y, color)
                next_boards.append(b)
        boards = next_boards

    for b in boards:
        yield b


def inverse_press_red(data: board.BoardBase, _: tuple[int, int]) -> Sequence[board.BoardBase]:
    return list(_iter_all_red_preimages(data))


def _orange_would_change(
    b: board.BoardBase, coord: tuple[int, int], from_color: board.BoardSpaceColors
) -> bool:
    # Determine whether forward orange would overwrite coord based on neighbors.
    num_adjacent = b.get_num_surrounding_spaces(coord)
    counts = Counter(b.get_surrounding_spaces(coord))
    most_common = counts.most_common(1)
    if not most_common:
        return False
    color, count = most_common[0]
    if count > num_adjacent // 2:
        return color != from_color
    return False


def inverse_press_orange(data: board.BoardBase, coord: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Only the pressed tile can differ pre-press.
    # Enumerate predecessor pressed-tile colors that would produce final tile value.
    x, y = coord
    if not (0 <= x < 3 and 0 <= y < 3):
        return []

    final_color = data.get_space(x, y)
    candidates: list[board.BoardBase] = []
    for c in board.BoardSpaceColors:
        pred = data.copy()
        pred.set_space(x, y, c)

        # Simulate orange rule from predecessor and test result at pressed tile.
        num_adjacent = pred.get_num_surrounding_spaces(coord)
        counts = Counter(pred.get_surrounding_spaces(coord))
        most_common = counts.most_common(1)
        out = c
        if most_common:
            maj_color, count = most_common[0]
            if count > num_adjacent // 2:
                out = maj_color

        if out == final_color:
            candidates.append(pred)

    # Deduplicate by board hash/eq
    uniq: dict[int, board.BoardBase] = {}
    for b in candidates:
        uniq[hash(b)] = b
    return list(uniq.values())


def inverse_press_blue(data: board.BoardBase, coord: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Blue copies the center tile's function from predecessor board.
    # Enumerate possible predecessor center colors and invert that operator.
    C = board.BoardSpaceColors
    out: list[board.BoardBase] = []

    inverse_ops = INVERSE_EVOLUTIONS

    # Case 1: predecessor center is BLUE -> forward blue is no-op.
    out.append(data.copy())

    # Case 2: predecessor center is one of 0..8 and blue applies that function.
    for center_color in C:
        if center_color == C.BLUE:
            continue
        if center_color.value >= len(inverse_ops):
            continue

        inv_op = inverse_ops[center_color.value]
        for pred in inv_op(data, coord):
            pred2 = pred.copy()
            pred2.set_space(1, 1, center_color)
            out.append(pred2)

    uniq: dict[int, board.BoardBase] = {}
    for b in out:
        uniq[hash(b)] = b
    return list(uniq.values())


INVERSE_EVOLUTIONS: Sequence[INVERSE_PRESS] = [
    inverse_press_gray,
    inverse_press_black,
    inverse_press_green,
    inverse_press_pink,
    inverse_press_yellow,
    inverse_press_violet,
    inverse_press_white,
    inverse_press_red,
    inverse_press_orange,
]


def inverse_press(data: board.BoardBase, coord: tuple[int, int]) -> Sequence[board.BoardBase]:
    # Backward operator dispatcher based on final pressed-tile color.
    # This mirrors forward dispatch shape but returns a predecessor set.
    x, y = coord
    piece = data.get_space(x, y)
    if piece == board.BoardSpaceColors.BLUE:
        return inverse_press_blue(data, coord)

    if piece.value >= len(INVERSE_EVOLUTIONS):
        return []

    return INVERSE_EVOLUTIONS[piece.value](data, coord)