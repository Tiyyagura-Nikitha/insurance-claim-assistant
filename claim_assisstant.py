import pandas as pd
import streamlit as st

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import pipeline


# ==========================================
# 1. LOAD INSURANCE DATA
# ==========================================

claim_df = pd.read_csv(
    "data/insurance_claims_5000.csv"
)

policy_df = pd.read_csv(
    "data/insurance_policy_5000.csv"
)


# ==========================================
# 2. LOAD EMBEDDING MODEL
# ==========================================

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


embedding_model = load_embeddings()


# ==========================================
# 3. LOAD FAISS DATABASE
# ==========================================

@st.cache_resource
def load_vector_store():
    return FAISS.load_local(
        "insurance_faiss_db",
        embedding_model,
        allow_dangerous_deserialization=True
    )


vector_store = load_vector_store()


# ==========================================
# 4. LOAD QWEN LLM
# ==========================================

@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="Qwen/Qwen2.5-1.5B-Instruct",
        device_map="auto"
    )


generator = load_model()


# ==========================================
# 5. KEYWORDS
# ==========================================

status_keywords = [
    "status",
    "claim status"
]

deductible_keywords = [
    "deductible",
    "deductibles"
]

room_keywords = [
    "room rent",
    "room limit",
    "room rental",
    "room charges"
]

amount_keywords = [
    "claim amount",
    "claimed amount",
    "approved amount",
    "rejected amount",
    "how much did i claim",
    "how much was approved"
]

cosmetic_keywords = [
    "cosmetic",
    "cosmetic treatment",
    "cosmetic procedure"
]

coverage_keywords = [
    "coverage",
    "covered",
    "what does my policy cover",
    "what is covered",
    "insurance coverage"
]

rejection_keywords = [
    "rejected",
    "rejection",
    "why was my claim rejected",
    "why rejected",
    "reason for rejection"
]

ambulance_keywords = [
    "ambulance",
    "ambulance limit"
]

icu_keywords = [
    "icu",
    "icu covered"
]

hospitalization_keywords = [
    "hospitalization",
    "hospitalisation",
    "hospitalization covered"
]

pre_hospitalization_keywords = [
    "pre-hospitalization",
    "pre hospitalization",
    "pre hospitalisation"
]

post_hospitalization_keywords = [
    "post-hospitalization",
    "post hospitalization",
    "post hospitalisation"
]

non_medical_keywords = [
    "non-medical",
    "non medical expenses"
]


# ==========================================
# 6. CLEAN LLM RESPONSE
# ==========================================

def clean_answer(answer):

    answer = answer.strip()

    unwanted_phrases = [
        "CUSTOMER QUESTION:",
        "Customer Question:",
        "ANSWER:",
        "Answer:",
        "FINAL RESPONSE:",
        "Final Response:",
        "FINAL ANSWER:",
        "Final Answer:",
        "Thank you",
        "Thank you.",
        "Please ensure",
        "Please note",
        "Note:",
        "Note -",
        "Please check back",
        "Please check your policy",
        "To resolve this issue",
        "This response directly addresses"
    ]

    for phrase in unwanted_phrases:
        if phrase in answer:
            answer = answer.split(phrase)[0].strip()

    # Remove extra whitespace
    answer = " ".join(answer.split())

    # Keep maximum 2 sentences
    sentences = answer.replace("!", ".").replace("?", ".").split(".")

    clean_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            clean_sentences.append(sentence)

        if len(clean_sentences) == 2:
            break

    if clean_sentences:
        answer = ". ".join(clean_sentences) + "."

    return answer

# ==========================================
# 7. MAIN FUNCTION
# ==========================================

