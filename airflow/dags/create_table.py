# from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator

from airflow import DAG
# from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator
# import clickhouse_connect
from datetime import datetime
# from pathlib import Path

# def get_client():
#     return clickhouse_connect.get_client(host='localhost', port=8123, username='clickhouse', password='clickhouse')

# def run_sql_from_file():
#     # client = get_client()
#     sql_path = Path(__file__).resolve().parents[1] / "/sql/create_data.sql"
#     with open(sql_path, "r", encoding="utf-8") as f:
#         query = f.read()
#     # client.command(query)
#     return query

with DAG(
    dag_id="create_table",
    start_date=datetime(2025, 11, 11),
    schedule="@once",
    catchup=False,
    tags=["clickhouse", "init", "etl"]
) as dag:
    t1 = ClickHouseOperator(
        task_id="create_tables",
        # python_callable=create_tables,
        clickhouse_conn_id="clickhouse_conn",
        sql="""
            create table if not exists report
            (
                sensor_id UInt64,
                sensor_name String,
                timestamp String,
                value Int64,
                product_id UInt64,
                product_name String,
                person_id UInt64,
                last_name String,
                first_name String,
                patronymic String,
                version UInt64
            )
            engine = ReplacingMergeTree(version)
            order by (sensor_name, timestamp);
            """
    )