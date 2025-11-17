from collections import namedtuple
from datetime import datetime

import clickhouse_connect
from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook

with DAG("report_etl", schedule="@hourly", catchup=False, start_date=datetime(2025, 11, 11)) as dag:
    @task
    def read_last_timestamp():
        hook = ClickHouseHook(clickhouse_conn_id="clickhouse_connection")
        result: list[datetime] = hook.execute(sql="select timestamp from report order by timestamp desc limit 1")
        return result[0] if len(result) != 0 else None

    @task
    def extract_telemetry(timestamp) -> list[any]:
        print(f"timestamp: {timestamp}")
        hook = ClickHouseHook(clickhouse_conn_id="clickhouse_connection")
        return hook.execute(sql="select * from telemetry where %(timestamp)s is null or timestamp >= %(timestamp)s",
                            params={"timestamp": timestamp})

    @task
    def extract_ids(telemetry: list[any]) -> tuple[int, ...]:
        print(f"telemetry: {telemetry}")
        return tuple(set([row[0] for row in telemetry]))

    @task(multiple_outputs=False)
    def extract_metadata(ids: tuple[int, ...]) -> list[any]:
        print(f"ids: {ids}")
        if len(ids) == 0:
            return []

        hook = PostgresHook(postgres_conn_id="crm_db_connection")
        return hook.get_records(sql="""
            select s.id as sensor_id, s.type as sensor_type, prod.id as product_id, prod.type as product_type,
                   pers.id as person_id, pers.last_name as last_name, pers.first_name as first_name, 
                   pers.patronymic as patronymic, pers.birthday as birthday, pers.email as email
            from sensor s
            inner join product prod on prod.id = s.product_id
            inner join person pers on pers.id = prod.person_id
            where s.id in %(ids)s;
            """,
            parameters={"ids": ids})

    @task
    def enrich(telemetry, metadata):
        print(f"telemetry: {telemetry}")

        data = dict()
        for row in metadata:
            data[row[0]] = row

        Report = namedtuple("Report", ["sensor_id", "sensor_type", "timestamp", "value",
                                       "product_id", "product_type", "person_id", "last_name", "first_name",
                                       "patronymic", "birthday", "email"])

        print(f"metadata: {data}")
        sensor_data = []
        for t in telemetry:
            d = data[t[0]]
            sensor_data.append(Report(d[0], d[1], t[1], t[2], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9]))
        return sensor_data

    @task
    def load(data):
        print(f"load: {data}")
        conn = ClickHouseHook(clickhouse_conn_id="clickhouse_connection").get_connection(conn_id="clickhouse_http_connection")
        client = clickhouse_connect.get_client(host=conn.host, port=conn.port, user=conn.login, password=conn.password)
        try:
            client.insert("report", data)
        finally:
            client.close()


    last_timestamp = read_last_timestamp()
    telemetry = extract_telemetry(last_timestamp)
    sensor_ids = extract_ids(telemetry)
    sensor_metadata = extract_metadata(sensor_ids)
    enriched_data = enrich(telemetry, sensor_metadata)
    load(enriched_data)