from __future__ import annotations

import random
from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class SupportsLessThan(Protocol):
    """Enforces the type has __lt__ implemented."""

    def __lt__(self, __other: Any) -> bool: ...


def weighted_coin_flip(prob: float) -> bool:
    """Flips a weighted coin with probability prob and 1 - prob."""
    return random.choices([True, False], [prob, 1 - prob])[0]
