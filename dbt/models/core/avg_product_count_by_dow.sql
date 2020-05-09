SELECT
    t1.order_dow,
    avg(t2.product_count) as avg_product_count
FROM
    {{ ref('clean_orders') }} as t1
LEFT JOIN
    {{ ref('avg_product_count') }} as t2
on t1.order_id = t2.order_id
GROUP BY
    t1.order_dow
ORDER BY
    t1.order_dow ASC
