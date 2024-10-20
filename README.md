# Documentación del DAG de Airflow

## ARSMM_Dag

Este DAG es responsable del análisis de redes sociales para una marca de moda. Extrae datos de las APIs de Facebook, Twitter e Instagram, realiza una transformación para unir los datos, aplica un modelo de NLP preentrenado e ingresa los resultados en una base de datos.

- **Fecha de Inicio**: 1 de enero de 2024
- **Descripción**: Dag de Análisis de Redes Sociales para una Marca de Moda
- **Etiquetas**: Ingeniería
- **Intervalo de Programación**: Ninguno (activación manual)

### Tareas:
- extrac_facebook_api: Simula la extracción de datos desde la API de Facebook.
- extrac_tw_api: Simula la extracción de datos desde la API de Twitter.
- extrac_instagram_api: Simula la extracción de datos desde la API de Instagram.
- trans_join_data: Tarea de transformación ficticia para unir los datos de las tres plataformas.
- consumo_modelo_nlp: Simula el consumo de un modelo de NLP para análisis adicional.
- ingest_db: Simula la ingesta de los datos procesados en una base de datos.

## Dag_Branch

Este DAG simula un pipeline de análisis de ventas con lógica de bifurcación basada en los datos extraídos. Si los datos extraídos superan un umbral, se transforman; de lo contrario, se predicen los datos perdidos.

- **Fecha de Inicio**: 1 de julio de 2024
- **Descripción**: Dag de ventas
- **Etiquetas**: Ingeniería
- **Intervalo de Programación**: Diario

### Tareas:
- start: Marca el inicio del DAG.
- extract: Extrae datos y devuelve un número aleatorio para simular el conteo de datos.
- branch_task: Dirige el flujo de ejecución según los datos extraídos.
- transform1: Tarea de transformación cuando los datos extraídos superan un umbral.
- predict_lost_data: Predice datos perdidos si la extracción devuelve un valor bajo.
- transform2: Simula un segundo paso de transformación.
- ingest: Ingresa los datos en una base de datos.
- end: Marca el final del DAG.

## Dag_Analitica_MKT

Este DAG maneja la analítica de marketing con el uso de un sensor de tarea externa que espera la ejecución exitosa de una tarea de otro DAG antes de continuar.

- **Fecha de Inicio**: 25 de julio de 2024
- **Descripción**: Dag de Analítica y sensor
- **Etiquetas**: Ingeniería
- **Intervalo de Programación**: Diario

### Tareas:
- start: Marca el inicio del DAG.
- sensor_DB_Ventas_Raw: Espera la finalización exitosa de la tarea transform2 del DAG DG_Ventas.
- mkt_data: Tarea reservada para la extracción de datos de marketing.
- join_transform: Une y transforma los datos para análisis adicional.
- ingest: Simula la ingesta de datos en una base de datos.
- end: Marca el final del DAG.

## Dag_Ventas

Este DAG simula un pipeline de procesamiento de datos de ventas. Realiza transformaciones ficticias y los datos son ingresados en múltiples destinos.

- **Fecha de Inicio**: 25 de julio de 2024
- **Descripción**: Dag de ventas
- **Etiquetas**: Ingeniería
- **Intervalo de Programación**: Diario

### Tareas:
- start: Marca el inicio del DAG.
- extract: Tarea ficticia que simula la extracción de datos.
- transform1: Primer paso de transformación.
- transform2: Ejecuta un comando Bash para simular una transformación.
- ingest1: Primera tarea de ingesta.
- ingest2: Segunda tarea de ingesta.
- end: Marca el final del DAG.

## DAG_ETL_Dummy

Este DAG ETL es una implementación ficticia de un pipeline ETL que extrae datos de dos fuentes, los une e ingresa el resultado en una base de datos PostgreSQL.

- **Fecha de Inicio**: No especificada
- **Descripción**: Creación de DAG ETL Dummy
- **Etiquetas**: ETL, Ingeniería
- **Intervalo de Programación**: Ninguno (activación manual)

