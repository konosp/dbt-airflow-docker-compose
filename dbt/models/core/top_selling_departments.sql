SELECT
    t2.department
    , sum(t1.number_of_orders) as number_of_orders
FROM 
    {{ ref('stg_top_selling_products') }} as t1
LEFT JOIN
    {{ source('instacart_raw_data','departments') }} as t2
ON 
    t1.department_id = t2.department_id
GROUP BY
    t2.department
ORDER BY
    number_of_orders DESC
LIMIT 10