from collections.abc import Sequence
from dataclasses import dataclass
from astar import AStar

from .board import BoardBase, BoardSpaceColors, CompactBoard, CoordinateError
from .press import press

@dataclass
class GameNode:
    board: BoardBase
    corner_color: BoardSpaceColors|None = None
    press_position: tuple[int, int]|None = None
    press_color: BoardSpaceColors|None = None
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameNode):
            return False
        return self.board == other.board

    def __hash__(self) -> int:
        return hash(self.board)
    def is_goal_reached(self, target_color: BoardSpaceColors|None = None) -> bool:
        target_color = target_color if self.corner_color is None else self.corner_color
        if target_color is None:
            return False
        for x in (0, 2):
            for y in (0, 2):
                if self.board.get_space(x, y) != target_color:
                    return False
        return True
class GameSearch(AStar):
    def is_goal_reached(self, current: GameNode, goal: GameNode) -> bool:
        return current.is_goal_reached(goal.corner_color)
    def neighbors(self, node: object) -> Sequence[GameNode]:
        if not isinstance(node, GameNode):
            return []
        neighbors : Sequence[GameNode] = []
        for x in range(3):
            for y in range(3):
                # Simulate a press at (x, y)
                new_board = press(node.board, (x, y))
                if new_board != node.board:
                    neighbors.append(GameNode(CompactBoard(new_board), press_position=(x, y), press_color=node.board.get_space(x, y)))
        return neighbors

    def heuristic_cost_estimate(self, current: GameNode, goal: GameNode) -> float:
        cost = 0
        for x in (0, 2):
            for y in (0, 2):
                current_space = current.board.get_space(x, y)
                goal_space = goal.board.get_space(x, y)
                if current_space != goal_space:
                    match (current_space, goal_space):
                        case (BoardSpaceColors.RED, BoardSpaceColors.BLACK):
                            cost += 1
                        case (BoardSpaceColors.BLACK, BoardSpaceColors.RED):
                            cost += 1
                        case _, (BoardSpaceColors.YELLOW|BoardSpaceColors.VIOLET):
                            delta = 1 if goal_space == BoardSpaceColors.YELLOW else -1
                            try :
                                check_space = current.board.get_space(x, y + delta)
                                if check_space == goal_space:
                                    cost += 1
                                else:
                                    cost += 5
                            except CoordinateError:
                                cost += 5
                        case _, BoardSpaceColors.GREEN:
                            try :
                                check_space = current.board.get_space(2 - x, 2 - y)
                                if check_space == BoardSpaceColors.GREEN:
                                    cost += 1
                            except CoordinateError:
                                cost += 5
                        case BoardSpaceColors.GRAY, BoardSpaceColors.WHITE:
                            surrounding = current.board.get_surrounding_spaces((x, y))
                            for space in surrounding:
                                if space == BoardSpaceColors.WHITE:
                                    cost += 1
                                    break
                            else:
                                cost += 5
                        case BoardSpaceColors.WHITE, BoardSpaceColors.GRAY:
                            surrounding = current.board.get_surrounding_spaces((x, y))
                            for space in surrounding:
                                if space == BoardSpaceColors.GRAY:
                                    cost += 5
                                    break
                            else:
                                cost += 1
                        case _:
                            cost += 3
        return cost

    def distance_between(self, n1: GameNode, n2: GameNode) -> float:
        return 1  # Each move has a uniform cost
