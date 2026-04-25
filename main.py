from morajai.board import BoardSpaceColors, Board
from morajai.astarsupport import GameNode, GameSearch

def trading_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.PINK)
    board.set_space(1, 0, BoardSpaceColors.YELLOW)
    board.set_space(2, 0, BoardSpaceColors.YELLOW)
    board.set_space(1, 1, BoardSpaceColors.YELLOW)
    board.set_space(2, 1, BoardSpaceColors.YELLOW)
    assert repr(board) == "P E E\nE Y Y\nE Y Y"
    return board

def tunnel_board() -> Board:
    board = Board()
    board.set_space(0, 0, BoardSpaceColors.PINK)
    board.set_space(0, 1, BoardSpaceColors.ORANGE)
    board.set_space(0, 2, BoardSpaceColors.BLACK)
    board.set_space(1, 0, BoardSpaceColors.ORANGE)
    board.set_space(1, 1, BoardSpaceColors.ORANGE)
    board.set_space(1, 2, BoardSpaceColors.ORANGE)
    board.set_space(2, 0, BoardSpaceColors.ORANGE)
    board.set_space(2, 1, BoardSpaceColors.ORANGE)
    board.set_space(2, 2, BoardSpaceColors.PINK)
    assert repr(board) == "K O P\nO O O\nP O O"
    return board

def solarium_board() -> Board:
    board = Board()
    board.set_space(0, 0, BoardSpaceColors.YELLOW)
    board.set_space(0, 1, BoardSpaceColors.GREEN)
    board.set_space(0, 2, BoardSpaceColors.GREEN)
    board.set_space(1, 0, BoardSpaceColors.GRAY)
    board.set_space(1, 1, BoardSpaceColors.YELLOW)
    board.set_space(1, 2, BoardSpaceColors.GRAY)
    board.set_space(2, 0, BoardSpaceColors.GREEN)
    board.set_space(2, 1, BoardSpaceColors.GREEN)
    board.set_space(2, 2, BoardSpaceColors.YELLOW)
    assert repr(board) == "G E Y\nG Y G\nY E G"
    return board

def master_bedroom_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.WHITE)
    board.set_space(2, 2, BoardSpaceColors.WHITE)
    board.set_space(0, 1, BoardSpaceColors.WHITE)
    board.set_space(2, 0, BoardSpaceColors.WHITE)
    assert repr(board) == "W E W\nW E E\nE E W"
    return board

def closed_exhibit_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.ORANGE)
    board.set_space(1, 2, BoardSpaceColors.BLACK)
    board.set_space(2, 2, BoardSpaceColors.ORANGE)
    board.set_space(0, 1, BoardSpaceColors.ORANGE)
    board.set_space(1, 1, BoardSpaceColors.RED)
    board.set_space(2, 1, BoardSpaceColors.ORANGE)
    board.set_space(0, 0, BoardSpaceColors.ORANGE)
    board.set_space(1, 0, BoardSpaceColors.BLACK)
    board.set_space(2, 0, BoardSpaceColors.ORANGE)
    assert repr(board) == "O K O\nO R O\nO K O"
    return board

def throne_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.BLACK)
    board.set_space(1, 2, BoardSpaceColors.GREEN)
    board.set_space(2, 2, BoardSpaceColors.BLUE)
    board.set_space(0, 1, BoardSpaceColors.BLUE)
    board.set_space(1, 1, BoardSpaceColors.BLUE)
    board.set_space(2, 1, BoardSpaceColors.BLUE)
    board.set_space(0, 0, BoardSpaceColors.VIOLET)
    assert repr(board) == "K G B\nB B B\nV E E"
    return board

def lost_and_found_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.PINK)
    board.set_space(1, 2, BoardSpaceColors.PINK)
    board.set_space(2, 2, BoardSpaceColors.PINK)
    board.set_space(0, 1, BoardSpaceColors.PINK)
    board.set_space(2, 1, BoardSpaceColors.PINK)
    assert repr(board) == "P P P\nP E P\nE E E"
    return board

def tomb_board() -> Board:
    board = Board()
    board.set_space(1, 2, BoardSpaceColors.VIOLET)
    board.set_space(1, 1, BoardSpaceColors.PINK)
    board.set_space(0, 0, BoardSpaceColors.VIOLET)
    board.set_space(1, 0, BoardSpaceColors.VIOLET)
    board.set_space(2, 0, BoardSpaceColors.VIOLET)
    assert repr(board) == "E V E\nE P E\nV V V"
    return board

def sanctum_orinda_aries_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.GREEN)
    board.set_space(1, 2, BoardSpaceColors.BLACK)
    board.set_space(2, 2, BoardSpaceColors.GREEN)
    board.set_space(0, 1, BoardSpaceColors.BLACK)
    board.set_space(1, 1, BoardSpaceColors.BLACK)
    board.set_space(2, 1, BoardSpaceColors.BLACK)
    board.set_space(0, 0, BoardSpaceColors.GREEN)
    board.set_space(1, 0, BoardSpaceColors.YELLOW)
    board.set_space(2, 0, BoardSpaceColors.GREEN)
    assert repr(board) == "G K G\nK K K\nG Y G"
    return board

