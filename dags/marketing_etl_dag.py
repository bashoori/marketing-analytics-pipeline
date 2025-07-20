import sys
import os

# Add root path to import extract, transform, load
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from etl.extract.extract_game_events import extract_game_events
from etl.extract.extract_campaigns import extract_campaign_data
from etl.transform.transform_data import transform_and_join
from etl.load.load_to_postgres import load_to_postgres

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='marketing_etl_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['marketing', 'ETL']
) as dag:

    extract_events = PythonOperator(
        task_id='extract_game_events',
        python_callable=extract_game_events
    )

    extract_campaigns = PythonOperator(
        task_id='extract_campaign_data',
        python_callable=extract_campaign_data
    )

    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_and_join
    )

    load = PythonOperator(
        task_id='load_data',
        python_callable=load_to_postgres
    )

    #  Define task dependencies
    [extract_events, extract_campaigns] >> transform >> load