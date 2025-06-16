/*-----------------------------------------------------------------------------
Script:       deploy_notebooks.sql
Last Updated: 2/25/2025
-----------------------------------------------------------------------------*/

-- See https://docs.snowflake.com/en/LIMITEDACCESS/execute-immediate-from-template

-- Create the Notebooks
--USE SCHEMA {{env}}_SCHEMA;

CREATE OR REPLACE NOTEBOOK IDENTIFIER('"CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_06_load_excel_files"')
    FROM '@"CRYPTO_DB"."INTEGRATIONS"."CRYPTO_GIT_REPO"/branches/"{{branch}}"/notebooks/06_load_excel_files/'
    QUERY_WAREHOUSE = 'CRYPTO_WH'
    MAIN_FILE = '06_load_excel_files.ipynb';

ALTER NOTEBOOK "CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_06_load_excel_files" ADD LIVE VERSION FROM LAST;

CREATE OR REPLACE NOTEBOOK IDENTIFIER('"CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_07_load_daily_city_metrics"')
    FROM '@"CRYPTO_DB"."INTEGRATIONS"."CRYPTO_GIT_REPO"/branches/"{{branch}}"/notebooks/07_load_daily_city_metrics/'
    QUERY_WAREHOUSE = 'CRYPTO_WH'
    MAIN_FILE = '07_load_daily_city_metrics.ipynb';

ALTER NOTEBOOK "CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_07_load_daily_city_metrics" ADD LIVE VERSION FROM LAST;