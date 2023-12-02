/* some example scripts to add an aexample simple row to the database for testing purposes */

-- Connect to the database (this is only in an app like psql)
\c spacer_job_board;

-- Insert a dummy company entry into the 'companies' table
INSERT INTO companies (name, website)
VALUES
    ('Example Company', 'https://www.examplecompany.com');

-- here the company_id should be set to 1 for the new entries

-- Insert a dummy job entry into the 'jobs' table
INSERT INTO jobs (job_title, company_id, date, location, url, work_type, experience_level, trough_agency, description, comments)
VALUES
    ('Software Developer', 1, '2023-10-21 14:30:00', 'Remote', 'https://www.example.com/job', 'remote', 'Intermediate', false, 'Sample job description.', 'Additional comments');

-- here the job_id should be set to 1 for the new entries

-- Insert a dummy job application status entry into the 'applications' table
INSERT INTO applications (job_id, date, cover_letter, status)
VALUES
    (1, '2023-10-23 09:30:00', 'Sample cover letter.', 'applied');

-- Insert a dummy interview entry into the 'interviews' table
INSERT INTO interviews (job_id, date, interview_type, interview_format)
VALUES
    (1, '2023-10-22 10:00:00', 'hr', 'zoom');
