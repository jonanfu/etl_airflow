# Trigger rules example
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


# imports
from datetime import datetime, timedelta

default_args = {
    'owner': 'Codigo Facilito Team',
    'depends_on_past': False,
    'email_on_failture': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    'DAG_Template_Info',
    default_args = default_args,
    description = 'Ejemplo de informacion de un Dag',
    schedule_interval=None,
    tags=['Ingenieria'],
) as dag:
    def _print_context(**kwargs):
        for key, value in kwargs.items():
            print(f'key: {key} - Value: {value} - Type: {type(value)}')
        
    task_print_context = PythonOperator(
        task_id = 'task_print_context',
        python_callable = _print_context
    )

    task_print_context