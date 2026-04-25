
from morajai.board import Board, BoardSpaceColors
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


# --- press_red tests ---

def test_press_red_white_becomes_black():
    """Spec: white tiles become black"""
    b = Board()
    b.set_space(0, 0, BoardSpaceColors.WHITE)
    b.set_space(2, 2, BoardSpaceColors.WHITE)
    b.set_space(1, 1, BoardSpaceColors.RED)
    result = press(b, (1, 1))
    assert result.get_space(0, 0) == BoardSpaceColors.BLACK
    assert result.get_space(2, 2) == BoardSpaceColors.BLACK

def test_press_red_black_becomes_red():
    """Spec: black tiles become red"""
    b = Board()
    b.set_space(0, 0, BoardSpaceColors.BLACK)
    b.set_space(2, 2, BoardSpaceColors.BLACK)
    b.set_space(1, 1, BoardSpaceColors.RED)
    result = press(b, (1, 1))
    assert result.get_space(0, 0) == BoardSpaceColors.RED
    assert result.get_space(2, 2) == BoardSpaceColors.RED

def test_press_red_other_colors_unchanged():
    """Non-white, non-black tiles should not change"""
    b = Board()
    b.set_space(0, 0, BoardSpaceColors.GREEN)
    b.set_space(0, 1, BoardSpaceColors.ORANGE)
    b.set_space(1, 1, BoardSpaceColors.RED)
    result = press(b, (1, 1))
    assert result.get_space(0, 0) == BoardSpaceColors.GREEN
    assert result.get_space(0, 1) == BoardSpaceColors.ORANGE

def test_press_red_both_white_and_black():
    """White→black and black→red in the same press; red tile is not white or black so stays"""
    b = Board()
    b.set_space(0, 0, BoardSpaceColors.WHITE)
    b.set_space(2, 0, BoardSpaceColors.BLACK)
    b.set_space(1, 1, BoardSpaceColors.RED)
    result = press(b, (1, 1))
    assert result.get_space(0, 0) == BoardSpaceColors.BLACK
    assert result.get_space(2, 0) == BoardSpaceColors.RED


# --- press_white tests ---

def test_press_white_turns_self_gray_when_isolated():
    """Spec: pressed white tile with no orthogonally-linked white tiles turns itself grey"""
    b = Board()
    b.set_space(1, 1, BoardSpaceColors.WHITE)
    result = press(b, (1, 1))
    assert result.get_space(1, 1) == BoardSpaceColors.GRAY

def test_press_white_self_and_connected_white_turn_gray():
    """Spec: pressed tile and orthogonally-linked white tiles all become grey"""
    b = Board()
    b.set_space(1, 1, BoardSpaceColors.WHITE)
    b.set_space(1, 2, BoardSpaceColors.WHITE)  # orthogonally linked
    b.set_space(0, 1, BoardSpaceColors.WHITE)  # orthogonally linked
    result = press(b, (1, 1))
    assert result.get_space(1, 1) == BoardSpaceColors.GRAY
    assert result.get_space(1, 2) == BoardSpaceColors.GRAY
    assert result.get_space(0, 1) == BoardSpaceColors.GRAY

def test_press_white_diagonal_white_not_connected():
    """Spec: orthogonally-linked only; diagonal white tile should not turn grey"""
    b = Board()
    b.set_space(1, 1, BoardSpaceColors.WHITE)
    b.set_space(2, 2, BoardSpaceColors.WHITE)  # diagonal, not orthogonal
    result = press(b, (1, 1))
    assert result.get_space(1, 1) == BoardSpaceColors.GRAY
    assert result.get_space(2, 2) == BoardSpaceColors.WHITE  # unchanged

def test_press_white_adjacent_gray_becomes_white():
    """Spec: grey tiles orthogonally-adjacent to the collapsed white group become white"""
    b = Board()
    b.set_space(1, 1, BoardSpaceColors.WHITE)
    # (1,0), (1,2), (0,1), (2,1) are orthogonal neighbors and are GRAY by default
    result = press(b, (1, 1))
    assert result.get_space(1, 1) == BoardSpaceColors.GRAY   # self turned grey
    assert result.get_space(1, 0) == BoardSpaceColors.WHITE  # adjacent gray → white
    assert result.get_space(1, 2) == BoardSpaceColors.WHITE
    assert result.get_space(0, 1) == BoardSpaceColors.WHITE
    assert result.get_space(2, 1) == BoardSpaceColors.WHITE

def test_press_white_chain_flood_fill():
    """Spec: orthogonally-linked chain of white tiles all collapse"""
    b = Board()
    b.set_space(0, 0, BoardSpaceColors.WHITE)
    b.set_space(1, 0, BoardSpaceColors.WHITE)  # linked to (0,0)
    b.set_space(2, 0, BoardSpaceColors.WHITE)  # linked to (1,0)
    result = press(b, (0, 0))
    assert result.get_space(0, 0) == BoardSpaceColors.GRAY
    assert result.get_space(1, 0) == BoardSpaceColors.GRAY
    assert result.get_space(2, 0) == BoardSpaceColors.GRAY
