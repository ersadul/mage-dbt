with first_order_date as (
    select 
        order_id, 
        min(sales_date) as first_sales_date
    from 
        {{ ref('int_orders_fraud_filtered')}}
    group by order_id
), 

invalid_orders as (
    select 
        o.*
    from
        {{ ref('int_orders_fraud_filtered')}} as o
    join first_order_date f 
        on o.order_id = f.order_id
    where o.sales_date > f.first_sales_date
)

select * from invalid_orders