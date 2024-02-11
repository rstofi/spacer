/* Queries related to the companies table */

-- spacer: check_if_company_exists
SELECT name FROM companies WHERE name = ?;

-- spacer: fetch_company_row
SELECT * FROM companies WHERE name = ?;

-- spacer: fetch_company_id
SELECT id FROM companies WHERE name = ?;

-- spacer: add_company
INSERT INTO companies(name, is_recruitment_agency, website, comments)
VALUES (?, ?, ?, ?);