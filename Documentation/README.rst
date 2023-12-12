SPACER - SimPle job AppliCation trackER
=========================================

``spacer`` is a lightweight command-line tool to track your job applications, helping you stay organized and analyze your statistics using ``python`` and ``Postgres SQL``.


Creating a database for job applications
----------------------------------------

For now the plan is to have an SQL script that creates the tables that `spacer` can work with.


Below is the planned database schema (made with ChatGPT):

**Database Schema Summary**

This database schema is designed to support a job application tracking system. It consists of four tables: JOBS, COMPANY, APPLICATIONS, and INTERVIEWS.

- **jobs Table**: Stores details about job advertisements.
    - Columns: id (Primary Key), job_title, company_id (Foreign Key), url, location, work_type, experience_level, date, description, comments.

- **companies Table**: Contains information about companies to which job applications are submitted.
    - Columns: id (Primary Key), name, website.

- **applications Table**: Tracks job applications and their statuses.
    - Columns: id (Primary Key), job_id (Foreign Key), date, cover_letter, status.

- **interviews Table**: Stores information about interviews associated with job applications.
    - Columns: id (Primary Key), job_id (Foreign Key), date, interview_type, interview_format, comments.

The schema provides a structured foundation for tracking job applications and interview details. It's designed to be flexible, user-friendly, and adaptable to your evolving needs. ENUM types are used for status and interview types to ensure data consistency and integrity. Cover letters are accommodated in the APPLICATIONS table, with the option to leave the field empty for applications that don't require a cover letter.

Additionally, a Comments column is added to the JOBS table to provide extra flexibility for capturing additional information as needed.