def get_claim_answer(claim_id, question):

    claim_id = claim_id.strip()
    question = question.strip()
    question_lower = question.lower()


    # ==========================================
    # 8. FIND CLAIM
    # ==========================================

    claim_result = claim_df[
        claim_df["claim_id"].astype(str).str.upper()
        == claim_id.upper()
    ]

    if claim_result.empty:
        return "Claim ID not found."

    claim = claim_result.iloc[0]


    # ==========================================
    # 9. FIND RELATED POLICY
    # ==========================================

    policy_result = policy_df[
        policy_df["policy_id"].astype(str).str.upper()
        == str(claim["policy_id"]).upper()
    ]

    if policy_result.empty:
        return "Policy information not found."

    policy = policy_result.iloc[0]


    # ==========================================
    # 10. CLAIM STATUS
    # ==========================================

    if any(
        word in question_lower
        for word in status_keywords
    ):
        return (
            f"Your claim status is "
            f"{claim['claim_status']}."
        )


    # ==========================================
    # 11. DEDUCTIBLE
    # ==========================================

    if any(
        word in question_lower
        for word in deductible_keywords
    ):
        return (
            f"Your deductible is "
            f"₹{policy['deductible']}."
        )


    # ==========================================
    # 12. ROOM RENT
    # ==========================================

    if any(
        word in question_lower
        for word in room_keywords
    ):
        return (
            f"Your room rent limit is "
            f"₹{policy['room_rent_limit_per_day']} per day."
        )


    # ==========================================
    # 13. CLAIM AMOUNTS
    # ==========================================

    if any(
        word in question_lower
        for word in amount_keywords
    ):

        if "approved" in question_lower:
            return (
                f"Your approved claim amount is "
                f"₹{claim['approved_amount']}."
            )

        if "rejected" in question_lower:
            return (
                f"Your rejected claim amount is "
                f"₹{claim['rejected_amount']}."
            )

        return (
            f"Your claimed amount is "
            f"₹{claim['claimed_amount']}."
        )


    # ==========================================
    # 14. COSMETIC TREATMENT
    # ==========================================

    if any(
        word in question_lower
        for word in cosmetic_keywords
    ):

        value = str(
            policy["cosmetic_treatment_covered"]
        ).strip().lower()

        if value in ["yes", "true", "covered"]:
            return (
                "Cosmetic treatments are covered "
                "under your policy."
            )

        return (
            "Cosmetic treatments are not covered "
            "under your policy."
        )


    # ==========================================
    # 15. AMBULANCE
    # ==========================================

    if any(
        word in question_lower
        for word in ambulance_keywords
    ):
        return (
            f"Your ambulance coverage limit is "
            f"₹{policy['ambulance_limit']}."
        )


    # ==========================================
    # 16. ICU
    # ==========================================

    if any(
        word in question_lower
        for word in icu_keywords
    ):

        value = str(
            policy["icu_covered"]
        ).strip().lower()

        if value in ["yes", "true", "covered"]:
            return (
                "ICU treatment is covered "
                "under your policy."
            )

        return (
            "ICU treatment is not covered "
            "under your policy."
        )


    # ==========================================
    # 17. HOSPITALIZATION
    # ==========================================

    if any(
        word in question_lower
        for word in hospitalization_keywords
    ):

        value = str(
            policy["hospitalization_covered"]
        ).strip().lower()

        if value in ["yes", "true", "covered"]:
            return (
                "Hospitalization is covered "
                "under your policy."
            )

        return (
            "Hospitalization is not covered "
            "under your policy."
        )


    # ==========================================
    # 18. PRE-HOSPITALIZATION
    # ==========================================

    if any(
        word in question_lower
        for word in pre_hospitalization_keywords
    ):
        return (
            f"Your policy covers "
            f"pre-hospitalization expenses for up to "
            f"{policy['pre_hospitalization_days']} days."
        )


    # ==========================================
    # 19. POST-HOSPITALIZATION
    # ==========================================

    if any(
        word in question_lower
        for word in post_hospitalization_keywords
    ):
        return (
            f"Your policy covers "
            f"post-hospitalization expenses for up to "
            f"{policy['post_hospitalization_days']} days."
        )


    # ==========================================
    # 20. NON-MEDICAL EXPENSES
    # ==========================================

    if any(
        word in question_lower
        for word in non_medical_keywords
    ):

        value = str(
            policy["non_medical_expenses_covered"]
        ).strip().lower()

        if value in ["yes", "true", "covered"]:
            return (
                "Non-medical expenses are covered "
                "under your policy."
            )

        return (
            "Non-medical expenses are not covered "
            "under your policy."
        )


    # ==========================================
    # 21. COVERAGE SUMMARY
    # ==========================================

    if any(
        word in question_lower
        for word in coverage_keywords
    ):

        coverage_parts = []

        hospitalization = str(
            policy["hospitalization_covered"]
        ).strip().lower()

        if hospitalization in [
            "yes",
            "true",
            "covered"
        ]:
            coverage_parts.append(
                "hospitalization"
            )

        icu = str(
            policy["icu_covered"]
        ).strip().lower()

        if icu in [
            "yes",
            "true",
            "covered"
        ]:
            coverage_parts.append(
                "ICU care"
            )

        room_rent = policy[
            "room_rent_limit_per_day"
        ]

        ambulance = policy[
            "ambulance_limit"
        ]

        pre_days = policy[
            "pre_hospitalization_days"
        ]

        post_days = policy[
            "post_hospitalization_days"
        ]

        deductible = policy[
            "deductible"
        ]

        first_sentence = (
            "Your policy covers "
            + ", ".join(coverage_parts)
            + f", with a room rent limit of "
            f"₹{room_rent} per day and ambulance "
            f"coverage up to ₹{ambulance}."
        )

        second_sentence = (
            f"It also provides {pre_days} days of "
            f"pre-hospitalization and {post_days} days "
            f"of post-hospitalization coverage, with a "
            f"deductible of ₹{deductible}."
        )

        return (
            first_sentence
            + " "
            + second_sentence
        )


    # ==========================================
    # 22. CLAIM REJECTION EXPLANATION - LLM
    # ==========================================

    if any(
        word in question_lower
        for word in rejection_keywords
    ):

        claim_status = str(
            claim["claim_status"]
        ).strip()

        rejection_reason = str(
            claim["rejection_reason"]
        ).strip()

        remarks = str(
            claim["remarks"]
        ).strip()


        # --------------------------------------
        # UNDER REVIEW / PENDING
        # --------------------------------------

        if claim_status.lower() in [
            "under review",
            "pending",
            "in progress"
        ]:

            context = f"""
Claim ID: {claim['claim_id']}
Claim Status: {claim_status}
Remarks: {remarks}
"""

            prompt = f"""
You are an insurance claim explanation assistant.

The user asked:
{question}

Verified information:

{context}

The claim has NOT been rejected.

Explain this to the customer in one short sentence.

Rules:
Write exactly one complete sentence.
The claim is still under review and has not been rejected.
Do not add any other information.

Answer:
"""

            result = generator(
                prompt,
                max_new_tokens=40,
                do_sample=False,
                return_full_text=False
            )

            answer = result[0][
                "generated_text"
            ].strip()

            return clean_answer(answer)


        # --------------------------------------
        # REJECTED CLAIM
        # --------------------------------------

        if claim_status.lower() == "rejected":

            if rejection_reason.lower() in [
                "",
                "nan",
                "none"
            ]:
                return (
                    "Your claim was rejected, but "
                    "no specific rejection reason is "
                    "available in the claim records."
                )

            context = f"""
Claim ID: {claim['claim_id']}
Claim Status: {claim_status}
Rejection Reason: {rejection_reason}
Remarks: {remarks}
"""

            prompt = f"""
You are an insurance claim explanation assistant.

The user asked:
{question}

Use ONLY the verified information below.

{context}

Explain the exact rejection reason.

Rules:
- Do not invent information.
- Do not add other reasons.
- Do not provide advice.
- Do not mention policy information.
- Keep the answer to 1 or 2 short sentences.
- Do not say thank you.
- Do not add a closing statement.

Answer:
"""

            result = generator(
                prompt,
                max_new_tokens=35,
                do_sample=False,
                return_full_text=False
            )

            answer = result[0][
                "generated_text"
            ].strip()

            return clean_answer(answer)


        # --------------------------------------
        # OTHER CLAIM STATUS
        # --------------------------------------

        return (
            f"Your claim is currently "
            f"{claim_status}. There is no rejection "
            f"reason recorded for this claim."
        )


    # ==========================================
    # 23. GENERAL QUESTION - LLM + RAG
    # ==========================================

    context = f"""
VERIFIED CLAIM INFORMATION

Claim ID: {claim['claim_id']}
Policy ID: {claim['policy_id']}
Claim Status: {claim['claim_status']}
Claimed Amount: ₹{claim['claimed_amount']}
Approved Amount: ₹{claim['approved_amount']}
Rejected Amount: ₹{claim['rejected_amount']}
Rejection Reason: {claim['rejection_reason']}
Remarks: {claim['remarks']}


VERIFIED POLICY INFORMATION

Policy Type: {policy['policy_type']}
Plan: {policy['plan']}
Sum Insured: ₹{policy['sum_insured']}
Hospitalization Covered: {policy['hospitalization_covered']}
Room Rent Limit: ₹{policy['room_rent_limit_per_day']}
ICU Covered: {policy['icu_covered']}
Ambulance Limit: ₹{policy['ambulance_limit']}
Deductible: ₹{policy['deductible']}
"""


    # ------------------------------------------
    # RAG RETRIEVAL
    # ------------------------------------------

    rag_context = ""

    try:
        retrieved_docs = vector_store.similarity_search(
            question,
            k=1
        )

        if retrieved_docs:
            rag_context = (
                retrieved_docs[0].page_content
            )

    except Exception:
        rag_context = ""


    # ------------------------------------------
    # QWEN PROMPT
    # ------------------------------------------

    prompt = f"""
You are an insurance claim explanation assistant.

Answer the customer's question using only
the verified information.

VERIFIED INFORMATION:

{context}

SUPPLEMENTARY KNOWLEDGE:

{rag_context}

CUSTOMER QUESTION:

{question}

Rules:

1. Answer only the question asked.
2. Use only the provided information.
3. Do not invent facts.
4. Keep the answer to 1-3 short sentences.
5. Use simple customer-friendly language.
6. Do not provide unrelated insurance information.
7. Do not give advice unless asked.
8. Do not provide documentation instructions unless asked.
9. Do not mention other claims or policies.
10. Do not say thank you.
11. Do not add greetings, notes, disclaimers,
or closing statements.
12. Stop immediately after answering.

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=60,
        do_sample=False,
        return_full_text=False
    )

    answer = result[0][
        "generated_text"
    ].strip()

    return clean_answer(answer)