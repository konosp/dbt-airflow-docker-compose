SELECT
    t2.product_id
    , t2.product_name
    , t2.aisle_id
    , t2.department_id
    , count(t1.order_id) as number_of_orders
FROM
    {{ ref('order_products') }} as t1
LEFT JOIN
    {{ source('instacart_raw_data','products') }} as t2
ON 
    t1.product_id = t2.product_id
GROUP BY
    t2.product_id
    , t2.product_name
    , t2.aisle_id
    , t2.department_id
ORDER BY
    number_of_orders DESC