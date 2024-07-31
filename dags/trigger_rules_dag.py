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

def _extract1():
    print('Extract 1')

def _extract2():
    print('Extract 2')
    raise ValueError('Error en Extract 2')


with DAG(
    'DAG_Trigger_Rules',
    default_args = default_args,
    description = 'Ejemplo de Triggers Rules',
    schedule_interval=None,
    tags=['Ingenieria'],
) as dag:
    
    start = DummyOperator(task_id='start')

    extract1 = python_task = PythonOperator(
        task_id="extract1",
        python_callable=_extract1
    )

    extract2 = python_task = PythonOperator(
        task_id="extract2",
        python_callable=_extract2
    )

    end = DummyOperator(
        task_id="end",
    )

    start >> [extract1, extract2] >> end

