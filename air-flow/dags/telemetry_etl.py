import random
from datetime import datetime, timedelta

import clickhouse_connect
from airflow import DAG
from airflow.operators.python import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook


@task
def extract_sensor_id() -> list[int]:
    ids = PostgresHook(postgres_conn_id="crm_db_connection").get_records(sql="select id from sensor")
    return [id[0] for id in ids]

@task
def generate(ids: list[int]):
    print(f'{ids}')
    length = len(ids)
    rows = []
    for _ in range(5):
        now = datetime.now()
        rows.append([
            ids[random.randint(0, length - 1)],
            datetime.fromtimestamp(random.uniform((now - timedelta(minutes=1)).timestamp(), now.timestamp())),
            random.random()
        ])
    return rows

@task
def load(data):
    # Telemetry = namedtuple("Telemetry", ["sensor_id", "timestamp", "value"])
    # data = [Telemetry(int(d[0]), d[1], float(d[2])) for d in data]
    # sql = 'insert into telemetry (sensor_id, timestamp, value) values (%d, %t, %f)'
    conn = ClickHouseHook(clickhouse_conn_id="clickhouse_connection").get_connection(conn_id="clickhouse_http_connection")
    client = clickhouse_connect.get_client(host=conn.host, port=conn.port, user=conn.login, password=conn.password)
    try:
        client.insert("telemetry", data)
    finally:
        client.close()
    # for d in data:
    #     print(d)
    #     hook.execute(sql=sql, params=[d.sensor_id, d.timestamp, d.value])

with DAG("telemetry_etl", schedule="@hourly", catchup=False, start_date=datetime(2025, 11, 11)):
    ids = extract_sensor_id()
    data = generate(ids)
    load(data)