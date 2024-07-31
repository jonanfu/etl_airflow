from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator


# imports
from datetime import datetime, timedelta
import random

default_args = {
    'owner': 'Codigo Facilito Team',
    'start_date': datetime(2024, 7, 1),
    'depends_on_past': False,
    'email_on_failture': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=20)
}

def _extract():
    print('Extracting data')
    print('Counting data')
    return random.randint(1,10)

def _branch(**kwargs):
    ti = kwargs['ti']
    row = ti.xcom_pull(task_ids='extract')
    if row > 5:
        return 'transform1'
    return 'predict_lost_data' 

with DAG(
    'Dag_Branch',
    schedule_interval='@daily',
    default_args = default_args,
    description = 'Dag de ventas',
    tags=['Ingenieria'],
) as dag:
    
    start = DummyOperator(
        task_id="start",
        # ui_color='#e8f7e4'
    )
    
    extract = PythonOperator(
        task_id = 'extract',
        python_callable = _extract
    )

    branch_task = BranchPythonOperator(
        task_id='branch_task',
        python_callable = _branch
    )

    transform1 = DummyOperator(
        task_id = 'transform1'
    )

    predict_lost_data = DummyOperator(
        task_id="predict_lost_data",
        # ui_color='#e8f7e4'
    )

    transform2 = DummyOperator(
        task_id="transform2",
        # ui_color='#e8f7e4'
    )

    ingest = DummyOperator(
        task_id="ingest",
        trigger_rule='one_success'
        # ui_color='#e8f7e4'
    )

    end = DummyOperator(
        task_id="end",
        # ui_color='#e8f7e4'
    )

    start >> extract >> branch_task
    branch_task >> transform1
    branch_task >> predict_lost_data >> transform2
    [transform1, transform2] >> ingest >> end


