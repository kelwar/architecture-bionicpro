import random
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook


with DAG("telemetry_etl", schedule=timedelta(minutes=1), catchup=False, start_date=(datetime.now() + timedelta(seconds=30))):
    @task
    def extract_sensor_id() -> list[int]:
        return (PostgresHook(conn_id="crm_db_connection")
                .get_records("select id from sensor;"))

    @task
    def generate(ids: list[int]):
        length = len(ids)
        rows = []
        for _ in range(5):
            now = datetime.now()
            rows.append(tuple([
                ids[random.randint(0, length)],
                datetime.fromtimestamp(random.uniform((now - timedelta(minutes=1)).timestamp(), now.timestamp())),
                random.random()
            ]))
        return rows

    @task
    def load(data):
        rows = [f'insert into telemetry (sensor_id, timestamp, value) values ({d[0]}, {d[1]}, {d[2]})' for d in data]
        ClickHouseHook(clickhouse_conn_id="clickhouse_connection").execute(rows)


    ids = extract_sensor_id()
    data = generate(ids)
    load(data)