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
    'ARSMM_Dag',
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    default_args = default_args,
    description = 'Dag de Analisis de Redes Sociales para una Marca de Moda',
    tags=['Ingenieria'],
) as dag:
    
    extrac_facebook_api = DummyOperator(
        task_id="extrac_facebook_api",
        # ui_color='#e8f7e4'
    )

    extrac_tw_api = DummyOperator(
        task_id="extrac_tw_api",
        # ui_color='#e8f7e4'
    )

    extrac_instagram_api = DummyOperator(
        task_id="extrac_instagram_api",
        # ui_color='#e8f7e4'
    )

    trans_join_data = DummyOperator(
        task_id="trans_join_data",
        # ui_color=
        # 
        # '#e8f7e4'
    )

    consumo_modelo_nlp = DummyOperator(
        task_id="consumo_modelo_nlp",
        # ui_color='#e8f7e4'
    )

    ingest_db = DummyOperator(
        task_id="ingest_db",
        # ui_color='#e8f7e4'
    )

    [extrac_facebook_api, extrac_tw_api, extrac_instagram_api] >> trans_join_data
    trans_join_data >> consumo_modelo_nlp
    consumo_modelo_nlp >> ingest_db