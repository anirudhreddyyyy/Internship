def search_documents(query, documents):
    query = query.lower()
    results = []

    for doc in documents:
        if (
            query in doc.filename.lower()
            or (doc.category and query in doc.category.lower())
            or (doc.content and query in doc.content.lower())
        ):
            results.append(doc)

    return results
