CREATE OR REPLACE VIEW vwmon_SNUSiteCountsDaily AS
SELECT
    ref_date,
    COUNT(DISTINCT CASE WHEN aging_bucket = 'day1' THEN smsitecode END) AS day1,
    COUNT(DISTINCT CASE WHEN aging_bucket = 'day2' THEN smsitecode END) AS day2,
    COUNT(DISTINCT CASE WHEN aging_bucket = 'day3' THEN smsitecode END) AS day3,
    COUNT(DISTINCT CASE WHEN aging_bucket = 'day4' THEN smsitecode END) AS day4,
    COUNT(DISTINCT CASE WHEN aging_bucket = 'day5' THEN smsitecode END) AS day5,
    COUNT(DISTINCT CASE WHEN aging_bucket = 'day6' THEN smsitecode END) AS day6,
    COUNT(DISTINCT CASE WHEN aging_bucket = 'day7' THEN smsitecode END) AS day7
FROM vwmon_SNUSiteDetailsDaily
GROUP BY ref_date
ORDER BY ref_date;