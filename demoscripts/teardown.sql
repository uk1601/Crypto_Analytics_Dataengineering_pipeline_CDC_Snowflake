/*-----------------------------------------------------------------------------
Script:       teardown.sql
Last Updated: 2/25/2025
-----------------------------------------------------------------------------*/


USE ROLE ACCOUNTADMIN;

DROP API INTEGRATION CRYPTO_GITHUB_API_INTEGRATION;
DROP DATABASE CRYPTO_DB;
DROP WAREHOUSE CRYPTO_WH;
DROP ROLE CRYPTO_ROLE;


-- Remove the relevant branch in your repo