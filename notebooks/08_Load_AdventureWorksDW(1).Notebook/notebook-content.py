# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "9ef2f10f-d9a6-45da-90f6-0e17841b6d90",
# META       "default_lakehouse_name": "Zava_Lakehouse",
# META       "default_lakehouse_workspace_id": "524dfea1-0c59-477f-81bd-f4ad4461d8b9",
# META       "known_lakehouses": [
# META         {
# META           "id": "9ef2f10f-d9a6-45da-90f6-0e17841b6d90"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import pandas as pd
from tqdm.auto import tqdm
base = "https://synapseaisolutionsa.z13.web.core.windows.net/data/AdventureWorks"

# load list of tables
df_tables = pd.read_csv(f"{base}/adventureworks.csv", names=["table"])

for table in (pbar := tqdm(df_tables['table'].values)):
    pbar.set_description(f"Uploading {table} to lakehouse")

    # download
    df = pd.read_parquet(f"{base}/{table}.parquet")

    # save as lakehouse table
    spark.createDataFrame(df).write.mode('overwrite').saveAsTable(table)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
