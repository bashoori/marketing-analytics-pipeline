import sys
import os
from datetime import datetime, timedelta

# Add the root path to the Python path for module imports
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import ETL task functions from local modules
from dags.etl.extract.extract_game_events import extract_game_events
from dags.etl.extract.extract_campaigns import extract_campaign_data
from dags.etl.transform.transform_data import transform_and_join
from dags.etl.load.load_to_postgres import load_to_postgres
from dags.etl.extract.trigger_lambda import trigger_lambda_function

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='marketing_etl_pipeline',
    description='ETL pipeline for marketing analytics data',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',  # Run every day
    catchup=False,               # Do not perform backfill
    tags=['marketing', 'ETL']    # Tag for UI filtering
) as dag:

    # Trigger AWS Lambda function (e.g., to fetch fresh data into S3)
    trigger_lambda = PythonOperator(
        task_id='trigger_lambda',
        python_callable=trigger_lambda_function
    )

    # Extract game event data from local/API source
    extract_events = PythonOperator(
        task_id='extract_game_events',
        python_callable=extract_game_events
    )

    # Extract campaign data from local/API source
    extract_campaigns = PythonOperator(
        task_id='extract_campaign_data',
        python_callable=extract_campaign_data
    )

    # Transform and join the extracted datasets
    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_and_join
    )

    # Load the final transformed data into PostgreSQL
    load = PythonOperator(
        task_id='load_data',
        python_callable=load_to_postgres
    )

    # Define task dependencies:
    # 1. First run the Lambda trigger
    # 2. Then run both extract tasks
    # 3. Then transform the merged data
    # 4. Finally, load to the database

    trigger_lambda >> [extract_events, extract_campaigns] >> transform >> load