SELECT
    job_title,
    CASE
        WHEN remote_ratio = 100 THEN 'Remote'
        WHEN remote_ratio = 0 THEN 'On-site'
        ELSE 'Hybrid'
    END AS work_mode,
    COUNT(*) AS count,
    ROUND(AVG(salary_usd), 2) AS avg_salary,
    MAX(salary_usd) AS max_salary,
    MIN(salary_usd) AS min_salary
FROM pipeline_db.processed
GROUP BY job_title,
    CASE
        WHEN remote_ratio = 100 THEN 'Remote'
        WHEN remote_ratio = 0 THEN 'On-site'
        ELSE 'Hybrid'
    END
ORDER BY job_title, work_mode;