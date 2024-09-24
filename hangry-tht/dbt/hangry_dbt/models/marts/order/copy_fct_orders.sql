with orders as (
    select 
        *
    from 
        {{ ref('int_orders_fraud_filtered')}}
),

promotions as (
    select 
        *
    from 
        {{ ref('stg_promotions')}}
),

menus as (
    select
        *,
        effective_date as start_date,
        LEAD(effective_date, 1) OVER (PARTITION BY menu_id ORDER BY effective_date) AS end_date
    from 
        {{ ref('stg_menus')}}
),

order_with_promotion as (
    select 
        o.order_id,
        o.menu_id,
        o.quantity,
        o.sales_date,
        coalesce(p.disc_value, 0.0) as discount_rate,
        coalesce(p.max_disc, 0) as max_discount
    from
        orders as o
        left join promotions as p
        on o.sales_date >= p.start_date
        and o.sales_date <= p.end_date
    order by o.order_id
),

final as (
    select
        op.order_id,
        m.brand,
        m.name,
        m.price,
        m.cogs,
        op.quantity,
        op.sales_date,
        op.discount_rate,
        op.max_discount
    from 
        order_with_promotion as op
        left join menus as m
        on op.menu_id = m.menu_id
        and op.sales_date >= m.start_date
        and (op.sales_date < m.end_date or end_date is null)
    order by 
        sales_date, order_id
)

select * from final 