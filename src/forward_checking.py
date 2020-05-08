from typing import List, Dict

import random

from src.algorithms import SolverState

def recurse_assign_forward_checking(
    solution: SolverState,
    all_role_guesses: List[str],
    curr_role_counts: Dict[str, int],
    restrict_possible: bool = True,
) -> List[str]:
    """
    Assign the remaining unknown cards by recursing and finding a consistent placement.
    If restrict_possible is enabled, then uses the possible_roles sets to assign.
    Else simply fills in slots with curr_role_counts.
    """

    def _recurse_assign(
        remaining_indices: Dict[int, List],
        queue: List[int],
        curr_role_counts: Dict[str, int],
        restrict_possible: bool = True
    ) -> List[str]:
        if all(assigned for assigned, _ in remaining_indices.values()):
            return remaining_indices

        # Forward Checking Pass
        while queue:
            ind = queue.pop()
            _, possible = remaining_indices[ind]
            leftover_roles = sorted(
                possible
                if restrict_possible
                else [k for k, v in curr_role_counts.items() if v > 0]
            )
            random.shuffle(leftover_roles)
            for rol in leftover_roles:
                if curr_role_counts[rol] > 0:
                    curr_role_counts[rol] -= 1
                    remaining_indices[ind][0] = rol

                    if curr_role_counts[rol] == 0:
                        for j in reversed(queue):
                            neighbor_value, neighbor_possible = remaining_indices[j]
                            if not neighbor_value:
                                neighbor_possible.discard(rol)
                                if not neighbor_possible:
                                    return []
                    result = _recurse_assign(
                        remaining_indices, queue, curr_role_counts, restrict_possible
                    )
                    if result:
                        return result
                    curr_role_counts[rol] += 1
                    remaining_indices[ind][0] = ""

        # Unable to assign all roles
        return []

    empty_indices = {
        i: ["", set(solution.possible_roles[i])]
        for i in range(const.NUM_ROLES)
        if all_role_guesses[i] == ""
    }
    if not empty_indices:
        return all_role_guesses
    queue = sorted(empty_indices.keys(), key=lambda x: len(empty_indices[x][1]), reverse=True)
    solved = _recurse_assign(empty_indices, queue, dict(curr_role_counts), restrict_possible)

    if not solved:
        return []
    for i in solved:
        value, _ = empty_indices[i]
        all_role_guesses[i] = value
    return all_role_guesses
