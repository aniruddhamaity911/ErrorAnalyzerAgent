from langgraph.constants import END
from langgraph.graph import StateGraph

from state import GraphState
from graph import answer_generator, grade_document, retrieve_error_logs, deep_search
from const import DEEP_SEARCH_LOG,ANSWER,RETRIEVE_LOG,GRADE_LOG

"""
define conditional flow
if the error_logs in state is empty
then deep search 
"""
def conditional_flow(state:GraphState)->str:
    """
    route the flow of the graph
    to ANSWER node or DEEP_SEARCH_LOG
    based on the graphState.
    if missing_keys rahState is not empty
    it will direct to DEEP_SEARCH_LOG
    else
    ANSWER
    :param state:
    :return:
    """
    print("<=====Conditional flow=====>")
    missing_keys = state["missing_keys"] or []
    if len(missing_keys) != 0:
        return "DEEP_SEARCH_LOG"
    return "ANSWER"

workFlows = StateGraph(GraphState)
workFlows.add_node(RETRIEVE_LOG,retrieve_error_logs)
workFlows.add_node(ANSWER,answer_generator)
workFlows.add_node(GRADE_LOG,grade_document)
workFlows.add_node(DEEP_SEARCH_LOG,deep_search)
workFlows.set_entry_point(RETRIEVE_LOG)
workFlows.add_edge(RETRIEVE_LOG,GRADE_LOG)
workFlows.add_conditional_edges(GRADE_LOG,conditional_flow,{DEEP_SEARCH_LOG:DEEP_SEARCH_LOG,
                                                              ANSWER:ANSWER})
workFlows.add_edge(DEEP_SEARCH_LOG,GRADE_LOG)
workFlows.add_edge(ANSWER,END)
app = workFlows.compile()
# app.get_graph().draw_mermaid_png(output_file_path="graph.png")
result = app.invoke(input={"question": "what are the major errors in the system"})
print(result["answer"])