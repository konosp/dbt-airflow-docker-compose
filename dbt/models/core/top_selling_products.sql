SELECT
    t1.product_name
    , t1.number_of_orders
FROM
    {{ ref('stg_top_selling_products') }} as t1
ORDER BY
    t1.number_of_orders DESC
LIMIT 10