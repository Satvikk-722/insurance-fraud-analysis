# ==========================================
# Insurance Fraud Risk Analytics
# Phase 1: Data Loading & Initial Audit
# ==========================================

import pandas as pd
import numpy as np

def load_data(data_path="../data/"):
    customers = pd.read_csv(f"{data_path}customers.csv")
    policies = pd.read_csv(f"{data_path}policies.csv")
    claims = pd.read_csv(f"{data_path}claims_raw.csv")
    payments = pd.read_csv(f"{data_path}payments.csv")

    return customers, policies, claims, payments

# -------------------------------
# Execute
# -------------------------------

customers, policies, claims, payments = load_data()

# print("Data Loaded Successfully ✅\n")

def audit_table(df, table_name):
    print(f"\n{'='*50}")
    print(f"Audit Report for: {table_name}")
    print(f"{'='*50}")

    print("\nShape:", df.shape)
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nDuplicate Rows:", df.duplicated().sum())
    print("\nSummary Statistics:\n", df.describe())


# audit_table(customers, "Customers")
# audit_table(policies, "Policies")
# audit_table(claims, "Claims")
# audit_table(payments, "Payments") 


# fraud_rate = claims['fraud_flag'].mean() * 100       #Fraud Rate= FraudClaims​/TotalClaims 
# print(f"\nOverall Fraud Rate: {fraud_rate:.2f}%")


# negative_days = (claims['days_since_policy_start'] < 0).sum() 
# print("Negative days_since_policy_start:", negative_days)



# REMOVING DUPLICATES 
# print("\nRemoving duplicate rows from Claims...")
claims_before = len(claims)
claims = claims.drop_duplicates()
claims_after = len(claims)
# print(f"Duplicates removed: {claims_before - claims_after}")
# print(f"Remaining rows: {claims_after}")



# REMOVING NEGATIVE DAYS
# print("\nRemoving logically invalid negative days...")
claims = claims[claims['days_since_policy_start'] >= 0]
# print("Remaining rows after removing negative days:", len(claims))

fraud_rate = claims['fraud_flag'].mean() * 100
# print(f"\nFraud Rate After Cleaning: {fraud_rate:.2f}%")



# FILLING CLAIM_TYPE 
# missing_claim_type_before = claims['claim_type'].isnull().sum()
# print("Missing claim_type BEFORE:", missing_claim_type_before)

claims['claim_type'] = claims['claim_type'].fillna("Unknown")

# missing_claim_type_after = claims['claim_type'].isnull().sum()
# print("Missing claim_type AFTER:", missing_claim_type_after)



# FILLING CUSTOMERS TABLE : INCOME 
# missing_income_before = customers['income'].isnull().sum()
# print("\nMissing income BEFORE:", missing_income_before)

median_income = customers['income'].median()

customers['income'] = customers['income'].fillna(median_income)

# missing_income_after = customers['income'].isnull().sum()
# print("Missing income AFTER:", missing_income_after)
 

# ==========================================
# Export Cleaned Data
# ==========================================

customers.to_csv("../data/customers_cleaned.csv", index=False)
policies.to_csv("../data/policies_cleaned.csv", index=False)
claims.to_csv("../data/claims_cleaned.csv", index=False)
payments.to_csv("../data/payments_cleaned.csv", index=False)

print("\nCleaned CSV files exported successfully ✅")



