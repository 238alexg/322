-- create_tables.sql
-- Created on 2/19/17 by Alex Geoffrey
-- For CIS322 at the University of Oregon

-- User table, contains primary key for reference, username and password (both 16 characters)
CREATE TABLE users (
	-- I am using a primary key since I am more familiar with them (as opposed to using a string as a PK), and to me it makes more sense in terms of efficiency since comparing integers is faster than comparing each of the 16 characters of the username
	user_pk serial primary key,
	-- I am using a 16-character variable size varchar for the username (since it is in the project specification). Variable size allows the password/username to not have a lot of whitespaces.
	username varchar(16),
	-- Similarly, I am using a 16-character password (since it is in the project specification), with a variable size.
	password varchar(16),
	role_fk integer REFERENCES roles
);

-- Roles table, for the users column. Having seperate table means less redundency
CREATE TABLE roles (
	roles_pk serial primary key,
	rolename varchar(25)
);

-- Assets table, with PK, up to 16 chars for tag, and any length for description
CREATE TABLE assets (
	assets_pk serial primary key,
	tag varchar(16),
	description text,
	facility_fk integer REFERENCES facilities NULL,
	arrival_dt timestamp
);

-- Facilities table, with PK, up to 32 chars for name and up to 6 chars for code
CREATE TABLE facilities (
	facility_pk serial primary key,
	name varchar(32),
	code varchar(6)
);
