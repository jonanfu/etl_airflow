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
    'SRP_Dag',
    start_date=datetime(2024,1,1),
    schedule_interval='@monthly',
    default_args = default_args,
    description = 'Dag de Sistema de Recomendación de peliculas',
    tags=['Ingenieria'],
) as dag:
    
    extrac_db_inter = DummyOperator(
        task_id="extrac_db_inter",
        # ui_color='#e8f7e4'
    )

    extrac_api = DummyOperator(
        task_id="extrac_api",
        # ui_color='#e8f7e4'
    )

    trans_join_data = DummyOperator(
        task_id="trans_join_data",
        # ui_color=
        # 
        # '#e8f7e4'
    )

    consumo_modelo_ml_api = DummyOperator(
        task_id="consumo_modelo_ml_api",
        # ui_color='#e8f7e4'
    )

    send_email = DummyOperator(
        task_id="send_email",
        # ui_color='#e8f7e4'
    )

    ingest_db = DummyOperator(
        task_id="ingest_db",
        # ui_color='#e8f7e4'
    )

    [extrac_db_inter, extrac_api] >> trans_join_data
    trans_join_data >> consumo_modelo_ml_api
    consumo_modelo_ml_api >> [send_email, ingest_db]