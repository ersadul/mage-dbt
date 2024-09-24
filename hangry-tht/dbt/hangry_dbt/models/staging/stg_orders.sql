SELECT 
    order_id,
    menu_id,
    quantity,
    sales_date
FROM 
    {{ source('mage_hangry_dbt', 'sales_pipeline_load_order_postgres') }}