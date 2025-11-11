from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from airflow import DAG
from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.operators.python import PythonOperator
from datetime import datetime
# import psycopg2
# import clickhouse_connect
# import time

# def extract_from_postgres():
#     POSTGRES_CONN = {
#         "dbname": "crm",
#         "user": "crm_user",
#         "password": "crm_pass",
#         "host": "crm_db",
#         "port": 5434,
#     }
#     conn = psycopg2.connect(**POSTGRES_CONN)
#     cur = conn.cursor()
#     cur.execute("""
#         select t.timestamp, t.value, s.id, s.type, prod.id, prod.type, pers.id,
#                pers.last_name, pers.first_name, pers.patronymic, pers.birthday
#         from telemetry t
#         inner join sensor s on s.id = t.sensor_id
#         inner join product prod on prod.id = s.product_id
#         inner join person pers on pers.id = prod.person_id
#     """)
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#     return rows
#
# def upsert_to_clickhouse(ti):
#     CLICKHOUSE_CONN = {
#         "host": "clickhouse-server",
#         "port": 9000,
#         "username": "clickhouse",
#         "password": "clickhouse",
#     }
#     rows = ti.xcom_pull(task_ids="extract")
#     client = clickhouse_connect.get_client(**CLICKHOUSE_CONN)
#     version = int(time.time())
#     enriched = [tuple(r) + (version,) for r in rows]  # добавляем версию
#     client.insert(
#         "report",
#         enriched,
#         column_names=[
#             "sensor_id", "sensor_name", "timestamp", "value", "product_id", "product_name",
#             "person_id", "last_name", "first_name", "patronymic", "version"
#         ],
#     )

with DAG(
    dag_id="crm_to_clickhouse",
    start_date=datetime(2025, 11, 11),
    schedule="@hourly",
    catchup=False,
    tags=["etl", "clickhouse", "crm"]
) as dag:
    extract = SQLExecuteQueryOperator(
        task_id="extract",
        conn_id="postgres_conn",
        # python_callable=extract_from_postgres,
        sql="""
            select t.timestamp, t.value, s.id, s.type, prod.id, prod.type, pers.id, 
                   pers.last_name, pers.first_name, pers.patronymic, pers.birthday
            from telemetry t
            inner join sensor s on s.id = t.sensor_id
            inner join product prod on prod.id = s.product_id
            inner join person pers on pers.id = prod.person_id
            """
    )

    load = ClickHouseOperator(
        task_id="upsert",
        clickhouse_conn_id="clickhouse_conn",
        # python_callable=upsert_to_clickhouse,
        sql="select * from report"
    )

    extract >> load