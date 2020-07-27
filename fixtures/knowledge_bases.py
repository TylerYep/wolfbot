""" knowledge_bases.py """
# pylint: disable=missing-function-docstring
from typing import List

import pytest

from src.statements import KnowledgeBase, Statement


@pytest.fixture
def small_knowledge_base(small_statement_list: List[Statement]) -> KnowledgeBase:
    return KnowledgeBase.from_statement_list(small_statement_list)


@pytest.fixture
def medium_knowledge_base(medium_statement_list: List[Statement]) -> KnowledgeBase:
    return KnowledgeBase.from_statement_list(medium_statement_list)


@pytest.fixture
def large_knowledge_base(large_statement_list: List[Statement]) -> KnowledgeBase:
    return KnowledgeBase.from_statement_list(large_statement_list)


# @pytest.fixture
# def small_knowledge_base(
#     small_game_roles, small_statement_list: List[Statement]
# ) -> KnowledgeBase:
#     return KnowledgeBase.from_statement_list(small_statement_list)


# @pytest.fixture
# def medium_knowledge_base(
#     medium_game_roles, medium_statement_list: List[Statement]
# ) -> KnowledgeBase:
#     return KnowledgeBase.from_statement_list(medium_statement_list)


# @pytest.fixture
# def large_knowledge_base(
#     large_game_roles, large_statement_list: List[Statement]
# ) -> KnowledgeBase:
#     return KnowledgeBase.from_statement_list(large_statement_list)
