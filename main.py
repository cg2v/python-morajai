from morajai.board import BoardSpaceColors, Board
from morajai.astarsupport import GameNode, GameSearch

def trading_board() -> Board:
    board = Board()
    board.set_space(0, 2, BoardSpaceColors.PINK)
    board.set_space(1, 0, BoardSpaceColors.YELLOW)
    board.set_space(2, 0, BoardSpaceColors.YELLOW)
    board.set_space(1, 1, BoardSpaceColors.YELLOW)
    board.set_space(2, 1, BoardSpaceColors.YELLOW)
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
    return board

def generate_goal(color: BoardSpaceColors) -> Board:
    board = Board()
    board.set_space(0, 0, color)
    board.set_space(0, 2, color)
    board.set_space(2, 0, color)
    board.set_space(2, 2, color)
    return board

def main():
    initial_board = tunnel_board()
    goal_board = generate_goal(BoardSpaceColors.ORANGE)

    print("Initial Board:")
    print(initial_board)
    print("\nGoal Board:")
    print(goal_board)

    start_node = GameNode(initial_board)
    goal_node = GameNode(goal_board, corner_color=BoardSpaceColors.ORANGE)

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
