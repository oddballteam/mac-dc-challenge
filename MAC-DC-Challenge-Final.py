# Databricks notebook source
df = spark.read.format("avro").load("/mnt/nifi-mac-dc/eligibility-enrollment-data.avro" )
df2 = spark.read.format("avro").load("/mnt/nifi-mac-dc/managed-care-data.avro" )
df.createOrReplaceTempView("Rob_Test_Eligibility")
df2.createOrReplaceTempView("Rob_Test_Managed_Care")

# COMMAND ----------

# MAGIC %sql -- Making a temp view to only contain final reports dated 01-01
# MAGIC CREATE
# MAGIC OR REPLACE TEMPORARY VIEW final_reports AS
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   Rob_Test_Eligibility
# MAGIC WHERE
# MAGIC   final_report = "Y"
# MAGIC   AND
# MAGIC   preliminary_updated = "U"
# MAGIC   AND report_date LIKE "%-01-01%";
# MAGIC -- delete the table to recreate it
# MAGIC   DROP TABLE IF EXISTS denormalized_data_store;
# MAGIC -- The mega query, create a table "denormalized data"
# MAGIC   CREATE TABLE denormalized_data_store AS
# MAGIC SELECT
# MAGIC   program_name,
# MAGIC   plan_name,
# MAGIC   geographic_region as program_geographic_region,
# MAGIC   state_name,
# MAGIC   medicaid_only_enrollment :: int as program_medicaid_only_enrollment,
# MAGIC   dual_enrollment :: int as program_dual_enrollment,
# MAGIC   total_enrollment :: int as program_total_enrollment,
# MAGIC   year as program_report_year,
# MAGIC   location as program_location,
# MAGIC   parent_organization as program_parent_organization,
# MAGIC   state,
# MAGIC   state_abbreviation,
# MAGIC   state_expanded_medicaid,
# MAGIC   preliminary_updated,
# MAGIC   final_report,
# MAGIC   new_applications_submitted_to_medicaid_and_chip_agencies :: int as new_applications_submitted_to_medicaid_and_chip_agencies,
# MAGIC   applications_for_financial_assistance_submitted_to_the_state_based_marketplace :: int as applications_for_financial_assistance_submitted_to_the_state_based_marketplace,
# MAGIC   total_applications_for_financial_assistance_submitted_at_state_level :: int total_applications_for_financial_assistance_submitted_at_state_level,
# MAGIC   individuals_determined_eligible_for_medicaid_at_application :: int as individuals_determined_eligible_for_medicaid_at_application,
# MAGIC   individuals_determined_eligible_for_chip_at_application :: int as individuals_determined_eligible_for_chip_at_application,
# MAGIC   total_new_determinations :: int as total_new_determinations,
# MAGIC   medicaid_and_chip_child_enrollment :: int as medicaid_and_chip_child_enrollment,
# MAGIC   total_medicaid_and_chip_enrollment :: int as total_medicaid_and_chip_enrollment,
# MAGIC   latitude,
# MAGIC   longitude,
# MAGIC   geocoded_column,
# MAGIC   total_medicaid_enrollment :: int as total_medicaid_enrollment,
# MAGIC   total_chip_enrollment :: int as total_chip_enrollment,
# MAGIC   report_date
# MAGIC FROM
# MAGIC   Rob_Test_Managed_Care
# MAGIC   INNER JOIN final_reports on Rob_Test_Managed_Care.state LIKE '%' || final_reports.state_name || '%'
# MAGIC   AND year = YEAR(report_date)
# MAGIC ORDER BY
# MAGIC   program_total_enrollment DESC;
# MAGIC   

# COMMAND ----------

