from langchain_ollama import OllamaLLM
from config import LLM_MODEL


def get_llm():
    return OllamaLLM(model=LLM_MODEL)


def stream_answer(llm, context: str, question: str):
    prompt = f"""
You are an AI engineering assistant.

Answer the question using ONLY the provided context.

If the answer is not found in the context, say:
"I could not find that in the documents."

Context:
{context}

Question:
{question}
"""

    for chunk in llm.stream(prompt):
        yield chunk