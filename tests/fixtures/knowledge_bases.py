""" knowledge_bases.py """
import pytest

from wolfbot.statements import KnowledgeBase, Statement


@pytest.fixture
def small_knowledge_base(small_statement_list: tuple[Statement, ...]) -> KnowledgeBase:
    return KnowledgeBase.from_statement_list(small_statement_list)


@pytest.fixture
def medium_knowledge_base(
    medium_statement_list: tuple[Statement, ...]
) -> KnowledgeBase:
    return KnowledgeBase.from_statement_list(medium_statement_list)


@pytest.fixture
def large_knowledge_base(large_statement_list: tuple[Statement, ...]) -> KnowledgeBase:
    return KnowledgeBase.from_statement_list(large_statement_list)
