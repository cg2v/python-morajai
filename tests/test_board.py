import pytest
from morajai.board import BoardSpaceColors, CoordinateError


def test_empty_repr(board):
    assert repr(board) == "E E E\nE E E\nE E E"

def test_first_board_repr(first_board):
    assert repr(first_board) == "P E E\nE Y Y\nE Y Y"

def test_set_get_space(board):
    assert board.get_space(0, 0) == BoardSpaceColors.GRAY
    board.set_space(0, 0, BoardSpaceColors.RED)
    assert board.get_space(0, 0) == BoardSpaceColors.RED

def test_set_space_invalid_type(board):
    with pytest.raises(TypeError):
        board.set_space(0, 0, "invalid_type")

def test_set_space_invalid_coordinates(board):
    with pytest.raises(IndexError):
        board.set_space(-1, 0, BoardSpaceColors.RED)
    with pytest.raises(IndexError):
        board.set_space(0, -1, BoardSpaceColors.RED)
    with pytest.raises(IndexError):
        board.set_space(3, 0, BoardSpaceColors.RED)
    with pytest.raises(IndexError):
        board.set_space(0, 3, BoardSpaceColors.RED)

def test_get_space_invalid_coordinates(board):
    with pytest.raises(IndexError):
        board.get_space(-1, 0)
    with pytest.raises(IndexError):
        board.get_space(0, -1)
    with pytest.raises(IndexError):
        board.get_space(3, 0)
    with pytest.raises(IndexError):
        board.get_space(0, 3)

def test_copy_board(first_board):
    copied_board = first_board.copy()
    assert repr(copied_board) == repr(first_board)
    assert copied_board is not first_board
    assert copied_board.get_space(0, 1) == BoardSpaceColors.GRAY
    assert copied_board.get_space(1, 0) == BoardSpaceColors.YELLOW
    assert copied_board.get_space(1, 1) == BoardSpaceColors.YELLOW
    assert copied_board.get_space(0, 0) == BoardSpaceColors.GRAY
    assert copied_board.get_space(2, 2) == BoardSpaceColors.GRAY

def test_get_surrounding_spaces(board):
    assert board.get_surrounding_spaces((0, 0)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
    ]
    assert board.get_surrounding_spaces((1, 1)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
    ]
    assert board.get_surrounding_spaces((2, 2)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
    ]

def test_get_surrounding_spaces_invalid_coordinates(board):
    with pytest.raises(CoordinateError):
        board.get_surrounding_spaces((-1, 0))
    with pytest.raises(CoordinateError):
        board.get_surrounding_spaces((0, -1))
    with pytest.raises(CoordinateError):
        board.get_surrounding_spaces((3, 0))
    with pytest.raises(CoordinateError):
        board.get_surrounding_spaces((0, 3))

def test_get_num_surrounding_spaces(board):
    assert board.get_num_surrounding_spaces((0, 0)) == 3
    assert board.get_num_surrounding_spaces((0, 1)) == 5
    assert board.get_num_surrounding_spaces((1, 0)) == 5
    assert board.get_num_surrounding_spaces((1, 1)) == 8
    assert board.get_num_surrounding_spaces((2, 1)) == 5
    assert board.get_num_surrounding_spaces((2, 2)) == 3

def test_get_num_surrounding_spaces_invalid_coordinates(board):
    with pytest.raises(CoordinateError):
        board.get_num_surrounding_spaces((-1, 0))
    with pytest.raises(CoordinateError):
        board.get_num_surrounding_spaces((0, -1))
    with pytest.raises(CoordinateError):
        board.get_num_surrounding_spaces((3, 0))
    with pytest.raises(CoordinateError):
        board.get_num_surrounding_spaces((0, 3))

def test_surrounding_spaces2(first_board):
    assert first_board.get_surrounding_spaces((0, 0)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
    ]
    assert first_board.get_surrounding_spaces((1, 1)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.PINK,
    ]
    assert first_board.get_surrounding_spaces((2, 2)) == [
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.GRAY,
    ]
    assert first_board.get_surrounding_spaces((0, 2)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.GRAY,
    ]
    assert first_board.get_surrounding_spaces((2, 0)) == [
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
    ]
    assert first_board.get_surrounding_spaces((1, 0)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
    ]