#Airflow imports
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

#GCP imports
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

# imports
from datetime import datetime, timedelta

def _extract_data(platform):
    import requests
    url = 'https://my.api.mockaroo.com/marketing_camp.json'
    headers = {"X-API-Key": "6d1e19d0"}
    response = requests.get(url, headers)
    with open(f'/tmp/marketing_stats_{platform}.csv', 'wb') as file:
        file.write(response.content)
        file.close()

default_args = {
    'owner': 'Codigo Facilito Team',
    'depends_on_past': False,
    'email_on_failture': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}

with DAG(
    'Marketing_ETL_DAG',
    schedule_interval=None,
    default_args = default_args,
    description = 'Dag de Marketing ETL',
    tags=['Ingenieria'],
) as dag:
    # Plataforms: google ads, facebook ads, youtube ads
    start = DummyOperator(
        task_id="start",
        # ui_color='#e8f7e4'
    )
    end = DummyOperator(
        task_id="end",
        # ui_color='#e8f7e4'
    )
    
    gads_extract = PythonOperator(
        task_id="gads_extract",
        python_callable=_extract_data,
        # op_kwargs: Optional[Dict] = None,
        op_args = ['gads'],
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )

    fads_extract = PythonOperator(
        task_id="fads_extract",
        python_callable=_extract_data,
        # op_kwargs: Optional[Dict] = None,
        op_args = ['fads'],
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )

    yads_extract = PythonOperator(
        task_id="yads_extract",
        python_callable=_extract_data,
        # op_kwargs: Optional[Dict] = None,
        op_args = ['yads'],
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )

    transf_gads = LocalFilesystemToGCSOperator(
        task_id = 'transf_gads',
        src = '/tmp/marketing_stats_gads.csv',
        dst='marketing_data/marketing_stats_gads.csv',
        bucket='marketing_jonanfu',
        gcp_conn_id='google_cloud_conn'
    )

    transf_fads = LocalFilesystemToGCSOperator(
        task_id = 'transf_fads',
        src = '/tmp/marketing_stats_fads.csv',
        dst='marketing_data/marketing_stats_fads.csv',
        bucket='marketing_jonanfu',
        gcp_conn_id='google_cloud_conn'
    )

    transf_yads = LocalFilesystemToGCSOperator(
        task_id = 'transf_yads',
        src = '/tmp/marketing_stats_yads.csv',
        dst='marketing_data/marketing_stats_yads.csv',
        bucket='marketing_jonanfu',
        gcp_conn_id='google_cloud_conn'
    )

    schema_fields = [
        {'name': 'date', 'type': 'DATE'},
        {'name': 'country', 'type': 'STRING'},
        {'name': 'city', 'type': 'STRING'},
        {'name': 'gender', 'type': 'STRING'},
        {'name': 'campaing', 'type': 'STRING'},
        {'name': 'clicks', 'type': 'INTEGER'},
        {'name': 'views', 'type': 'INTEGER'},
        {'name': 'sales', 'type': 'FLOAT'},
        {'name': 'cost', 'type': 'FLOAT'},

    ]

    gads_bigquery = GCSToBigQueryOperator(
        task_id = 'gads_bigquery',
        bucket = 'marketing_jonanfu',
        source_objects = ['marketing_data/marketing_stats_gads.csv'],
        destination_project_dataset_table = 'marketing.gads',
        schema_fields = schema_fields,
        write_disposition = 'WRITE_TRUNCATE',
        skip_leading_rows = 1,
        gcp_conn_id = 'google_cloud_conn'
    )

    fads_bigquery = GCSToBigQueryOperator(
        task_id = 'fads_bigquery',
        bucket = 'marketing_jonanfu',
        source_objects = ['marketing_data/marketing_stats_fads.csv'],
        destination_project_dataset_table = 'marketing.fads',
        schema_fields = schema_fields,
        write_disposition = 'WRITE_TRUNCATE',
        skip_leading_rows = 1,
        gcp_conn_id = 'google_cloud_conn'
    )

    yads_bigquery = GCSToBigQueryOperator(
        task_id = 'yads_bigquery',
        bucket = 'marketing_jonanfu',
        source_objects = ['marketing_data/marketing_stats_yads.csv'],
        destination_project_dataset_table = 'marketing.yads',
        schema_fields = schema_fields,
        write_disposition = 'WRITE_TRUNCATE',
        skip_leading_rows = 1,
        gcp_conn_id = 'google_cloud_conn'
    )


    query = """
    CREATE OR REPLACE TABLE `poner_nombre_bigquery.marketing.insights` AS
    SELECT
    date, campaign, 'gads' as platform,
    sum(clicks) as clicks, sum(views), as views, sum(sales) as sales, sum(cost) as cost
    FROM  `poner_nombre_bigquery.marketing.gads`
    group by 1,2
    union all
    SELECT
    date, campaign, 'fads' as platform,
    sum(clicks) as clicks, sum(views), as views, sum(sales) as sales, sum(cost) as cost
    FROM  `poner_nombre_bigquery.marketing.fads`
    group by 1,2
    union all
    SELECT
    date, campaign, 'yads' as platform,
    sum(clicks) as clicks, sum(views), as views, sum(sales) as sales, sum(cost) as cost
    FROM  `poner_nombre_bigquery.marketing.yads`
    group by 1,2
    union all
    """

    create_view = BigQueryExecuteQueryOperator(
        task_id = 'create_view',
        sql=query,
        use_legacy_sql = False,
        gcp_conn_id='google_cloud_conn'
    )

    start >> [gads_extract, fads_extract, yads_extract]

    gads_extract >> transf_gads >> gads_bigquery
    fads_extract >> transf_fads >> fads_bigquery
    yads_extract >> transf_yads >> yads_bigquery

    [gads_bigquery, fads_bigquery, yads_bigquery] >> create_view >> end
