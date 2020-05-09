SELECT 
    order_id
    , count(product_id) AS product_count
FROM
    {{ ref('order_products') }}
GROUP BY order_id