{{
    config(
        materialized='view'
    )
}}

SELECT
    *
FROM
    dbt_seed_data.departments