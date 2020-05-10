SELECT
    date(order_date) as dt,
    count(order_id) as daily_orders_count
FROM
    {{ ref('clean_orders') }}
WHERE 
    order_date >= '{{ var("start_date") }}' AND order_date < '{{ var("end_date") }}'
group by
    dt
order by
    dt asc