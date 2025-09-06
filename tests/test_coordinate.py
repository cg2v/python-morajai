import math
from collections.abc import Sequence
from morajai.board import get_clockwise_coordinate

def is_clockwise_around(center: tuple[int, int], coords: Sequence[tuple[int, int]]) -> bool:
    """Return True if coords move clockwise around center (non-enumerating, uses angles)."""
    def angle(p):
        return math.atan2(p[1] - center[1], p[0] - center[0])
    angles = [angle(p) for p in coords]
    # Compute signed differences between consecutive angles, wrapping to [-pi, pi]
    def signed_diff(a1, a2):
        diff = a2 - a1
        while diff <= -math.pi:
            diff += 2 * math.pi
        while diff > math.pi:
            diff -= 2 * math.pi
        return diff
    diffs = [signed_diff(angles[i], angles[(i+1)]) for i in range(len(angles)-1)]
    total = sum(diffs)
    # Clockwise if total is negative (full loop ~ -2*pi)
    return total < 0

def test_is_clockwise_around():
    center = (1, 1)
    # Clockwise order around center
    coords_cw = [(1,2), (2,2), (2,1), (2,0), (1,0), (0,0), (0,1), (0,2)]
    # Counterclockwise order
    coords_ccw = list(reversed(coords_cw))
    assert is_clockwise_around(center, coords_cw)
    assert not is_clockwise_around(center, coords_ccw)
def pythagorean_distance(coord1: tuple[int, int], coord2: tuple[int, int]) -> int:
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

def test_clockwise_sanity():
    """makes sure the pythagorean distance of the clockwise adjacent coordinates is less than 2"""
    for coord in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
        adjacent_coords = get_clockwise_coordinate(coord)
        for adj_coord in adjacent_coords:
            assert 0 < pythagorean_distance(coord, adj_coord) < 2, f"Failed on {coord} -> {adj_coord}"


def test_clockwise_coordinates():
    for coord in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
        adjacent_coords = get_clockwise_coordinate(coord)
        assert is_clockwise_around(coord, adjacent_coords)