SELECT
    job_title,
    experience_level,
    COUNT(*) AS count,
    ROUND(AVG(salary_usd), 2) AS avg_salary,
    MAX(salary_usd) AS max_salary,
    MIN(salary_usd) AS min_salary
FROM pipeline_db.processed
GROUP BY job_title, experience_level
ORDER BY job_title,
    CASE experience_level
        WHEN 'Entry' THEN 1
        WHEN 'Mid' THEN 2
        WHEN 'Senior' THEN 3
        WHEN 'Lead' THEN 4
        WHEN 'Executive' THEN 5
    END;