import streamlit as st
from pathlib import Path
import sys
import tempfile

from langchain_community.document_loaders import PyPDFLoader

# Make project root importable
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.splitter import split_documents
from src.embeddings import get_embeddings
from src.vectordb import create_and_save_vectorstore
from src.retriever import retrieve_docs, build_context
from src.llm import get_llm, stream_answer
from src.router import detect_query_type
from src.summarizer import summarize_each_file


st.set_page_config(
    page_title="AI Engineering Copilot",
    page_icon="🤖",
    layout="wide"
)


def load_uploaded_pdfs(uploaded_files):
    documents = []

    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        loader = PyPDFLoader(tmp_path)
        docs = loader.load()

        for doc in docs:
            doc.metadata["source_file"] = uploaded_file.name

        documents.extend(docs)

    return documents


def format_sources(retrieved_docs):
    formatted = []

    for i, doc in enumerate(retrieved_docs, start=1):
        source_file = doc.metadata.get("source_file", "Unknown file")
        page = doc.metadata.get("page", "Unknown page")
        preview = doc.page_content[:300].replace("\n", " ")

        formatted.append(
            {
                "index": i,
                "file": source_file,
                "page": page,
                "preview": preview,
            }
        )

    return formatted


def format_file_list(files):
    return "\n".join(
        [f"{i}. {file.name}" for i, file in enumerate(files, start=1)]
    )


def format_summaries_as_markdown(summaries):
    parts = []

    for filename, summary in summaries.items():
        parts.append(f"### {filename}\n{summary}")

    return "\n\n".join(parts)


@st.cache_resource(show_spinner=False)
def build_uploaded_system(file_names, file_bytes_list):
    uploaded_files_data = []

    for name, file_bytes in zip(file_names, file_bytes_list):
        uploaded_files_data.append(
            {
                "name": name,
                "bytes": file_bytes,
            }
        )

    documents = []

    for file_data in uploaded_files_data:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file_data["bytes"])
            tmp_path = tmp_file.name

        loader = PyPDFLoader(tmp_path)
        docs = loader.load()

        for doc in docs:
            doc.metadata["source_file"] = file_data["name"]

        documents.extend(docs)

    embeddings = get_embeddings()
    chunks = split_documents(documents)
    vectorstore = create_and_save_vectorstore(chunks, embeddings)
    llm = get_llm()

    return documents, vectorstore, llm


# ----------------------------
# Page header
# ----------------------------
st.title("🤖 AI Engineering Copilot")
st.caption("Upload PDFs and chat with your technical documents.")

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type="pdf",
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("Please upload one or more PDF files to start.")
    st.stop()

st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")
st.markdown("---")


# ----------------------------
# Session state
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

current_files = [file.name for file in uploaded_files]

if "last_uploaded_files" not in st.session_state:
    st.session_state.last_uploaded_files = current_files

if st.session_state.last_uploaded_files != current_files:
    st.session_state.chat_history = []
    st.session_state.last_uploaded_files = current_files


# ----------------------------
# Build system from uploaded files
# ----------------------------
try:
    file_names = [file.name for file in uploaded_files]
    file_bytes_list = [file.getvalue() for file in uploaded_files]

    with st.spinner("Processing uploaded documents..."):
        documents, vectorstore, llm = build_uploaded_system(file_names, file_bytes_list)

except Exception as e:
    st.error(f"System startup failed: {e}")
    st.stop()


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("Uploaded Files")
    for file in uploaded_files:
        st.write(file.name)

    st.divider()
    st.subheader("Example Commands")
    st.write("- list files")
    st.write("- summarize files")
    st.write("- Explain a concept from the documents...")

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()


# Show conversation
for item in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(item["question"])

    with st.chat_message("assistant"):
        if item["answer_type"] in ["list_files", "summarize_all"]:
            st.markdown(item["answer"])
        else:
            st.write(item["answer"])

        if item["sources"]:
            st.markdown("**Sources:**")
            for source in item["sources"]:
                with st.expander(
                    f"{source['file']} | Page {source['page']}",
                    expanded=False
                ):
                    st.write(source["preview"])



# Chat input
query = st.chat_input("Ask a question about your documents...")

if query:
    query_type = detect_query_type(query)

    answer = ""
    sources = []

    if query_type == "list_files":
        answer = format_file_list(uploaded_files)

    elif query_type == "summarize_all":
        with st.spinner("Generating summaries..."):
            summaries = summarize_each_file(llm, documents)
        answer = format_summaries_as_markdown(summaries)

    else:
        with st.spinner("Searching documents..."):
            retrieved_docs = retrieve_docs(vectorstore, query)
            context = build_context(retrieved_docs)
            answer = stream_answer(llm, context, query)
            sources = format_sources(retrieved_docs)

    st.session_state.chat_history.append(
        {
            "question": query,
            "answer": answer,
            "sources": sources,
            "answer_type": query_type,
        }
    )

    st.rerun()