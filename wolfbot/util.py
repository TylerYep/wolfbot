from __future__ import annotations

import random
from collections import Counter
from collections.abc import Sequence
from typing import TypeVar

# TODO https://github.com/PyCQA/pylint/issues/3401
T = TypeVar("T")  # pylint: disable=invalid-name


def get_counts(arr: Sequence[T], use_counter_threshold: int = 40) -> dict[T, int]:
    """
    Returns a dict of counts of each item in a list.
    When there are fewer than ~40 items, using a regular
    dictionary is faster than using a Counter.
    """
    if len(arr) < use_counter_threshold:
        counts: dict[T, int] = {}
        for item in arr:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        return counts

    return dict(Counter(arr))


def weighted_coin_flip(prob: float) -> bool:
    """Flips a weighted coin with probability prob and 1 - prob."""
    return random.choices([True, False], [prob, 1 - prob])[0]
