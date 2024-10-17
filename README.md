# Airflow DAG Documentation

## ARSMM_Dag

This DAG is responsible for the analysis of social media networks for a fashion brand. It extracts data from Facebook, Twitter, and Instagram APIs, performs a transformation to join the data, applies a pre-trained NLP model, and ingests the results into a database.

- **Start Date**: January 1, 2024
- **Description**: Dag de Análisis de Redes Sociales para una Marca de Moda
- **Tags**: Ingeniería
- **Schedule Interval**: None (manual trigger)

### Tasks:
- `extrac_facebook_api`: Simulates the extraction of data from Facebook API.
- `extrac_tw_api`: Simulates the extraction of data from Twitter API.
- `extrac_instagram_api`: Simulates the extraction of data from Instagram API.
- `trans_join_data`: Dummy transformation task to join the data from all three platforms.
- `consumo_modelo_nlp`: Simulates the consumption of an NLP model for further analysis.
- `ingest_db`: Simulates the ingestion of the processed data into a database.

## Dag_Branch

This DAG simulates a sales analysis pipeline with a branching logic based on extracted data. If the extracted data exceeds a threshold, it transforms the data; otherwise, it predicts lost data.

- **Start Date**: July 1, 2024
- **Description**: Dag de ventas
- **Tags**: Ingeniería
- **Schedule Interval**: Daily

### Tasks:
- `start`: Marks the beginning of the DAG.
- `extract`: Extracts data and returns a random number to simulate data count.
- `branch_task`: Directs the flow of execution based on the extracted data.
- `transform1`: Transformation task when extracted data exceeds a threshold.
- `predict_lost_data`: Predicts lost data if extraction returns a lower value.
- `transform2`: Simulates a secondary transformation step.
- `ingest`: Ingests data into a database.
- `end`: Marks the end of the DAG.

## Dag_Analitica_MKT

This DAG handles marketing analytics with the use of an external task sensor to wait for the successful execution of a task from another DAG before proceeding.

- **Start Date**: July 25, 2024
- **Description**: Dag de Analítica y sensor
- **Tags**: Ingeniería
- **Schedule Interval**: Daily

### Tasks:
- `start`: Marks the beginning of the DAG.
- `sensor_DB_Ventas_Raw`: Waits for the successful completion of the `transform2` task from the `DG_Ventas` DAG.
- `mkt_data`: Placeholder task for marketing data extraction.
- `join_transform`: Joins and transforms data for further analysis.
- `ingest`: Simulates data ingestion into a database.
- `end`: Marks the end of the DAG.

## Dag_Ventas

This DAG simulates a sales data processing pipeline. It performs dummy transformations and ingests the data into multiple targets.

- **Start Date**: July 25, 2024
- **Description**: Dag de ventas
- **Tags**: Ingeniería
- **Schedule Interval**: Daily

### Tasks:
- `start`: Marks the beginning of the DAG.
- `extract`: Dummy task simulating data extraction.
- `transform1`: First transformation step.
- `transform2`: Executes a Bash command to simulate a transformation.
- `ingest1`: First ingestion task.
- `ingest2`: Second ingestion task.
- `end`: Marks the end of the DAG.

## DAG_ETL_Dummy

This ETL DAG is a dummy implementation of an ETL pipeline that extracts data from two sources, joins them, and ingests the result into a PostgreSQL database.

- **Start Date**: Not specified
- **Description**: Creación de DAG ETL Dummy
- **Tags**: ETL, Ingeniería
- **Schedule Interval**: None (manual trigger)

### Tasks:
- `get_api_bash`: Simulates an API call using a Bash command.
- `get_api_python`: Simulates an API call using Python.
- `join_trans`: Joins and transforms the data from both sources.
- `load_postgresSQL`: Ingests the data into a PostgreSQL database.

## DAG_ETL_Postgres

This ETL DAG extracts data from an API, joins it with data from a second source, and loads the transformed result into a PostgreSQL database. It includes an SQL operation to check the table structure before loading the data.

- **Start Date**: Not specified
- **Description**: Creación de DAG ETL PostgreSQL
- **Tags**: ETL, Ingeniería, PostgreSQL
- **Schedule Interval**: None (manual trigger)

### Tasks:
- `get_api_python`: Extracts data from an API using a Python script.
- `get_api_bash`: Extracts data from an API using a Bash command.
- `join_trans`: Joins and transforms the data from both extraction tasks.
- `check_table`: Verifies the existence of the target table in the PostgreSQL database.
- `load_data`: Loads the transformed data into the PostgreSQL database.

# Documentación de DAGs - Proyecto ETL Airflow

Este documento describe los distintos DAGs (Directed Acyclic Graphs) implementados en Airflow para realizar tareas de extracción, transformación y carga (ETL) en diferentes sistemas.

## 1. DAG: MSPM_Dag

### Descripción
Este DAG ejecuta un flujo de monitoreo de sensores en una planta de manufactura. Se ejecuta cada hora.

### Configuración General
- **Nombre del DAG**: `MSPM_Dag`
- **Owner**: Codigo Facilito Team
- **Schedule**: @hourly
- **Fecha de Inicio**: 25 de julio de 2024
- **Retries**: 1
- **Retry Delay**: 2 minutos
- **Tags**: ['Ingenieria']

### Tareas

1. **start**: Marca el inicio del flujo de trabajo.
2. **extract_sensor_data**: Agrupación de tareas para extraer datos de 30 sensores. Cada sensor ejecuta una función Python que imprime un mensaje de extracción.
3. **ingest_db**: Ingresa los datos extraídos a la base de datos.
4. **trans_in_db_analisis**: Realiza una transformación de datos para análisis.
5. **email_supervisores**: Envía un correo a los supervisores con el estado de los sensores.
6. **email_mantenimiento**: Envía un correo al equipo de mantenimiento.
7. **update_dash_mantenimiento**: Actualiza el dashboard de mantenimiento.
8. **update_dash_produccion**: Actualiza el dashboard de producción.
9. **end**: Marca el fin del flujo de trabajo.

### Flujo de Ejecución

```mermaid
graph LR
    start --> extract_sensor_data --> ingest_db --> trans_in_db_analisis --> email_supervisores --> end
    trans_in_db_analisis --> email_mantenimiento --> end
    trans_in_db_analisis --> update_dash_mantenimiento --> end
    trans_in_db_analisis --> update_dash_produccion --> end


