import pandas as pd


# Load datasets

policy_df = pd.read_csv(
    "data/insurance_policy_5000.csv"
)

claim_df = pd.read_csv(
    "data/insurance_claims_5000.csv"
)



# Taking user input

claim_id = input("Enter Claim ID: ")



# Searching claim

claim_details = claim_df[
    claim_df["claim_id"] == claim_id
]



if claim_details.empty:

    print("Claim not found")


else:

    print("\n========== CLAIM DETAILS ==========")

    print(claim_details)



    # Extract policy ID from claim

    policy_id = claim_details.iloc[0]["policy_id"]



    # Searching policy details

    policy_details = policy_df[
        policy_df["policy_id"] == policy_id
    ]



    print("\n========== POLICY DETAILS ==========")

    print(policy_details)