from config import TOP_K

# function to retrieve relevant documents from the vectorstore based on the user's question
def retrieve_docs(vectorstore, question: str):
    return vectorstore.similarity_search(question, k=TOP_K)

# Function to build a context string from the retrieved documents
def build_context(retrieved_docs):
    context_parts = []

    for doc in retrieved_docs:
        source_file = doc.metadata.get("source_file", "Unknown file")
        page = doc.metadata.get("page", "Unknown page")

        context_parts.append(
            f"File: {source_file}\nPage: {page}\nContent: {doc.page_content}"
        )

    return "\n\n".join(context_parts)