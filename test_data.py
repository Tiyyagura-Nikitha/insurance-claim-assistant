import pandas as pd


# Reading insurance policy data
policy_df = pd.read_csv("data/insurance_policy_5000.csv")


# Reading insurance claims data
claim_df = pd.read_csv("data/insurance_claims_5000.csv")


print("========== POLICY DATA ==========")

print(policy_df.head())


print("\n========== CLAIM DATA ==========")

print(claim_df.head())


print("\n========== RECORD COUNT ==========")

print("Total Policy Records:", len(policy_df))

print("Total Claim Records:", len(claim_df))