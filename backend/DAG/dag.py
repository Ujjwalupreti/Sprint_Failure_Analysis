from airflow import DAG
import sys
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import dag, task
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime
import pandas as pd

project_root = r""
if project_root not in sys.path:
    sys.path.append(project_root)
from models.trainer import train_model

@dag(
    dag_id="sprint_failed_script",
    schedule="@daily",
    start_date=datetime(2023, 11, 1),
    catchup=False
)
def sprint_failed_script():
    
    @task
    def extract_data() -> pd.DataFrame:
        mysql_hook = MySqlHook(mysql_conn_id="mysql_default")
        df = mysql_hook.get_pandas_df(sql="query.sql")
        return df

    @task
    def training_model(df: pd.DataFrame):
        print(f"Data received! Shape: {df.shape}")
        train_model(df)
        return "Model trained successfully"

    extracted_df = extract_data()
    training_model(extracted_df)

sprint_failed_script()