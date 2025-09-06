from pytest import fixture
from morajai.board import Board, BoardSpaceColors, CompactBoard

#pylint: disable=redefined-outer-name
@fixture
def board():
    return Board()


@fixture
def first_board():
    rv = Board()
    rv.set_space(0, 2, BoardSpaceColors.PINK)
    rv.set_space(1, 0, BoardSpaceColors.YELLOW)
    rv.set_space(2, 0, BoardSpaceColors.YELLOW)
    rv.set_space(1, 1, BoardSpaceColors.YELLOW)
    rv.set_space(2, 1, BoardSpaceColors.YELLOW)
    return rv


@fixture
def compact_board(board):
    return CompactBoard(board)

@fixture
def compact_first_board(first_board):
    return CompactBoard(first_board)