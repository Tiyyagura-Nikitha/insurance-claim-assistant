import pandas as pd

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


# Load datasets

policy_df = pd.read_csv(
    "data/insurance_policy_5000.csv"
)

claim_df = pd.read_csv(
    "data/insurance_claims_5000.csv"
)


documents = []


# Creating claim documents

for index, row in claim_df.iterrows():

    text = f"""
Claim Information:

Claim ID:
{row['claim_id']}

Policy ID:
{row['policy_id']}

Claim Date:
{row['claim_date']}

Claim Amount:
{row['claimed_amount']}

Approved Amount:
{row['approved_amount']}

Claim Status:
{row['claim_status']}

Rejection Reason:
{row['rejection_reason']}

Remarks:
{row['remarks']}
"""

    documents.append(
        Document(page_content=text)
    )



# Creating policy documents

for index, row in policy_df.iterrows():

    text = f"""
Policy Information:

Policy ID:
{row['policy_id']}

Policy Holder:
{row['policyholder_name']}

City:
{row['city']}

Policy Type:
{row['policy_type']}

Plan:
{row['plan']}

Sum Insured:
{row['sum_insured']}

Hospitalization Covered:
{row['hospitalization_covered']}

Room Rent Limit:
{row['room_rent_limit_per_day']}

ICU Covered:
{row['icu_covered']}

Ambulance Limit:
{row['ambulance_limit']}

Pre Hospitalization Days:
{row['pre_hospitalization_days']}

Post Hospitalization Days:
{row['post_hospitalization_days']}

Deductible:
{row['deductible']}

Cosmetic Treatment Covered:
{row['cosmetic_treatment_covered']}

Non Medical Expenses Covered:
{row['non_medical_expenses_covered']}

Network Hospital Required:
{row['network_hospital_required']}

Required Documents:
{row['claim_document_requirement']}

Policy Status:
{row['policy_status']}
"""

    documents.append(
        Document(page_content=text)
    )



print("Total Documents Created:", len(documents))
print("Starting embedding creation...")



# Create embedding model

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



# Create FAISS vector database

vector_store = FAISS.from_documents(
    documents,
    embedding_model
)



# Save database

vector_store.save_local(
    "insurance_faiss_db"
)


print("FAISS database created successfully!")