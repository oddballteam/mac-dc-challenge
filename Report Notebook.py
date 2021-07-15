# Databricks notebook source
# MAGIC %sql
# MAGIC Describe denormalized_data_store;

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Displaying the Top programs by total enrollment in a particular state

# COMMAND ----------

# MAGIC %sql
# MAGIC   SELECT concat(program_name, ': ', plan_name) as progam_plan, program_total_enrollment from denormalized_data_store WHERE state="Texas";

# COMMAND ----------

# MAGIC %md Top Programs in a state as a percentage of that states total enrollment

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT concat(program_name, ': ', plan_name) as progam_plan, (program_total_enrollment/total_medicaid_and_chip_enrollment * 100) as percent from denormalized_data_store WHERE state="Texas" AND program_report_year=2018 ORDER BY percent DESC LIMIT 10 ;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT  SUM(program_total_enrollment/total_medicaid_and_chip_enrollment * 100) from denormalized_data_store WHERE state="Virginia" AND program_report_year=2018;

# COMMAND ----------


