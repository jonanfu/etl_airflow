from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator


# imports
from datetime import datetime, timedelta

default_args = {
    'owner': 'Codigo Facilito Team',
    'start_date': datetime(2024, 7, 25),
    'depends_on_past': False,
    'email_on_failture': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=20)
}

with DAG(
    'Dag_Ventas',
    schedule_interval='@daily',
    default_args = default_args,
    description = 'Dag de ventas',
    tags=['Ingenieria'],
) as dag:
    start = DummyOperator(
        task_id="start",
        # ui_color='    #e8f7e  4'  
    )

    extract = DummyOperator(
        task_id="extract",
        # u
        # i_color='#e8f7e4'
    )

    transform1 = DummyOperator(
        task_id="transform1",
        # ui_color='#e8f7e4'
    )

    transform2 = BashOperator(
        task_id="transform2",
        bash_command='sleep 5',
        # env: Optional[Dict[str, str]] = None,
        # output_encoding: str = 'utf-8',
        # skip_exit_code: int = 99,
    )

    ingest1 = DummyOperator(
        task_id="ingest1",
        # ui_color='#e8f7e4'
    )

    ingest2 = DummyOperator(
        task_id="ingest2",
        # ui_color='#e8f7e4'
    )

    end = DummyOperator(
        task_id="end",
        # ui_color='#e8f7e4'
    )

    start >> extract >> [transform1, transform2]
    transform1 >> ingest1
    transform2 >> ingest2
    [ingest1, ingest2] >> end