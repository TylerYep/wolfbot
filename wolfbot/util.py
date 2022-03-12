from __future__ import annotations

import random
from typing import Any, Protocol, TypeVar

# TODO https://github.com/PyCQA/pylint/issues/3401
T = TypeVar("T")  # pylint: disable=invalid-name


class SupportsLessThan(Protocol):
    """Enforces the type has __lt__ implemented."""

    def __lt__(self, __other: Any) -> bool:
        ...


def weighted_coin_flip(prob: float) -> bool:
    """Flips a weighted coin with probability prob and 1 - prob."""
    return random.choices([True, False], [prob, 1 - prob])[0]
