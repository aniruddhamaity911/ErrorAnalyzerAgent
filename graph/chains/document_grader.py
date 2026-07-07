from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from config import llm

SYSTEM = """You are a grader assessing relevance of a retrieved error logs here it is document, to a user question usually about error. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score True or False score to indicate whether the document or error logs are relevant to the question."""

class DocumentGrade(BaseModel):
    """
    The structure of the output
    of document_grader chain.
    if True: the retrieved document/documents are sufficient to answer
    else False.
    """
    score: bool = Field(description="Documents are relevant to the question, True or False")


prompt = ChatPromptTemplate(
    messages=[
        ('system', SYSTEM),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)
llm_structure = llm.with_structured_output(DocumentGrade)
retrieve_grade = prompt | llm_structure
