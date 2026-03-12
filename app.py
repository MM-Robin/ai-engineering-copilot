from config import DATA_FOLDER

from src.loader import get_pdf_files, load_all_pdfs
from src.splitter import split_documents
from src.embeddings import get_embeddings
from src.vectordb import (
    create_and_save_vectorstore,
    load_existing_vectorstore,
    vectorstore_exists,
)
from src.retriever import retrieve_docs, build_context
from src.llm import get_llm, answer_question
from src.router import detect_query_type
from src.summarizer import summarize_each_file


def build_system():
    pdf_files = get_pdf_files(DATA_FOLDER)
    documents = load_all_pdfs(pdf_files)
    embeddings = get_embeddings()

    if vectorstore_exists():
        print("Loading existing vector store...")
        vectorstore = load_existing_vectorstore(embeddings)
    else:
        print("Creating new vector store...")
        chunks = split_documents(documents)
        vectorstore = create_and_save_vectorstore(chunks, embeddings)

    return pdf_files, documents, vectorstore


def print_sources(retrieved_docs):
    print("\nSources:")
    print("-" * 60)

    for i, doc in enumerate(retrieved_docs, start=1):
        source_file = doc.metadata.get("source_file", "Unknown file")
        page = doc.metadata.get("page", "Unknown page")
        preview = doc.page_content[:200].replace("\n", " ")

        print(f"{i}. File: {source_file} | Page: {page}")
        print(f"   Preview: {preview}")
        print("-" * 60)


def main():
    print("Starting AI Engineering Copilot...\n")

    pdf_files, documents, vectorstore = build_system()
    llm = get_llm()

    print("\nLoaded files:")
    for i, pdf in enumerate(pdf_files, start=1):
        print(f"{i}. {pdf.name}")

    print("\nSystem ready.")
    print("=" * 60)

    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()

        if question.lower() == "exit":
            print("Goodbye.")
            break

        if not question:
            continue

        query_type = detect_query_type(question)

        if query_type == "list_files":
            print("\nLoaded files:")
            for i, pdf in enumerate(pdf_files, start=1):
                print(f"{i}. {pdf.name}")
            continue

        if query_type == "summarize_all":
            summaries = summarize_each_file(llm, documents)

            print("\nFile Summaries:")
            print("=" * 60)

            for filename, summary in summaries.items():
                print(f"\n{filename}")
                print("-" * 60)
                print(summary)

            continue

        retrieved_docs = retrieve_docs(vectorstore, question)
        context = build_context(retrieved_docs)
        answer = answer_question(llm, context, question)

        print("\nAnswer:")
        print("=" * 60)
        print(answer)

        print_sources(retrieved_docs)


if __name__ == "__main__":
    main()