### Tareas:
- get_api_bash: Simula una llamada a API usando un comando Bash.
- get_api_python: Simula una llamada a API usando Python.
- join_trans: Une y transforma los datos de ambas fuentes.
- load_postgresSQL: Ingresa los datos en una base de datos PostgreSQL.

## DAG_ETL_Postgres

Este DAG ETL extrae datos de una API, los une con datos de una segunda fuente y carga el resultado transformado en una base de datos PostgreSQL. Incluye una operación SQL para verificar la estructura de la tabla antes de cargar los datos.

- **Fecha de Inicio**: No especificada
- **Descripción**: Creación de DAG ETL PostgreSQL
- **Etiquetas**: ETL, Ingeniería, PostgreSQL
- **Intervalo de Programación**: Ninguno (activación manual)

### Tareas:
- get_api_python: Extrae datos de una API usando un script en Python.
- get_api_bash: Extrae datos de una API usando un comando Bash.
- join_trans: Une y transforma los datos de ambas tareas de extracción.
- check_table: Verifica la existencia de la tabla destino en la base de datos PostgreSQL.
- load_data: Carga los datos transformados en la base de datos PostgreSQL.

## MSPM_Dag

Este DAG realiza el monitoreo de sensores para una planta de manufactura. Extrae datos de 30 sensores y envía alertas y actualizaciones de dashboards.

- **Fecha de Inicio**: 25 de julio de 2024
- **Descripción**: Dag de Monitoreo de Sensores para una Planta de Manufactura
- **Etiquetas**: Ingeniería
- **Intervalo de Programación**: Cada hora

### Tareas:
- `start`: Marca el inicio del DAG.
- `extract_sensor_data`: Extrae datos de 30 sensores.
- `ingest_db`: Ingresa los datos en una base de datos.
- `trans_in_db_analisis`: Realiza un análisis dentro de la base de datos.
- `email_supervisores`: Envía un correo electrónico a los supervisores.
- `email_mantenimiento`: Envía un correo electrónico al equipo de mantenimiento.
- `update_dash_mantenimiento`: Actualiza el dashboard de mantenimiento.
- `update_dash_produccion`: Actualiza el dashboard de producción.
- `end`: Marca el final del DAG.

---

## SRP_Dag

Este DAG implementa un sistema de recomendación de películas. Extrae datos de bases de datos internas y APIs externas, los combina y pasa el resultado a un modelo de machine learning.

- **Fecha de Inicio**: 1 de enero de 2024
- **Descripción**: Dag de Sistema de Recomendación de Películas
- **Etiquetas**: Ingeniería
- **Intervalo de Programación**: Mensual

### Tareas:
- `extrac_db_inter`: Extrae datos de bases de datos internas.
- `extrac_api`: Extrae datos de una API externa.
- `trans_join_data`: Combina y transforma los datos.
- `consumo_modelo_ml_api`: Consume un modelo de machine learning para generar recomendaciones.
- `send_email`: Envía correos con los resultados.
- `ingest_db`: Ingresa los resultados en una base de datos.

## DAG: Marketing_ETL_DAG

Este DAG maneja la extracción, transformación y carga (ETL) de datos de diversas plataformas de marketing (Google Ads, Facebook Ads, YouTube Ads) hacia Google Cloud Storage (GCS) y BigQuery.

- **Fecha de Inicio**: `None`
- **Descripción**: `Dag de Marketing ETL`
- **Etiquetas**: `Ingeniería`, `Marketing`
- **Plataformas de Datos**:
  - Google Ads
  - Facebook Ads
  - YouTube Ads
- **Procesos**:
  1. Extracción de datos desde las plataformas de marketing.
  2. Transformación y limpieza de los datos.
  3. Carga de los datos en GCS.
  4. Almacenamiento de los resultados finales en BigQuery.
- **Dependencias**:
  - Google Cloud SDK
  - BigQuery API
  - Cloud Storage API
- **Frecuencia de Ejecución**: Diaria
- **Ubicación del código**: `./dags/Marketing_ETL_DAG.py`

---
