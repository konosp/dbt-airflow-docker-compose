SELECT
    dt
    , daily_orders_count
    , avg(daily_orders_count) OVER (
        ORDER BY dt asc 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as rolling_7_day_avg
FROM
    {{ ref('daily_orders') }}
group by 
    dt
    , daily_orders_count
HAVING  dt >= '{{ var("start_date") }}'
    AND dt < '{{ var("end_date") }}'
order by
    dt asc