CREATE OR REPLACE VIEW vwmon_SNUSiteCountsWeekly AS
SELECT
    ref_date,
    COUNT(DISTINCT CASE WHEN aging_bucket='<week1' THEN smsitecode END)  AS w1,
    COUNT(DISTINCT CASE WHEN aging_bucket='>week1&<week2' THEN smsitecode END) AS w2,
    COUNT(DISTINCT CASE WHEN aging_bucket='>week2&<week3' THEN smsitecode END) AS w3,
    COUNT(DISTINCT CASE WHEN aging_bucket='>week3&<week4' THEN smsitecode END) AS w4,
    COUNT(DISTINCT CASE WHEN aging_bucket='>week4' THEN smsitecode END)  AS w5
FROM vwmon_SNUSiteDetailsWeekly
GROUP BY ref_date;