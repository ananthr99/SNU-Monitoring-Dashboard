CREATE OR REPLACE VIEW vwmon_SNUSiteDetailsDaily AS
SELECT DISTINCT
	c1.rec_date,
	c1.smsitecode,
	c1.smsitename,
	c2.ref_date,
	CONCAT('day', DATEDIFF(c2.ref_date, c1.rec_date)) AS aging_bucket
FROM
(
	SELECT
		smsiteid,
		smsitecode,
		smsitename,
		DATE(FROM_UNIXTIME(rectimestamp)) AS rec_date
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
	ORDER BY DATE(FROM_UNIXTIME(rectimestamp))
) c2
ON c1.rec_date BETWEEN DATE_SUB(c2.ref_date, INTERVAL 7 DAY) AND DATE_SUB(c2.ref_date, INTERVAL 1 DAY)
ORDER BY c2.ref_date,c1.rec_date,c1.smsitecode,c1.smsitename;