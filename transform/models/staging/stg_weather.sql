-- stg_weather.sql
with source as (
    select * from {{ source('my_dlt_data', 'weather_oslo') }}
),

renamed as (
    select
        time as forecast_time,
        data__instant__details__air_temperature as air_temp_celsius,
        data__instant__details__wind_speed as wind_speed_mps,
        data__instant__details__relative_humidity as relative_humidity_pct
    from source
)

select * from renamed
