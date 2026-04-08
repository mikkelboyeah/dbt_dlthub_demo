-- dim_weather.sql
{{ config(materialized='table') }}

with staging as (
    select * from {{ ref('stg_weather') }}
)

select
    forecast_time::timestamp as forecast_time,
    air_temp_celsius,
    wind_speed_mps,
    relative_humidity_pct
from staging
