from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from transformers import pipeline


# -----------------------------
# 1. Load Embedding Model
# -----------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



# -----------------------------
# 2. Load FAISS Database
# -----------------------------

vector_store = FAISS.load_local(
    "insurance_faiss_db",
    embedding_model,
    allow_dangerous_deserialization=True
)



# -----------------------------
# 3. Load Open Source LLM
# -----------------------------

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    max_new_tokens=150
)



# -----------------------------
# 4. User Question
# -----------------------------

question = input(
    "Ask your insurance question: "
)



# -----------------------------
# 5. Retrieve Relevant Documents
# -----------------------------

docs = vector_store.similarity_search(
    question,
    k=1
)



# -----------------------------
# 6. Prepare Context
# -----------------------------

context = ""

for doc in docs:
    context += doc.page_content



# -----------------------------
# 7. Create Prompt
# -----------------------------

prompt = f"""

You are an insurance claim assistant.

Answer the user's question using only the insurance information provided.

Insurance Information:

{context}


Question:

{question}


Provide a short and clear explanation.

Answer:
"""



# -----------------------------
# 8. Generate AI Response
# -----------------------------

response = generator(
    prompt,
    max_new_tokens=150,
    do_sample=False
)



# -----------------------------
# 9. Display Answer
# -----------------------------

print("\n========== AI Explanation ==========\n")

print(
    response[0]["generated_text"].replace(prompt, "").strip()
)