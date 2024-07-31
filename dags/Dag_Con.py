from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.external_task import ExternalTaskSensor


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
    'Dag_Analitica_MKT',
    schedule_interval='@daily',
    default_args = default_args,
    description = 'Dag de Analitica y sensor',
    tags=['Ingenieria'],
) as dag:
    
    start = DummyOperator(
        task_id="start",
        # ui_color='#e8f7e4'
    )

    sensor_DB_Ventas_Raw = ExternalTaskSensor(
        task_id = 'sensor_DB_Ventas_Raw',
        external_dag_id = 'DG_Ventas',
        external_task_id = 'transform2',
        allowed_states=['success']
    )

    mkt_data = DummyOperator(
        task_id = 'mkt_data'
    )

    join_transform = DummyOperator(
        task_id = 'join_transform'
    )

    ingest = DummyOperator(
        task_id="ingest",
        # ui_color='#e8f7e4'
    )

    end = DummyOperator(
        task_id="end",
        # ui_color='#e8f7e4'
    )

    start >> [sensor_DB_Ventas_Raw, mkt_data] >> join_transform >> ingest >> end