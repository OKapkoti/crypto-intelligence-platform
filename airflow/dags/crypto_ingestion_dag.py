from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime


with DAG(
    dag_id="crypto_ingestion_dag",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["crypto", "bronze"]
) as dag:

    fetch_crypto_data = BashOperator(
        task_id="fetch_crypto_data",
        bash_command="python /opt/airflow/src/extract/fetch_crypto_data.py"
    )