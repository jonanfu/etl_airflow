from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.decorators import task_group


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
    'MSPM_Dag',
    start_date=datetime(2024,7,25),
    schedule_interval='@hourly',
    default_args = default_args,
    description = 'Dag de Monitoreo de Sensores para una Planta de Manofacutra',
    tags=['Ingenieria'],
) as dag:
    
    start = DummyOperator(
        task_id="start",
        # ui_color='#e8f7e4'
    )

    end = DummyOperator(
        task_id="end",
        # ui_color='#e8f7e4'
    )
    
    @task_group(group_id='extract_sensor_data')
    def extrac_sensor_data():
        list_sensores = [f'sensor_{i}' for i in range(1, 31)]

        for sensor in list_sensores:
            PythonOperator(
                task_id=f'extract_{sensor}',
                python_callable = lambda: print(f'Extrayendo datos del sensor {sensor}')
            )

    ingest_db = DummyOperator(
        task_id="ingest_db",
        # ui_color=
        # 
        # '#e8f7e4'
    )

    trans_in_db_analisis = DummyOperator(
        task_id="trans_in_db_analisis",
        # ui_color='#e8f7e4'
    )

    email_supervisores = DummyOperator(
        task_id="email_supervisores",
        # ui_color='#e8f7e4'
    )

    email_mantenimiento = DummyOperator(
        task_id="email_mantenimiento",
        # ui_color='#e8f7e4'
    )

    update_dash_mantenimiento = DummyOperator(
        task_id="update_dash_mantenimiento",
        # ui_color='#e8f7e4'
    )

    update_dash_produccion = DummyOperator(
        task_id="update_dash_produccion",
        # ui_color='#e8f7e4'
    )

    start >> extrac_sensor_data() >> ingest_db >> trans_in_db_analisis
    trans_in_db_analisis >> [email_supervisores,
                             email_mantenimiento,
                             update_dash_mantenimiento,
                             update_dash_produccion] >> end