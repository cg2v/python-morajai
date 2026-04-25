from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass

from .board import BoardBase, BoardSpaceColors, CompactBoard
from .inverse import inverse_press


@dataclass(frozen=True)
class Predecessor:
    board: BoardBase
    press_position: tuple[int, int]
    press_color: BoardSpaceColors


def iter_predecessors(
    state: BoardBase,
    *,
    include_noops: bool = False,
    dedupe: bool = True,
    skip_unsupported: bool = True,
) -> Iterator[Predecessor]:
    """
    Yield predecessor states P such that pressing P at press_position can produce `state`.

    Args:
        state: The current board state for which predecessors are requested.
        include_noops: If False, suppress predecessors equal to `state`.
        dedupe: If True, deduplicate equivalent predecessor boards.
        skip_unsupported: If True, ignore actions whose inverse is not implemented.
    """
    seen: set[CompactBoard] = set()

    for x in range(3):
        for y in range(3):
            coord = (x, y)

            try:
                candidates = inverse_press(state, coord)
            except NotImplementedError:
                if skip_unsupported:
                    continue
                raise

            for pred_board in candidates:
                if not include_noops and pred_board == state:
                    continue

                compact = CompactBoard(pred_board)
                if dedupe and compact in seen:
                    continue
                seen.add(compact)

                yield Predecessor(
                    board=compact,
                    press_position=coord,
                    press_color=pred_board.get_space(x, y),
                )


def list_predecessors(
    state: BoardBase,
    *,
    include_noops: bool = False,
    dedupe: bool = True,
    skip_unsupported: bool = True,
) -> Sequence[Predecessor]:
    """Materialized version of iter_predecessors."""
    return list(
        iter_predecessors(
            state,
            include_noops=include_noops,
            dedupe=dedupe,
            skip_unsupported=skip_unsupported,
        )
    )