with source as (
    select * from {{ source('cpg_raw', 'raw_products') }}
),

renamed as (
    select
        trim(product_id) as product_id,
        trim(sku_name) as sku_name,
        trim(category) as category_name,
        cast(unit_cost_gbp as number(10, 2)) as unit_cost_gbp,
        cast(msrp_gbp as number(10, 2)) as msrp_gbp,
        round(cast(msrp_gbp as number(10, 2)) - cast(unit_cost_gbp as number(10, 2)), 2) as gross_margin_gbp
    from source
)

select * from renamed
