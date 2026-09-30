import pandas as pd


# Load datasets

policy_df = pd.read_csv(
    "data/insurance_policy_5000.csv"
)

claim_df = pd.read_csv(
    "data/insurance_claims_5000.csv"
)



# User input

claim_id = input("Enter Claim ID: ")



# Find claim

claim_details = claim_df[
    claim_df["claim_id"] == claim_id
]


if claim_details.empty:

    print("Claim not found")


else:

    # Extract policy id

    policy_id = claim_details.iloc[0]["policy_id"]


    # Find policy

    policy_details = policy_df[
        policy_df["policy_id"] == policy_id
    ]



    # Convert data into text context

    claim = claim_details.iloc[0]
    policy = policy_details.iloc[0]



    context = f"""

INSURANCE CLAIM INFORMATION

Claim ID: {claim['claim_id']}
Policy ID: {claim['policy_id']}
Patient Name: {claim['patient_name']}
Treatment: {claim['treatment']}
Hospital Name: {claim['hospital_name']}

Hospital Bill: ₹{claim['hospital_bill']}
Claimed Amount: ₹{claim['claimed_amount']}
Approved Amount: ₹{claim['approved_amount']}
Rejected Amount: ₹{claim['rejected_amount']}

Claim Status: {claim['claim_status']}

Documents Submitted:
{claim['documents_received']}

Remarks:
{claim['remarks']}



POLICY INFORMATION

Policy Holder:
{policy['policyholder_name']}

Policy Type:
{policy['policy_type']}

Plan:
{policy['plan']}

Sum Insured:
₹{policy['sum_insured']}

Hospitalization Covered:
{policy['hospitalization_covered']}

Room Rent Limit:
₹{policy['room_rent_limit_per_day']} per day

ICU Covered:
{policy['icu_covered']}

Deductible:
₹{policy['deductible']}

Policy Status:
{policy['policy_status']}

"""


    print("\n========== GENERATED CONTEXT ==========")

    print(context)