import random
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook


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
    rows = [f'insert into telemetry (sensor_id, timestamp, value) values ({", ".join(d)})' for d in data]
    ClickHouseHook(clickhouse_conn_id="clickhouse_connection").execute(rows)

with DAG("telemetry_etl", schedule=timedelta(minutes=1), catchup=False, start_date=(datetime.now() + timedelta(seconds=30))):
    ids = extract_sensor_id()
    data = generate(ids)
    load(data)