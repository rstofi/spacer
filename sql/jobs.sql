/* Queries related to the companies table */

-- spacer: check_if_job_exists
SELECT job_title FROM jobs WHERE job_title = ? AND company_id = ?;

-- spacer: add_job_application
INSERT INTO jobs(job_title, company_id, date, location, url, work_type, experience_level, description, comments)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
