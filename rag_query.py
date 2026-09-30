from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Load embedding model

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load FAISS database

vector_store = FAISS.load_local(
    "insurance_faiss_db",
    embedding_model,
    allow_dangerous_deserialization=True
)


# User question

question = input("Ask your insurance question: ")


# Search similar documents

results = vector_store.similarity_search(
    question,
    k=3
)


print("\n===== Relevant Information =====")


for doc in results:
    print(doc.page_content)
    print("----------------------------")