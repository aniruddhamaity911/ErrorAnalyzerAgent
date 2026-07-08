from typing import TypedDict

from langchain_core.documents import Document


class GraphState(TypedDict):
    """
    The state of lang graph
    Stores
    question,
    iteration_count,
    error_log
    web_documents
    answer
    """
    question: str
    iteration_count: int
    error_log: list[Document]
    web_documents: list[Document]
    answer: str
