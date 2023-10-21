/* Script to create the database used by the spacer app */
CREATE DATABASE IF NOT EXISTS spacer_job_board;

-- Connect to the database (this is only in an app like psql)
\c spacer_job_board;

-- Create the enumeration types
CREATE TYPE Work_TypeEnum AS ENUM ('remote', 'hybrid', 'on-site');
CREATE TYPE Application_StatusEnum AS ENUM ('applied', 'interview in progress', 'offer made', 'rejected', 'accepted');
CREATE TYPE Interview_TypeEnum AS ENUM ('hr', 'technical', 'team meeting', 'homework');
CREATE TYPE Interview_FormatEnum AS ENUM ('phone', 'zoom', 'in-person', 'other');

-- Create the companies table
CREATE TABLE companies (
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(100),
	website VARCHAR(300)
);

-- Create the 'jobs' table
CREATE TABLE jobs (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    job_title VARCHAR(200),
    company_id INT,
    date TIMESTAMP,
    location VARCHAR(200),
    url VARCHAR(700),
    work_type Work_TypeEnum,
    experience_level VARCHAR(100),
    trough_agency BOOLEAN,
    description TEXT,
    comments TEXT,
    -- Define the foreign key constraint
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

-- Create the applications table
CREATE TABLE applications(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	job_id INT,
	date TIMESTAMP,
	cover_letter TEXT,
	status Application_StatusEnum,
	FOREIGN KEY (job_id) REFERENCES jobs (id)
);

-- Create interviews table
CREATE TABLE interviews(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	job_id INT,
	date TIMESTAMP,
	interview_type Interview_TypeEnum,
	interview_format Interview_FormatEnum,
	FOREIGN KEY (job_id) REFERENCES jobs (id)
);