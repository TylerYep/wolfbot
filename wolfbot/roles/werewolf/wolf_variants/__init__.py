from wolfbot.roles.werewolf.wolf_variants.center_wolf import get_center_wolf_statements
from wolfbot.roles.werewolf.wolf_variants.expectimax_wolf import (
    get_statement_expectimax,
)
from wolfbot.roles.werewolf.wolf_variants.random_wolf import get_wolf_statements_random
from wolfbot.roles.werewolf.wolf_variants.reg_wolf import get_wolf_statements
from wolfbot.roles.werewolf.wolf_variants.rl_wolf import get_statement_rl

__all__ = (
    "get_center_wolf_statements",
    "get_statement_expectimax",
    "get_wolf_statements_random",
    "get_wolf_statements",
    "get_statement_rl",
)
