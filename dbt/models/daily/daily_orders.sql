select
    date(order_date) as dt,
    count(order_id) as daily_orders_count
from
    {{ ref('clean_orders') }}

{% if is_incremental() %}

    {% if adapter.get_relation(this.database, this.schema, this.table) and not flags.FULL_REFRESH %}
        WHERE order_date >= '{{ var("start_date") }}' AND order_date < '{{ var("end_date") }}'
    {% endif %}

{% endif %}
    
group by
    dt
order by
    dt asc