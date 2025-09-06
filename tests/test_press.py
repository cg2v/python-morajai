
from morajai.board import BoardSpaceColors
from morajai.press import press

def test_first_noops(first_board):
    new_board = press(first_board, (0, 0))
    assert new_board == first_board
    new_board = press(first_board, (1, 0))
    assert new_board == first_board
    new_board = press(first_board, (2, 0))
    assert new_board == first_board
    new_board = press(first_board, (1, 2))
    assert new_board == first_board
    new_board = press(first_board, (2, 2))
    assert new_board == first_board


def test_first_pink(first_board):
    new_board = press(first_board, (0, 2))
    assert new_board.get_space(0, 0) == BoardSpaceColors.GRAY
    assert new_board.get_space(0, 1) == BoardSpaceColors.YELLOW
    assert new_board.get_space(0, 2) == BoardSpaceColors.PINK
    assert new_board.get_space(1, 0) == BoardSpaceColors.YELLOW
    assert new_board.get_space(1, 1) == BoardSpaceColors.GRAY
    assert new_board.get_space(1, 2) == BoardSpaceColors.GRAY
    assert new_board.get_space(2, 0) == BoardSpaceColors.YELLOW
    assert new_board.get_space(2, 1) == BoardSpaceColors.YELLOW
    assert new_board.get_space(2, 2) == BoardSpaceColors.GRAY

def test_first_yellow(first_board):
    new_board = press(first_board, (1, 1))
    assert new_board.get_space(0, 0) == BoardSpaceColors.GRAY
    assert new_board.get_space(0, 1) == BoardSpaceColors.GRAY
    assert new_board.get_space(0, 2) == BoardSpaceColors.PINK
    assert new_board.get_space(1, 0) == BoardSpaceColors.YELLOW
    assert new_board.get_space(1, 1) == BoardSpaceColors.GRAY
    assert new_board.get_space(1, 2) == BoardSpaceColors.YELLOW
    assert new_board.get_space(2, 0) == BoardSpaceColors.YELLOW
    assert new_board.get_space(2, 1) == BoardSpaceColors.YELLOW
    assert new_board.get_space(2, 2) == BoardSpaceColors.GRAY
    new_board = press(new_board, (2, 1))
    assert new_board.get_space(0, 0) == BoardSpaceColors.GRAY
    assert new_board.get_space(0, 1) == BoardSpaceColors.GRAY
    assert new_board.get_space(0, 2) == BoardSpaceColors.PINK
    assert new_board.get_space(1, 0) == BoardSpaceColors.YELLOW
    assert new_board.get_space(1, 1) == BoardSpaceColors.GRAY
    assert new_board.get_space(1, 2) == BoardSpaceColors.YELLOW
    assert new_board.get_space(2, 0) == BoardSpaceColors.YELLOW
    assert new_board.get_space(2, 1) == BoardSpaceColors.GRAY
    assert new_board.get_space(2, 2) == BoardSpaceColors.YELLOW
