SELECT
    t2.aisle
    , sum(t1.number_of_orders) as number_of_orders
FROM 
    {{ ref('stg_top_selling_products') }} as t1
LEFT JOIN
    {{ source('instacart_raw_data','aisles') }} as t2
ON 
    t1.aisle_id = t2.aisle_id
GROUP BY
    t2.aisle
ORDER BY
    number_of_orders DESC
LIMIT 10