with calculated_metrics as (
    select  
        *,
        price * quantity as gross_revenue,
        least(price * quantity * 0.2, max_discount) as total_discount_applied,
        cogs * quantity as cogs_total,
        (price * quantity) - least(price * quantity * 0.2, max_discount) - (cogs * quantity) as net_profit
    from 
        {{ ref('fct_orders')}}
),

final as (
    select
        name,
        brand,
        date_trunc(sales_date, day) as date,
        sum(gross_revenue) as daily_gross_revenue,
        sum(total_discount_applied) as daily_total_discount_applied,
        sum(cogs_total) as daily_cogs_total,
        sum(net_profit) as daily_net_profit
    from 
        calculated_metrics
    group by
        date, name, brand
)

select * from final
