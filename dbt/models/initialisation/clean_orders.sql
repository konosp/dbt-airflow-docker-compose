with initial_dates as (
    -- Initialise with Monday, Jan 6th 2019 as the first day
    select *
    , COALESCE(days_since_prior_order, 0) as days_since_prior_order_v2
    -- Randomize the day of the first order
    , case order_number
        when 1 then timestamp '2019-01-06 00:00:00' + (round(random()) * 5 * INTERVAL '1 week') + INTERVAL '1 day' * order_dow + INTERVAL '1 hour' * order_hour_of_day
    end as random_date_v2
    from {{ source('instacart_raw_data', 'orders') }}
),
cumulative_dates as (
    select *
    , sum(days_since_prior_order_v2) over ( partition by user_id ORDER BY user_id asc, order_number ASC) as days_since_prior_order_cum
    , case order_number
            when 1 then random_date_v2
            else FIRST_VALUE(random_date_v2) OVER (PARTITION BY user_id ORDER BY order_number ASC ) 
        end as first_order 
    from initial_dates
)
select 
    order_id
    , user_id
    , order_number
    , order_dow
    , order_hour_of_day
    , days_since_prior_order
    , days_since_prior_order_cum
    , date_trunc('day', first_order + days_since_prior_order_cum * INTERVAL '1 day') + ( order_hour_of_day * INTERVAL '1 hour' ) as order_date
from cumulative_dates
