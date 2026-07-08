from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from config import llm

SYSTEM = """
You are an expert Site Reliability Engineer (SRE) and production log analyst.

Your task is to determine whether the retrieved logs contain enough information to answer the user's question.

Rules:
1. Read the user's question carefully.
2. Analyze the retrieved logs.
3. Decide whether the logs are sufficient to determine the root cause and provide a meaningful answer.
4. If the logs are sufficient, set score=True.
5. If the logs are NOT sufficient, set score=False and generate a concise web search query that is likely to find the missing information.
6. Do not answer the user's question.
7. Do not explain your reasoning.
8. Return only the structured output.
"""


class DocumentGrade(BaseModel):
    """
    Determines whether the retrieved logs are sufficient.
    """

    score: bool = Field(
        description="True if the retrieved logs are sufficient to answer the user's question."
    )

    web_query: Optional[str] = Field(
        default=None,
        description="A search query to use when score=False. Otherwise null."
    )


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM),
        (
            "human",
            """
User Question:
{question}

Retrieved Logs:
{document}
"""
        ),
    ]
)

llm_structure = llm.with_structured_output(DocumentGrade)

retrieve_grade = prompt | llm_structure
