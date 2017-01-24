-- Alex Geoffrey
-- Assignment 2
-- SQL Create tables script

CREATE TABLE products (
	product_pk serial primary key,
	vendor text,
	description text,
	alt_description text
);
CREATE TABLE assets (
	asset_pk serial primary key,
	product_fk integer REFERENCES products(product_pk),
	asset_tag text,
	description text,
	alt_description text
);
CREATE TABLE facilities (
	facility_pk serial primary key,
	fcode text,
	common_name text,
	location text
);
CREATE TABLE asset_at (
	asset_fk serial primary key,
	facility_fk integer REFERENCES facilities(facility_pk) not null,
	arrive_dt timestamp,
	depart_dt timestamp
);
CREATE TABLE convoys (
	convoy_pk serial primary key,
	request text,
	source_fk integer REFERENCES facilities(facility_pk) not null,
	dest_fk integer REFERENCES facilities(facility_pk) not null,
	depart_dt timestamp,
	arrive_dt timestamp
);
