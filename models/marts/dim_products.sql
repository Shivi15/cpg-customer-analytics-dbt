{{ config(
    materialized='table'
) }}

with staging_products as (
    select * from {{ ref('stg_cpg__products') }}
)

select
    product_id,
    sku_name,
    category_name,
    unit_cost_gbp,
    msrp_gbp,
    gross_margin_gbp,
    round((gross_margin_gbp / nullif(msrp_gbp, 0)) * 100, 2) as gross_margin_percentage,
    current_timestamp() as dbt_loaded_at
from staging_products
