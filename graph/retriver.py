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
        k=5
    )
    print("<======== Retrieval completed ========>")
    return {"documents": documents}




if __name__ == "__main__":
    state = {"question":"Payment already processed "}
    docs  =retrieve_error_logs(state)

    print("completed")
