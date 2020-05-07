#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	ALTER ROLE $POSTGRES_USER SET search_path TO $AIRFLOW_SCHEMA;
	CREATE SCHEMA IF NOT EXISTS $DBT_SCHEMA AUTHORIZATION $POSTGRES_USER;
	CREATE SCHEMA IF NOT EXISTS $DBT_SEED_SCHEMA AUTHORIZATION $POSTGRES_USER;
	CREATE SCHEMA IF NOT EXISTS $AIRFLOW_SCHEMA AUTHORIZATION $POSTGRES_USER;

	SET datestyle = "ISO, DMY";

	create table if not exists $DBT_SEED_SCHEMA.order_products__prior (
		order_id           integer,
		product_id         integer,
		add_to_cart_order  integer,
		reordered          integer
	);

	create table if not exists $DBT_SEED_SCHEMA.order_products__train (
		order_id           integer,
		product_id         integer,
		add_to_cart_order  integer,
		reordered          integer
	);

	create table if not exists $DBT_SEED_SCHEMA.orders (
		order_id           	integer,
		user_id				integer,
		eval_set			varchar(10),
		order_number		integer,
		order_dow			integer,
		order_hour_of_day	integer,
		days_since_prior_order real
	);

	create table if not exists $DBT_SEED_SCHEMA.products (
		product_id          integer,
		product_name        varchar(200),
		aisle_id  			integer,
		department_id       integer
	);

	create table if not exists $DBT_SEED_SCHEMA.departments (
		department_id     	integer,
		department        	varchar(100)
	);

	create table if not exists $DBT_SEED_SCHEMA.aisles (
		aisle_id     	integer,
		aisle        	varchar(100)
	);

	-- Import Data
	COPY $DBT_SEED_SCHEMA.order_products__prior FROM '/dbt/data/order_products__prior.csv' DELIMITER ',' CSV HEADER;
	COPY $DBT_SEED_SCHEMA.order_products__train FROM '/dbt/data/order_products__train.csv' DELIMITER ',' CSV HEADER;
	COPY $DBT_SEED_SCHEMA.orders FROM '/dbt/data/orders.csv' DELIMITER ',' CSV HEADER NULL '';
	COPY $DBT_SEED_SCHEMA.products FROM '/dbt/data/products.csv' DELIMITER ',' CSV HEADER;
	COPY $DBT_SEED_SCHEMA.departments FROM '/dbt/data/departments.csv' DELIMITER ',' CSV HEADER;
	COPY $DBT_SEED_SCHEMA.aisles FROM '/dbt/data/aisles.csv' DELIMITER ',' CSV HEADER;
EOSQL