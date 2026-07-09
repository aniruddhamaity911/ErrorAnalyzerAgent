from typing import Dict, Any
from graph.chains.generate_answer import generation_chain
from state import GraphState


def answer_generator(state:GraphState)->Dict[str,Any]:
    """The method
    generate the answer based on the errors
    and user questions.
    :param state: The state of the graph
    :returns answer state"""

    print("<======generating answer======>")
    question = state['question']
    errors = state['error_log']
    answer = generation_chain.invoke({"question":question,"document":errors})
    return {"answer":answer}
