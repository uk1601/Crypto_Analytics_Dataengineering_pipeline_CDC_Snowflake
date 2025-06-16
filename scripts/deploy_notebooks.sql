/*-----------------------------------------------------------------------------
Script:       deploy_notebooks.sql
Last Updated: 2/25/2025
-----------------------------------------------------------------------------*/

-- Create the Yahoo Finance API Notebook
-- CREATE OR REPLACE NOTEBOOK IDENTIFIER('"CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Yahoo_Finance_API"')
--     FROM '@"CRYPTO_DB"."INTEGRATIONS"."CRYPTO_GIT_REPO"/branches/"{{branch}}"/notebooks/01.Yahoo_Finance_API/'
--     QUERY_WAREHOUSE = 'CRYPTO_WH'
--     MAIN_FILE = '01.Yahoo_Finance_API.ipynb';

-- -- Add a live version
-- ALTER NOTEBOOK "CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Yahoo_Finance_API" ADD LIVE VERSION FROM LAST;

CREATE OR REPLACE NOTEBOOK IDENTIFIER('"CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Load_raw_data_from_csv_files"')
    FROM '@"CRYPTO_DB"."INTEGRATIONS"."CRYPTO_GIT_REPO"/branches/"{{branch}}"/notebooks/02.Load_raw_data_from_csv_files/'
    QUERY_WAREHOUSE = 'CRYPTO_WH'
    MAIN_FILE = '02.Load_raw_data_from_csv_files.ipynb';

-- Add a live version
ALTER NOTEBOOK "CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Load_raw_data_from_csv_files" ADD LIVE VERSION FROM LAST;

CREATE OR REPLACE NOTEBOOK IDENTIFIER('"CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Data_Harmonization"')
    FROM '@"CRYPTO_DB"."INTEGRATIONS"."CRYPTO_GIT_REPO"/branches/"{{branch}}"/notebooks/03.Data_Harmonization/'
    QUERY_WAREHOUSE = 'CRYPTO_WH'
    MAIN_FILE = '03.Data_Harmonization.ipynb';

-- Add a live version
ALTER NOTEBOOK "CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Data_Harmonization" ADD LIVE VERSION FROM LAST;

CREATE OR REPLACE NOTEBOOK IDENTIFIER('"CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Data_Analytics"')
    FROM '@"CRYPTO_DB"."INTEGRATIONS"."CRYPTO_GIT_REPO"/branches/"{{branch}}"/notebooks/04.Data_Analytics/'
    QUERY_WAREHOUSE = 'CRYPTO_WH'
    MAIN_FILE = '04.Data_Analytics.ipynb';

-- Add a live version
ALTER NOTEBOOK "CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Data_Analytics" ADD LIVE VERSION FROM LAST;

CREATE OR REPLACE NOTEBOOK IDENTIFIER('"CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Task_Orchestration"')
    FROM '@"CRYPTO_DB"."INTEGRATIONS"."CRYPTO_GIT_REPO"/branches/"{{branch}}"/notebooks/05.Task_Orchestration/'
    QUERY_WAREHOUSE = 'CRYPTO_WH'
    MAIN_FILE = '05.Task_Orchestration.ipynb';

-- Add a live version
ALTER NOTEBOOK "CRYPTO_DB"."{{env}}_SCHEMA"."{{env}}_Task_Orchestration" ADD LIVE VERSION FROM LAST;
