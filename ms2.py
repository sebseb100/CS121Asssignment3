#we must remove duplicates for extra credit 

import json
from collections import defaultdict
from math import log10, sqrt

# Load the inverted index from the JSON file
def load_inverted_index():
    with open('inverted_index.json', 'r') as f:
        inverted_index = json.load(f)
    return inverted_index

# Calculate the tf-idf score for a term in a document
def calculate_tf_idf(tf, df, N):
    return (1 + log10(tf)) * log10(N / df)

# Search for documents that contain all the query terms using AND operator
def search_documents(query, inverted_index):
    query_terms = query.lower().split()
    result = defaultdict(float)

    for term in query_terms:
        if term in inverted_index:
            docs = inverted_index[term]
            for doc in docs:
                doc_id = doc['doc_id']
                tf = doc['tf-dif']
                df = len(docs)
                N = len(inverted_index)
                tf_idf = calculate_tf_idf(tf, df, N)
                result[doc_id] += tf_idf

    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return sorted_result

# Main function to handle the search queries
def search_main(query):
    inverted_index = load_inverted_index()
    results = search_documents(query, inverted_index)
    return results

# Example usage of the search_main function for the provided queries
if __name__ == "__main__":
    queries = [
        "cristina lopes",
        "machine learning",
        "ACM",
        "master of software engineering"
    ]

    for query in queries:
        results = search_main(query)
        print(f"Search results for query '{query}':")
        for result in results:
            print(f"Document: {result[0]}, Score: {result[1]}")
        print()
