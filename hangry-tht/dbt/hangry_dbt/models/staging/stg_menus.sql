SELECT 
    menu_id,
    brand,
    name,
    price,
    cogs,
    effective_date
FROM 
    {{ source('mage_hangry_dbt', 'sales_pipeline_load_menu_sheet')}}