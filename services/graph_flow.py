from langgraph.constants import END
from langgraph.graph import StateGraph

from state import GraphState
from graph import answer_generator, grade_document, retrieve_error_logs

workFlows = StateGraph(GraphState)
workFlows.add_node("RETRIEVE",retrieve_error_logs)
workFlows.add_node("ANSWER",answer_generator)
workFlows.add_node("GRADE",grade_document)
workFlows.set_entry_point("RETRIEVE")
workFlows.add_edge("RETRIEVE","GRADE")
workFlows.add_edge("GRADE","ANSWER")
workFlows.add_edge("ANSWER",END)
app = workFlows.compile()
# app.get_graph().draw_mermaid_png(output_file_path="graph.png")
print(app.invoke(input={"question": ""}))