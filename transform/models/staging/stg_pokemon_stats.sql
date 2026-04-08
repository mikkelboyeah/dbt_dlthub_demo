-- stg_pokemon_stats.sql
with source as (
    select * from {{ source('my_dlt_data', 'pokemon__stats') }}
),

renamed as (
    select
        _dlt_id,
        _dlt_parent_id as pokemon_dlt_id,
        base_stat,
        effort,
        stat__name as stat_name
    from source
)

select * from renamed
