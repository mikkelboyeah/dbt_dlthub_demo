-- fct_pokemon.sql
{{ config(materialized='table') }}

with pokemon as (
    select * from {{ ref('stg_pokemon') }}
),

pokemon_stats as (
    select * from {{ ref('stg_pokemon_stats') }}
),

pokemon_types as (
    select * from {{ ref('stg_pokemon_types') }}
),

pivot_stats as (
    select
        pokemon_dlt_id,
        max(case when stat_name = 'hp' then base_stat end) as hp,
        max(case when stat_name = 'attack' then base_stat end) as attack,
        max(case when stat_name = 'defense' then base_stat end) as defense,
        max(case when stat_name = 'speed' then base_stat end) as speed
    from pokemon_stats
    group by 1
),

string_agg_types as (
    select
        pokemon_dlt_id,
        string_agg(type_name, ', ') as type_labels
    from pokemon_types
    group by 1
)

select
    p.pokemon_id,
    p.name,
    p.height,
    p.weight,
    p.base_experience,
    t.type_labels,
    s.hp,
    s.attack,
    s.defense,
    s.speed
from pokemon p
left join string_agg_types t on p._dlt_id = t.pokemon_dlt_id
left join pivot_stats s on p._dlt_id = s.pokemon_dlt_id
order by p.pokemon_id asc
