from typing import Any, Dict

from langchain_core.documents import Document

from graph.chains import document_grader
from state import GraphState


def grade_document(state:GraphState)->Dict[str,Any]:
    """
    The method to grade the error logs.
    If the logs are sufficient to answer the user query
    then present state is perfect else
    the method will set web_query to the state
    :param state:  of the present graph
    :return: dictionary
    """
    question = state["question"]
    documents = state["error_log"]
    final_documents = []
    print("<=====grading the error log=====>")
    for doc in documents:
        content = doc.page_content
        score = document_grader.retrieve_grade.invoke({"question": question, "document": content})
        if score.score:
            final_documents.append(doc)
    if len(final_documents) == 0:
        final_documents.append(Document(page_content="There is no valid log present.Do not analyze further.reply user that no error found"
                                                     "please check the question or provide sufficient more details"))
    print("<=====grading the error log completed=====>")
    return {"error_log": final_documents}