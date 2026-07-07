from datetime import datetime, timezone

from langchain_mongodb import MongoDBAtlasVectorSearch

from config import get_required_env
from pymongo import MongoClient
from const import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION, EMBEDDING_MODEL, VECTOR_SEARCH_INDEX
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

environment_var = get_required_env()


class VectorStore:
    """
    The class is for storing the error in vector db.
    """

    def __init__(self):
        """
        required environment variables
        MONGODB_URI,
        MONGODB_DB,
        MONGODB_COLLECTION,
        EMBEDDING_MODEL,

        """
        client = MongoClient(environment_var[MONGODB_URI])
        db = client[environment_var[MONGODB_DB]]
        collection = db[environment_var[MONGODB_COLLECTION]]
        embedding_model = OpenAIEmbeddings(model=environment_var.get(EMBEDDING_MODEL, "default"))
        self.vector_store = MongoDBAtlasVectorSearch(collection=collection,
                                                     embedding=embedding_model,
                                                     index_name=environment_var[VECTOR_SEARCH_INDEX], )

    def save_errors(self, error_logs):
        """
        Store the list of error logs into mongodb vector database
        :param error_logs: list of Error objects
        :return:
        """
        documents = []

        for error in error_logs:
            text = f"""
                    Timestamp:
                    {error.timestamp}
                    
                    Level:
                    {error.level}
                    
                    Message:
                    {error.message}
                    
                    Complete Error:
                    {error.raw_error}
                """

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "timestamp": error.timestamp,
                        "level": error.level,
                        "message": error.message,
                        "createdAt": datetime.now(timezone.utc),
                    },
                )
            )

        self.vector_store.add_documents(documents)

        print(f"Inserted {len(documents)} error documents.")
    def search(self, query: str, k: int = 3) -> list[Document]:
        return self.vector_store.similarity_search(
            query=query,
            k=k
        )



