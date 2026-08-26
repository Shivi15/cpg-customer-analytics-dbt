{{ config(
    materialized='table'
) }}

with staging_customers as (
    select * from {{ ref('stg_cpg__customers') }}
)

select
    customer_id,
    first_name,
    last_name,
    email,
    country_code,
    registered_date,
    current_timestamp() as dbt_loaded_at
from staging_customers
