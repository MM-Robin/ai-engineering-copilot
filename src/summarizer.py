def group_docs_by_file(documents):
    grouped = {}

    for doc in documents:
        source_file = doc.metadata.get("source_file", "Unknown file")
        grouped.setdefault(source_file, []).append(doc)

    return grouped


def summarize_text(llm, text: str):
    prompt = f"""
You are an AI engineering copilot.

Summarize this document in 4-6 clear bullet-style sentences.
Focus only on:
1. main topic
2. important concepts
3. practical meaning

Do not add unrelated information.
Do not mention files that are not in the provided text.

Document:
{text}
"""
    return llm.invoke(prompt)


def summarize_each_file(llm, documents):
    grouped = group_docs_by_file(documents)
    summaries = {}

    for filename, docs in grouped.items():
        combined_text = "\n".join(doc.page_content for doc in docs[:10])
        summaries[filename] = summarize_text(llm, combined_text)

    return summaries