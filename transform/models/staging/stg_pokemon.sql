-- stg_pokemon.sql
with source as (
    select * from {{ source('my_dlt_data', 'pokemon') }}
),

renamed as (
    select
        _dlt_id,
        id as pokemon_id,
        name,
        height,
        weight,
        base_experience
    from source
)

select * from renamed
