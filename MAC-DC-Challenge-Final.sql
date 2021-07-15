-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Loading and denormalizing data
-- MAGIC 
-- MAGIC In order to query the data effectively, and use it for display purposes in tableau, we have to denormalize the data and insert it into a hive table.
-- MAGIC First we load the data from the mounted s3 buckets.
-- MAGIC Then we perform a join, while renaming and casting columns

-- COMMAND ----------

-- MAGIC %python
-- MAGIC df = spark.read.format("avro").load("/mnt/nifi-mac-dc/eligibility-enrollment-data.avro" )
-- MAGIC df2 = spark.read.format("avro").load("/mnt/nifi-mac-dc/managed-care-data.avro" )
-- MAGIC df.createOrReplaceTempView("Rob_Test_Eligibility")
-- MAGIC df2.createOrReplaceTempView("Rob_Test_Managed_Care")

-- COMMAND ----------

-- Making a temp view to only contain final reports dated 01-01
CREATE
OR REPLACE TEMPORARY VIEW final_reports AS
SELECT
  *
FROM
  Rob_Test_Eligibility
WHERE
  final_report = "Y"
  AND
  preliminary_updated = "U"
  AND report_date LIKE "%-01-01%";
-- delete the table to recreate it
  DROP TABLE IF EXISTS denormalized_data_store;
-- The mega query, create a table "denormalized data"
  CREATE TABLE denormalized_data_store AS
SELECT
  program_name,
  plan_name,
  geographic_region as program_geographic_region,
  state_name,
  medicaid_only_enrollment :: int as program_medicaid_only_enrollment,
  dual_enrollment :: int as program_dual_enrollment,
  total_enrollment :: int as program_total_enrollment,
  year as program_report_year,
  location as program_location,
  parent_organization as program_parent_organization,
  state,
  state_abbreviation,
  state_expanded_medicaid,
  preliminary_updated,
  final_report,
  new_applications_submitted_to_medicaid_and_chip_agencies :: int as new_applications_submitted_to_medicaid_and_chip_agencies,
  applications_for_financial_assistance_submitted_to_the_state_based_marketplace :: int as applications_for_financial_assistance_submitted_to_the_state_based_marketplace,
  total_applications_for_financial_assistance_submitted_at_state_level :: int total_applications_for_financial_assistance_submitted_at_state_level,
  individuals_determined_eligible_for_medicaid_at_application :: int as individuals_determined_eligible_for_medicaid_at_application,
  individuals_determined_eligible_for_chip_at_application :: int as individuals_determined_eligible_for_chip_at_application,
  total_new_determinations :: int as total_new_determinations,
  medicaid_and_chip_child_enrollment :: int as medicaid_and_chip_child_enrollment,
  total_medicaid_and_chip_enrollment :: int as total_medicaid_and_chip_enrollment,
  latitude,
  longitude,
  geocoded_column,
  total_medicaid_enrollment :: int as total_medicaid_enrollment,
  total_chip_enrollment :: int as total_chip_enrollment,
  report_date
FROM
  Rob_Test_Managed_Care
  INNER JOIN final_reports on Rob_Test_Managed_Care.state LIKE '%' || final_reports.state_name || '%'
  AND year = YEAR(report_date);
  


-- COMMAND ----------


