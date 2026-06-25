from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Om Kapkoti",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="crypto_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 6, 25),
    schedule=None,
    catchup=False,
    tags=["crypto", "data-engineering"],
) as dag:

    fetch_crypto_data = BashOperator(
        task_id="fetch_crypto_data",
        bash_command="""
        cd /opt/airflow/src
        python extract/fetch_crypto_data.py
        """,
    )

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command="""
        docker exec spark \
        /opt/spark/bin/spark-submit \
        /opt/spark-apps/transform/bronze_to_silver.py
        """,
    )

    validate_silver = BashOperator(

        task_id="validate_silver",

        bash_command="""
        docker exec spark \
        /opt/spark/bin/spark-submit \
        /opt/spark-apps/quality/validate_silver.py
        """

    )

    silver_to_gold = BashOperator(
        task_id="silver_to_gold",
        bash_command="""
        docker exec spark \
        /opt/spark/bin/spark-submit \
        /opt/spark-apps/transform/silver_to_gold.py
        """,
    )

    fetch_crypto_data >> bronze_to_silver >> validate_silver >> silver_to_gold