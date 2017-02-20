-- create_tables.sql
-- Created on 2/19/17 by Alex Geoffrey
-- For CIS322 at the University of Oregon

-- User table, contains primary key for reference, username and password (both 16 characters)
CREATE TABLE users (
	-- I am using a primary key since I am more familiar with them (as opposed to using a string as a PK), and to me it makes more sense in terms of efficiency since comparing integers is faster than comparing each of the 16 characters of the username
	user_pk serial primary key,
	-- I am using a 16-character array for the username (since it is in the project specification)
	username varchar(16),
	-- Similarly, I am using a 16-character password (since it is in the project specification)
	password varchar(16)
);


