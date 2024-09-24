SELECT 
    id,
    start_date,
    end_date,
    disc_value,
    max_disc
FROM 
    {{ source('mage_hangry_dbt', 'sales_pipeline_load_promotion_csv_gcs')}}