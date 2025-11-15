from datetime import datetime

from airflow import DAG
from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator

with DAG("init_tables", schedule="@once", catchup=False, start_date=datetime.now()):
    init_telemetry = ClickHouseOperator(
        task_id="init_telemetry",
        clickhouse_conn_id="clickhouse_connection",
        sql="./sql/create_telemetry_table.sql"
    )

    init_report = ClickHouseOperator(
        task_id="init_report",
        clickhouse_conn_id="clickhouse_connection",
        sql="./sql/create_report_table.sql"
    )

    init_telemetry >> init_report
