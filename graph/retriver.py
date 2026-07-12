from typing import Dict, Any
from services import VectorStore
from state import GraphState

vector_store = VectorStore()
def retrieve_error_logs(state:GraphState)->Dict[str,Any]:
    """
    from the document database i.e. mongodb
    retrieve relevant error logs
    :param state: GraphState
    :return: dictionary
    """
    question = state["question"]
    print("<======== Retrieving error logs ========>")
    documents = vector_store.search(
        query=question,
        k=5,
    )
    print("<======== Retrieval completed ========>")
    return {"error_log": documents}


def deep_search(state:GraphState)->Dict[str,Any]:
    """
    from error DB
    retrieve the error logs
    which contain the keyword
    in graph state's missing_keywords
    :param state:
    :return:
    """
    keywords = state["missing_keys"]
    documents = vector_store.deep_search(keywords)
    return {"error_log": documents}


if __name__ == "__main__":
    state = {"question":"REQ-9009802"}
    docs  =retrieve_error_logs(state,)
    for doc in docs:
        print(doc)
    print("completed")