def sanctum_fenn_aries_board() -> Board:
    board = Board()
    board.set_space(1, 2, BoardSpaceColors.GREEN)
    board.set_space(0, 1, BoardSpaceColors.ORANGE)
    board.set_space(1, 1, BoardSpaceColors.RED)
    board.set_space(2, 1, BoardSpaceColors.ORANGE)
    board.set_space(0, 0, BoardSpaceColors.WHITE)
    board.set_space(1, 0, BoardSpaceColors.GREEN)
    board.set_space(2, 0, BoardSpaceColors.BLACK)
    assert repr(board) == "E G E\nO R O\nW G K"
    return board

def sanctum_arch_aries_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.BLACK)
    board.set_space(1, 2, BoardSpaceColors.YELLOW)
    board.set_space(0, 1, BoardSpaceColors.YELLOW)
    board.set_space(1, 1, BoardSpaceColors.GREEN)
    board.set_space(2, 1, BoardSpaceColors.YELLOW)
    board.set_space(1, 0, BoardSpaceColors.YELLOW)
    board.set_space(2, 0, BoardSpaceColors.BLACK)
    assert repr(board) == "K Y E\nY G Y\nE Y K"
    return board

def sanctum_eraja_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.YELLOW)
    board.set_space(1, 2, BoardSpaceColors.VIOLET)
    board.set_space(2, 2, BoardSpaceColors.YELLOW)
    board.set_space(0, 1, BoardSpaceColors.GREEN)
    board.set_space(1, 1, BoardSpaceColors.RED)
    board.set_space(2, 1, BoardSpaceColors.BLACK)
    board.set_space(0, 0, BoardSpaceColors.VIOLET)
    board.set_space(1, 0, BoardSpaceColors.VIOLET)
    board.set_space(2, 0, BoardSpaceColors.VIOLET)
    assert repr(board) == "Y V Y\nG R K\nV V V"
    return board

def sanctum_corarica_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.ORANGE)
    board.set_space(1, 2, BoardSpaceColors.BLACK)
    board.set_space(2, 2, BoardSpaceColors.ORANGE)
    board.set_space(0, 1, BoardSpaceColors.ORANGE)
    board.set_space(1, 1, BoardSpaceColors.ORANGE)
    board.set_space(2, 1, BoardSpaceColors.ORANGE)
    board.set_space(0, 0, BoardSpaceColors.VIOLET)
    board.set_space(1, 0, BoardSpaceColors.GREEN)
    board.set_space(2, 0, BoardSpaceColors.VIOLET)
    assert repr(board) == "O K O\nO O O\nV G V"
    return board

def sanctum_mora_jai_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.YELLOW)
    board.set_space(1, 2, BoardSpaceColors.YELLOW)
    board.set_space(2, 2, BoardSpaceColors.YELLOW)
    board.set_space(0, 1, BoardSpaceColors.WHITE)
    board.set_space(1, 1, BoardSpaceColors.PINK)
    board.set_space(2, 1, BoardSpaceColors.WHITE)
    assert repr(board) == "Y Y Y\nW P W\nE E E"
    return board

def sanctum_verra_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.PINK)
    board.set_space(1, 2, BoardSpaceColors.PINK)
    board.set_space(0, 0, BoardSpaceColors.ORANGE)
    board.set_space(1, 0, BoardSpaceColors.ORANGE)
    board.set_space(2, 0, BoardSpaceColors.ORANGE)
    assert repr(board) == "P P E\nE E E\nO O O"
    return board

def sanctum_nuance_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.GREEN)
    board.set_space(2, 2, BoardSpaceColors.GREEN)
    board.set_space(1, 1, BoardSpaceColors.ORANGE)
    board.set_space(2, 1, BoardSpaceColors.ORANGE)
    board.set_space(1, 0, BoardSpaceColors.BLACK)
    board.set_space(2, 0, BoardSpaceColors.VIOLET)
    assert repr(board) == "G E G\nE O O\nE K V"
    return board

def generate_goal(color: BoardSpaceColors) -> Board:
    board = Board()
    board.set_space(0, 0, color)
    board.set_space(0, 2, color)
    board.set_space(2, 0, color)
    board.set_space(2, 2, color)
    return board

def main():
    initial_board = solarium_board()
    goal_board = generate_goal(BoardSpaceColors.GREEN)

    print("Initial Board:")
    print(initial_board)
    print("\nGoal Board:")
    print(goal_board)

    start_node = GameNode(initial_board)
    goal_node = GameNode(goal_board, corner_color=BoardSpaceColors.GREEN)

    search = GameSearch()
    path = search.astar(start_node, goal_node)

    if path:
        print("\nSolution found:")
        for step, node in enumerate(path):
            print(f"\nStep {step}:")
            if node.press_position and node.press_color:
                print(f"Press at {node.press_position} ({3 * node.press_position[1] + node.press_position[0] + 1}) with color {node.press_color.name}")
            print(node.board)
    else:
        print("\nNo solution found.")

if __name__ == "__main__":
    main()
