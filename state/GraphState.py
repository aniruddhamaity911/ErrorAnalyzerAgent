from typing import TypedDict

from langchain_core.documents import Document


class GraphState(TypedDict):
    """
    The state of lang graph
    Stores
    question,
    iteration_count,
    error_log
    missing_keys
    answer
    """
    question: str
    iteration_count: int
    error_log: list[Document]
    missing_keys: list[str]
    answer: str
