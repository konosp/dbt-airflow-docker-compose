(
    select *
    from dbt_seed_data.order_products__prior
)
UNION 
(   
    select *
    from dbt_seed_data.order_products__train
)