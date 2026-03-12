#  AI Engineering Copilot

AI Engineering Copilot is a **Retrieval-Augmented Generation (RAG) assistant** that allows users to upload technical PDF documents and ask questions about their content using a **local Large Language Model (LLM)**.

The system retrieves relevant document sections using semantic search and generates answers with **source citations and page numbers**.

---

#  Features

✔ Upload multiple PDF documents  
✔ Ask questions about technical documents  
✔ Retrieval-Augmented Generation (RAG) pipeline  
✔ Semantic search using HuggingFace embeddings  
✔ Vector database for document retrieval  
✔ Local LLM inference using **Ollama**  
✔ Chat interface built with **Streamlit**  
✔ Source citations with file name and page number  
✔ Document summarization  
✔ File listing capability  
✔ Chat history maintained during session  

---

#  System Architecture

```
User Question
     ↓
Streamlit Chat Interface
     ↓
Retriever (Vector Search)
     ↓
Relevant Document Chunks
     ↓
Local LLM (Ollama)
     ↓
Generated Answer + Sources
```

This architecture follows the **Retrieval-Augmented Generation (RAG)** pattern commonly used in production AI systems.

---

#  Tech Stack

| Component | Technology |
|--------|--------|
| Language | Python |
| LLM Framework | LangChain |
| Embeddings | HuggingFace |
| Vector Database | FAISS / Vector Store |
| Local LLM | Ollama |
| UI | Streamlit |
| NLP Method | Retrieval-Augmented Generation (RAG) |

---

#  Project Structure

```
ai-engineering-copilot/

config.py
prompts.py
requirements.txt

src/
│
├ embeddings.py
├ llm.py
├ loader.py
├ retriever.py
├ router.py
├ splitter.py
├ summarizer.py
└ vectordb.py

ui/
└ streamlit_app.py
```

---

#  Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/MM-Robin/ai-engineering-copilot.git
cd ai-engineering-copilot
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Install Ollama

Download Ollama

```
https://ollama.com
```

Pull a model

```bash
ollama pull llama3
```

---

#  Run the Application

```bash
streamlit run ui/streamlit_app.py
```

Open the browser and upload your documents.

---

---

#  Demo

Upload technical PDFs and interact with them through a chat interface.

Example response includes:

• Generated answer  
• Document source  
• Page number references  

The system will retrieve relevant document sections and generate answers.

---

#  Future Improvements

• Streaming responses (ChatGPT-style)  
• Multi-document smart routing  
• Faster vector search  
• Persistent conversation memory  
• Cloud deployment  

---

#  Author

**Mainuddin Robin**

---
