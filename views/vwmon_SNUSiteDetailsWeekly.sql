CREATE OR REPLACE VIEW vwmon_SNUSiteDetailsWeekly AS
SELECT DISTINCT
	c3.ref_date,
	c3.smsitecode,
	c3.smsitename,
	c3.aging_bucket
FROM (
	SELECT
		c2.ref_date,
		c1.smsiteid,
		c1.smsitecode,
		c1.smsitename,
		CASE
			WHEN c1.recdate BETWEEN DATE_SUB(c2.ref_date, INTERVAL 7 DAY) AND DATE_SUB(c2.ref_date, INTERVAL 1 DAY) THEN '<week1'
			WHEN c1.recdate BETWEEN DATE_SUB(c2.ref_date, INTERVAL 14 DAY) AND DATE_SUB(c2.ref_date, INTERVAL 8 DAY) THEN '>week1&<week2'
			WHEN c1.recdate BETWEEN DATE_SUB(c2.ref_date, INTERVAL 21 DAY) AND DATE_SUB(c2.ref_date, INTERVAL 15 DAY) THEN '>week2&<week3'
			WHEN c1.recdate BETWEEN DATE_SUB(c2.ref_date, INTERVAL 28 DAY) AND DATE_SUB(c2.ref_date, INTERVAL 22 DAY) THEN '>week3&<week4'
			WHEN c1.recdate < DATE_SUB(c2.ref_date, INTERVAL 28 DAY) THEN '>week4'
		END AS aging_bucket
	FROM (
		SELECT
			smsiteid,
			smsitecode,
			smsitename,
			DATE(FROM_UNIXTIME(rectimestamp)) AS recdate
		FROM cube_energyconsumption
		WHERE (rhrRTUOnHoursFinal - rhrRTUOnHoursInitial) = 0
		GROUP BY
			DATE(FROM_UNIXTIME(rectimestamp)),
			smsiteid,
			smsitecode,
			smsitename
	) c1
	JOIN
	(
		SELECT DISTINCT DATE(FROM_UNIXTIME(rectimestamp)) AS ref_date
		FROM cube_energyconsumption
	) c2
	ON c1.recdate < c2.ref_date
) c3
WHERE c3.aging_bucket IS NOT NULL;