from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

# get all PDF files from the specified data folder
def get_pdf_files(data_folder: str):
    folder = Path(data_folder)

    if not folder.exists():
        raise FileNotFoundError(f"Data folder not found: {data_folder}")

    pdf_files = sorted(folder.glob("*.pdf"))

    if not pdf_files:
        raise ValueError(f"No PDF files found in folder: {data_folder}")

    return pdf_files


def load_all_pdfs(pdf_files):
    all_documents = []

    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file.name}")
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()

        for doc in docs:
            doc.metadata["source_file"] = pdf_file.name

        all_documents.extend(docs)

    if not all_documents:
        raise ValueError("No documents could be loaded from the PDFs.")

    return all_documents