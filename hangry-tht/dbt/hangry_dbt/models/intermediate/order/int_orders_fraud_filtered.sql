{{ config(
    materialized='ephemeral'
)}}

with first_order_date as (
    select 
        order_id, 
        min(sales_date) as first_sales_date
    from 
        {{ ref('stg_orders')}}
    group by order_id
), 

valid_orders as (
    select 
        o.*,
        f.first_sales_date
    from
        {{ ref('stg_orders')}} as o
    join first_order_date f 
        on o.order_id = f.order_id
        
),

agg_quantity as (
    SELECT
        order_id,
        menu_id,
        SUM(quantity) AS quantity,
        first_sales_date as sales_date
FROM
    valid_orders
GROUP BY
    order_id,
    menu_id,
    sales_date 
order by order_id

)

select * from agg_quantity