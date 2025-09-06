import pytest
from morajai.board import BoardSpaceColors, CompactBoard, CoordinateError


def compact_board_from_board(board):
    return CompactBoard(board)



def test_empty_repr_compact(compact_board):
    assert repr(compact_board) == "E E E\nE E E\nE E E"

def test_first_board_repr_compact(compact_first_board):
    assert repr(compact_first_board) == "P E E\nE Y Y\nE Y Y"

def test_get_space_compact(compact_board):
    assert compact_board.get_space(0, 0) == BoardSpaceColors.GRAY
    # CompactBoard is immutable, so we do not test set_space

def test_get_space_invalid_coordinates_compact(compact_board):
    with pytest.raises(IndexError):
        compact_board.get_space(-1, 0)
    with pytest.raises(IndexError):
        compact_board.get_space(0, -1)
    with pytest.raises(IndexError):
        compact_board.get_space(3, 0)
    with pytest.raises(IndexError):
        compact_board.get_space(0, 3)

def test_get_surrounding_spaces_compact(compact_board):
    assert compact_board.get_surrounding_spaces((0, 0)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
    ]
    assert compact_board.get_surrounding_spaces((1, 1)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
    ]
    assert compact_board.get_surrounding_spaces((2, 2)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
    ]

def test_get_surrounding_spaces_invalid_coordinates_compact(compact_board):
    with pytest.raises(CoordinateError):
        compact_board.get_surrounding_spaces((-1, 0))
    with pytest.raises(CoordinateError):
        compact_board.get_surrounding_spaces((0, -1))
    with pytest.raises(CoordinateError):
        compact_board.get_surrounding_spaces((3, 0))
    with pytest.raises(CoordinateError):
        compact_board.get_surrounding_spaces((0, 3))

def test_get_num_surrounding_spaces_compact(compact_board):
    assert compact_board.get_num_surrounding_spaces((0, 0)) == 3
    assert compact_board.get_num_surrounding_spaces((0, 1)) == 5
    assert compact_board.get_num_surrounding_spaces((1, 0)) == 5
    assert compact_board.get_num_surrounding_spaces((1, 1)) == 8
    assert compact_board.get_num_surrounding_spaces((2, 1)) == 5
    assert compact_board.get_num_surrounding_spaces((2, 2)) == 3

def test_get_num_surrounding_spaces_invalid_coordinates_compact(compact_board):
    with pytest.raises(CoordinateError):
        compact_board.get_num_surrounding_spaces((-1, 0))
    with pytest.raises(CoordinateError):
        compact_board.get_num_surrounding_spaces((0, -1))
    with pytest.raises(CoordinateError):
        compact_board.get_num_surrounding_spaces((3, 0))
    with pytest.raises(CoordinateError):
        compact_board.get_num_surrounding_spaces((0, 3))

def test_surrounding_spaces2_compact(compact_first_board):
    assert compact_first_board.get_surrounding_spaces((0, 0)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
    ]
    assert compact_first_board.get_surrounding_spaces((1, 1)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.PINK,
    ]
    assert compact_first_board.get_surrounding_spaces((2, 2)) == [
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.GRAY,
    ]
    assert compact_first_board.get_surrounding_spaces((0, 2)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.GRAY,
    ]
    assert compact_first_board.get_surrounding_spaces((2, 0)) == [
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
    ]
    assert compact_first_board.get_surrounding_spaces((1, 0)) == [
        BoardSpaceColors.GRAY,
        BoardSpaceColors.GRAY,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
        BoardSpaceColors.YELLOW,
    ]
