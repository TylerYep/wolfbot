from wolfbot.predictions.engine import (
    get_basic_guesses,
    get_switch_dict,
    recurse_assign,
)
from wolfbot.predictions.evil import (
    make_evil_prediction,
    make_random_prediction,
    make_unrestricted_prediction,
)
from wolfbot.predictions.normal import make_prediction
from wolfbot.predictions.relaxed import make_relaxed_prediction

__all__ = (
    "get_basic_guesses",
    "get_switch_dict",
    "make_evil_prediction",
    "make_prediction",
    "make_random_prediction",
    "make_relaxed_prediction",
    "make_unrestricted_prediction",
    "recurse_assign",
)
