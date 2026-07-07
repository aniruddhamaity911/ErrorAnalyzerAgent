from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from const import ENVIRONMENT_VARIABLE, EMBEDDING_MODEL,LLM_MODEL

embedder = OpenAIEmbeddings(model=ENVIRONMENT_VARIABLE.get(EMBEDDING_MODEL, "default"))
llm = ChatOpenAI(model=ENVIRONMENT_VARIABLE.get(LLM_MODEL, "gpt-4o-mini"))
