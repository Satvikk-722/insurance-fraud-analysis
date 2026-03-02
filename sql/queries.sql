CREATE DATABASE insurance_fraud_analysis;
USE insurance_fraud_analysis;
SELECT COUNT(*) FROM customers_cleaned;
SELECT COUNT(*) FROM payments_cleaned;
SELECT COUNT(*) FROM claims_cleaned;
SELECT COUNT(*) FROM policies_cleaned;


-- Verifying Fraud Rate 
SELECT 
    ROUND(AVG(fraud_flag) * 100, 2) AS fraud_rate_percentage
FROM claims_cleaned;  



-- Fraud Rate by Policy Type
SELECT 
    p.policy_type,
    COUNT(c.claim_id) AS total_claims,
    SUM(c.fraud_flag) AS fraud_cases,
    ROUND(AVG(c.fraud_flag) * 100, 2) AS fraud_rate_percentage
FROM claims_cleaned c
JOIN policies_cleaned p 
    ON c.policy_id = p.policy_id
GROUP BY p.policy_type
ORDER BY fraud_rate_percentage DESC;





-- Early Claim vs Fraud
SELECT 
    CASE 
        WHEN days_since_policy_start < 30 THEN 'Early Claim'
        ELSE 'Normal Claim'
    END AS claim_timing,
    COUNT(*) AS total_claims,
    ROUND(AVG(fraud_flag) * 100, 2) AS fraud_rate_percentage
FROM claims_cleaned
GROUP BY claim_timing;



-- High Claim Frequency vs Fraud 
SELECT 
    CASE 
        WHEN claim_frequency_last_12m > 3 THEN 'High Frequency'
        ELSE 'Normal Frequency'
    END AS frequency_group,
    COUNT(*) AS total_claims,
    ROUND(AVG(fraud_flag) * 100, 2) AS fraud_rate_percentage
FROM claims_cleaned
GROUP BY frequency_group;



-- Top 10 high-risk agents
SELECT 
    p.agent_id,
    COUNT(c.claim_id) AS total_claims,
    SUM(c.fraud_flag) AS fraud_cases,
    ROUND(AVG(c.fraud_flag) * 100, 2) AS fraud_rate_percentage
FROM claims_cleaned c
JOIN policies_cleaned p 
    ON c.policy_id = p.policy_id
GROUP BY p.agent_id
HAVING COUNT(c.claim_id) > 50
ORDER BY fraud_rate_percentage DESC
LIMIT 10;


-- Top 10 Most Fraud-Prone Customers
SELECT 
    c.customer_id,
    COUNT(cl.claim_id) AS total_claims,
    SUM(cl.fraud_flag) AS fraud_cases,
    ROUND(AVG(cl.fraud_flag) * 100, 2) AS fraud_rate,
    RANK() OVER (ORDER BY AVG(cl.fraud_flag) DESC) AS fraud_rank
FROM claims_cleaned cl
JOIN policies_cleaned p 
    ON cl.policy_id = p.policy_id
JOIN customers_cleaned c 
    ON p.customer_id = c.customer_id
GROUP BY c.customer_id
HAVING COUNT(cl.claim_id) > 3
ORDER BY fraud_rate DESC
LIMIT 10;


