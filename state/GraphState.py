from typing import TypedDict

from langchain_core.documents import Document


class GraphState(TypedDict):
    """
    The state of lang graph
    Stores
    question,
    iteration_count,
    documents
    answer
    """
    question: str
    iteration_count: int
    documents: list[Document]
    answer: str
