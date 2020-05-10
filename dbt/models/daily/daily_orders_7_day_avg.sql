select sum(daily_orders_count) as summary
FROM {{ ref('daily_orders') }}