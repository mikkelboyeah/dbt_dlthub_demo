-- stg_pokemon_types.sql
with source as (
    select * from {{ source('my_dlt_data', 'pokemon__types') }}
),

renamed as (
    select
        _dlt_id,
        _dlt_parent_id as pokemon_dlt_id,
        slot,
        type__name as type_name
    from source
)

select * from renamed
