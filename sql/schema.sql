/* Script to create the database used by the spacer app */

/* SQLite doesn't have native ENUM types, so I've created separate tables for 
each enumeration and used INTEGER columns as foreign keys in the main tables. */

/* Enum Tables */

-- Create the enumeration types
CREATE TABLE Work_TypeEnum (
    id INTEGER PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO Work_TypeEnum (value) 
    VALUES 
        ('remote'), 
        ('hybrid'), 
        ('on-site');

CREATE TABLE Application_StatusEnum (
    id INTEGER PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO Application_StatusEnum (value)
    VALUES 
        ('applied'), 
        ('interviews in progress'), 
        ('offer made'), 
        ('rejected'),
        ('declined'), -- Declined an offer
        ('discarded'),
        ('opted-out'), -- Opted out during the interview phase
        ('accepted');

CREATE TABLE Interview_TypeEnum (
    id INTEGER PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO Interview_TypeEnum (value) 
    VALUES 
        ('HR'),
        ('screening'), 
        ('technical'), 
        ('cultural'), 
        ('homework'), 
        ('other');

CREATE TABLE Interview_FormatEnum (
    id INTEGER PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO Interview_FormatEnum (value) 
    VALUES 
        ('phone'), 
        ('online'), 
        ('in-person'), 
        ('other');

CREATE TABLE ExperienceLevelEnum (
    id INTEGER PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO ExperienceLevelEnum (value) 
    VALUES 
        ('Internship'), 
        ('Junior'), 
        ('Medior'), 
        ('Senior'), 
        ('Associate'), 
        ('Executive'), 
        ('Other');

/* The MAIN Tables */

-- Create the companies table
CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name TEXT, -- Should be also unique (I can change this in the future)
    is_recruitment_agency BOOLEAN,
    website TEXT,
    comments TEXT
);

-- Create the 'jobs' table
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    job_title TEXT,
    company_id INTEGER,
    date TEXT, -- SQLite does not have a native TIMESTAMP type
    location TEXT,
    url TEXT,
    work_type INTEGER REFERENCES Work_TypeEnum(id),
    experience_level INTEGER REFERENCES ExperienceLevelEnum(id),
    description TEXT,
    comments TEXT,
    -- Define the foreign key constraint
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

-- Create the applications table
CREATE TABLE applications(
    id INTEGER PRIMARY KEY,
    job_id INTEGER,
    date TEXT, -- SQLite does not have a native TIMESTAMP type
    end_date TEXT, -- Date when I discard the job or when I am rejected
    -- I didn't wanted to do a slowly changing dimension thing...
    cover_letter TEXT,
    status INTEGER REFERENCES Application_StatusEnum(id),
    comments TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);

-- Create interviews table
CREATE TABLE interviews(
    id INTEGER PRIMARY KEY,
    job_id INTEGER,
    date TEXT, -- SQLite does not have a native TIMESTAMP type
    interview_type INTEGER REFERENCES Interview_TypeEnum(id),
    interview_format INTEGER REFERENCES Interview_FormatEnum(id),
    comments TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);