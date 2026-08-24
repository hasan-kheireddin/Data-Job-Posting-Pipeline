SELECT
    job_title,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_usd), 2) AS avg_salary,
    MAX(salary_usd) AS max_salary,
    MIN(salary_usd) AS min_salary
FROM pipeline_db.processed
GROUP BY job_title
ORDER BY avg_salary DESC;