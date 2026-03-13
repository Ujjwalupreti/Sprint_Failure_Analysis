SELECT 
    team_seniority_ratio,
    code_churn_lines,
    project_type,
    sprint_description,
    target_failed
FROM agile_sprint_records
WHERE sprint_end_date >= CURRENT_DATE - INTERVAL '6 months';