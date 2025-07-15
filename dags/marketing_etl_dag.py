from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

def run_etl():
    print("✅ Running placeholder ETL inside Airflow...")

default_args = {
    'start_date': datetime(2024, 1, 1),
}

with DAG('marketing_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    etl_task = PythonOperator(
        task_id='run_etl',
        python_callable=run_etl
    )
