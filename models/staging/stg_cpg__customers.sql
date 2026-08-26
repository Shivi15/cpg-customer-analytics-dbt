with source as (
    select * from {{ source('cpg_raw', 'raw_customers') }}
),

renamed as (
    select
        trim(customer_id) as customer_id,
        trim(first_name) as first_name,
        trim(last_name) as last_name,
        lower(trim(email)) as email,
        upper(trim(country)) as country_code,
        cast(signup_date as date) as registered_date
    from source
)

select * from renamed
