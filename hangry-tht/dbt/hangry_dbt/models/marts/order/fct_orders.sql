{{ config(
    materialized='incremental',
) }}

WITH orders AS (
    SELECT *
    FROM {{ ref('int_orders_fraud_filtered') }}
),

promotions AS (
    SELECT *
    FROM {{ ref('stg_promotions') }}
),

menus AS (
    SELECT
        *,
        effective_date AS start_date,
        LEAD(effective_date, 1) OVER (PARTITION BY menu_id ORDER BY effective_date) AS end_date
    FROM {{ ref('stg_menus') }}
),

order_with_promotion AS (
    SELECT 
        o.order_id,
        o.menu_id,
        o.quantity,
        o.sales_date,
        COALESCE(p.disc_value, 0.0) AS discount_rate,
        COALESCE(p.max_disc, 0) AS max_discount
    FROM orders AS o
    LEFT JOIN promotions AS p
    ON o.sales_date >= p.start_date
    AND o.sales_date <= p.end_date
    ORDER BY o.order_id
),

final_data AS (
    SELECT
        op.order_id,
        m.brand,
        m.name,
        m.price,
        m.cogs,
        op.quantity,
        op.sales_date,
        op.discount_rate,
        op.max_discount
    FROM 
        order_with_promotion AS op
    LEFT JOIN menus AS m
    ON op.menu_id = m.menu_id
    AND op.sales_date >= m.start_date
    AND (op.sales_date < m.end_date OR m.end_date IS NULL)
    ORDER BY 
        op.sales_date, op.order_id
),

incremental_fact_data AS (
    SELECT final.*
    FROM final_data final
    LEFT JOIN {{ this }} tgt
    ON final.order_id = tgt.order_id
    AND final.sales_date = tgt.sales_date
    {% if is_incremental() %}
        -- Filter out existing rows during an incremental run
        WHERE tgt.order_id IS NULL
    {% endif %}
)

SELECT *
FROM incremental_fact_data
