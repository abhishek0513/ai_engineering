import chromadb

chrome = chromadb.Client()
zorvex_collection = chrome.create_collection(
    name = "zorvex"
)
zorvex_collection.add(
    ids = ["c0", "c1", "c2", "c3"],
    documents = [
        "Leave Policy - Employees are entitled to 20 days of paid leave per year. Leave requests must be submitted at least two weeks in advance.",
        "Medical Policy - Employees are eligible for health insurance coverage. The company covers 80% of the premium, and employees are responsible for the remaining 20%.",
        "Remote Work Policy - Employees may work remotely up to two days per week. Remote work requests must be approved by the manager.",
        "Maternity Policy - Employees are entitled to 12 weeks of paid maternity leave. Requests must be submitted at least four weeks in advance."
    ]
)

result = zorvex_collection.query(
    query_texts = ["What is the Work from home policy?"],
    n_results = 1
)

print(result["documents"][0])