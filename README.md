# Data Pipeline for Sales Reporting  
## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Tech Stack](#tech-stack)
- [Data Pipeline Design](#data-pipeline-design)
- [Key Features](#key-features)
- [Reporting Dashboard](#reporting-dashboard)
- [dbt overview](#dbt-structure-lineage-and-models)
- [References](#references)
## Project Overview
This project is designed to build an end-to-end data pipeline that generates a data mart for sales reporting using **Mage.ai**. The goal is to provide daily, weekly, and year-to-date (YTD) sales insights, including critical business metrics such as gross revenue, discounts, cost of goods sold (COGS), and net profit.

The project serves as a take-home test for a Data Engineer Analyst position, focusing on developing efficient data pipelines, applying best practices for data quality, and transforming raw sales data into meaningful reports for business users. 

## Objectives
The main objectives of this project are to:
- Ingest and clean raw sales data.
- Create staging and transformation layers to ensure data is structured and ready for analysis.
- Implement daily, weekly, and YTD sales trends for business reporting.
- Present key metrics including gross revenue, total discount applied, COGS, and net profit through a dashboard.
  
## Tech Stack
- **Mage.ai**: For pipeline orchestration and data transformation.
- **dbt**: For data transformation.
- **BigQuery**: For data storage and warehousing.
- **Looker**: For data visualizing.

## Data Pipeline Design
The pipeline processes raw data, applies transformations, and loads the data into a data mart for reporting. It consists of the following steps:
1. **Data Ingestion**: Fetching raw data from various sources (sheet, google cloud storage, postgres).
2. **Data Cleaning and Deduplication**: Handling missing values, data validation, and deduplication to ensure data quality.
3. **Staging Area**: Loading cleaned data into a staging area for transformation.
4. **Data Transformation**: Using dbt to transform the data for daily, weekly, and YTD reports.
5. **Data Loading**: Loading the transformed data into a data warehouse.
6. **Reporting**: Creating a simple dashboard to present the sales metrics, including:
   - **Gross Revenue**
   - **Total Discounts Applied**
   - **COGS**
   - **Net Profit**

## Key Features
- **Daily Sales Trends**: Monitor day-to-day sales performance.
- **Weekly Sales Trends**: Analyze trends over the course of a week.
- **YTD Sales**: Keep track of year-to-date performance.
- **Data Backfilling**: Ensures that historical data is accurately processed.

## Reporting Dashboard
A dashboard is created to present the results of the processed data. Metrics such as gross revenue, total discounts, and net profit are displayed, providing a comprehensive view of the sales performance.
![image](/misc/looker_dashboard.jpg)

## dbt Structure, Lineage, and Models
![image](/misc/models_folder_structure.jpg)  
![image](/misc/mage_data_lineage.jpg)  
![image](/misc/bigquery_materialization.jpg)  

## References
- [mage docs](https://docs.mage.ai/introduction/overview)
- [mage dbt docs](https://docs.mage.ai/guides/dbt/developing-dbt-in-mage)
- [dbt best practice docs](https://docs.getdbt.com/best-practices)
- [dbt fundamentals](https://learn.getdbt.com/learn/course/dbt-fundamentals)
