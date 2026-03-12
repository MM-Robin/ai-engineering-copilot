def detect_query_type(question: str) -> str:
    q = question.lower().strip()

    # file listing intent
    if (
        ("list" in q and "file" in q)
        or ("show" in q and "file" in q)
        or ("which" in q and "file" in q)
        or ("what" in q and "file" in q)
    ):
        return "list_files"

    # summarize all files intent
    if (
        ("summarize" in q and "file" in q)
        or ("summary" in q and "file" in q)
    ):
        return "summarize_all"

    return "qa"