from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

from config import llm

SYSTEM = """
You are an expert Site Reliability Engineer (SRE) and production log analyst.

Your task is to determine whether the retrieved logs contain enough
information to answer the user's question.

Rules:

1. Read the user's question carefully.
2. Read the retrieved logs.
3. Determine whether the logs contain enough information to answer the user's question.
4. If yes, return:
   - score=True
   - missing_keyWords=[]

5. If no, return:
   - score=False
   - Extract only the important identifiers, entities or search terms that are present in the user's question but are missing from the retrieved logs.
   - These keywords will be used for another database search.
   - these keywords should be word must not a sentence

6. Good keywords include:
   - UNIQUE numbers
   - UNIQUE entities
   - UNIQUE search terms
   - Correlation IDs
   - User IDs
   - Order IDs
   - Barcode IDs
   - File names
   - Service names
   - Error messages
   - Exception names
   - SQL table names
   - API names

7. Do NOT invent new keywords.
8. Do NOT explain your reasoning.
9. Return only the structured output.
"""


class DocumentGrade(BaseModel):
    score: bool = Field(
        description="True if the retrieved logs are sufficient to answer the user's question."
    )

    missing_keyWords: List[str] = Field(
        default_factory=list,
        description=(
            "Important identifiers or search keywords that appear in the user's "
            "question but are absent from the retrieved logs. "
            "Used for the next retrieval attempt."
        )
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
