# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

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

# Area de creación de funciones
def _get_api():
    import requests
    url = 'https://my.api.mockaroo.com/sales_db.json'
    headers = {"X-API-Key": "6d1e19d0"}
    response = requests.get(url, headers)
    with open('/tmp/sales_db_py.csv', 'wb') as file:
        file.write(response.content)
        file.close()

def _join_trans():
    import pandas as pd

    df_py = pd.read_csv('/tmp/sales_db_py.csv')
    print(df_py.head)
    df_bash = pd.read_csv('/tmp/sales_db_bash.csv')
    print(df_bash.head())
    df = pd.concat([df_py, df_bash], ignore_index = True)
    df = df.groupby(['date', 'store'])['sales'].sum().reset_index()
    df = df.rename(columns={'date':'ddate'})
    df.to_csv('/tmp/sales_db.csv', sep='\t', index=False, header=False)
    print(df.head())

def _load_data():
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    pd_hook = PostgresHook(postgres_conn_id='postgres_conn_local')
    pd_hook.bulk_load(table='sales_db', tmp_file='/tmp/sales_db.csv')


with DAG(
    'DAG_ETL_Postgres',
    default_args = default_args,
    description = 'Creacion de DAG ETL PosgreSQL',
    schedule_interval=None,
    tags=['ETL', 'Ingenieria', 'PosgreSQL'],
) as dag:
    get_api_python = PythonOperator(
        task_id = 'get_api_python',
        python_callable = _get_api
    )

    get_api_bash = BashOperator(
        task_id = 'get_api_bash',
        bash_command = 'curl -H "X-API-Key: 6d1e19d0" https://my.api.mockaroo.com/sales_db.json > /tmp/sales_db_bash.csv'
    )

    join_trans = PythonOperator(
        task_id = 'join_trans',
        python_callable = _join_trans
    )

    check_table = PostgresOperator(
        task_id = 'check_table',
        postgres_conn_id = 'postgres_conn_local',
        sql = 'sql/create_table.sql'
    )

    load_data = PythonOperator(
        task_id = 'load_data',
        python_callable = _load_data
    )

    [get_api_bash, get_api_python] >> join_trans >> check_table >> load_data

