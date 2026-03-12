import os
from langchain_community.vectorstores import FAISS
from config import VECTORSTORE_PATH

# Functions to create, save, and load the FAISS vectorstore
def create_and_save_vectorstore(chunks, embeddings):
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_PATH)
    return vectorstore


def load_existing_vectorstore(embeddings):
    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def vectorstore_exists():
    return os.path.exists(VECTORSTORE_PATH)