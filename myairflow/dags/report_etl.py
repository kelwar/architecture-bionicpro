from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook


with DAG("report_etl", schedule=timedelta(minutes=1), catchup=False, start_date=(datetime.now() + timedelta(minutes=1))) as dag:
    @task
    def extract_telemetry():
        timestamp = datetime.fromtimestamp((datetime.now() - timedelta(minutes=1)).timestamp())
        return (ClickHouseHook(clickhouse_conn_id="clickhouse_connection")
                .get_conn().execute(query="select sensor_id, timestamp, value from telemetry where timestamp >= ?", params=timestamp))

    @task
    def extract_ids(telemetry: list[any]) -> set[int]:
        return set([row[0] for row in telemetry])

    @task
    def extract_metadata(ids: set[int]) -> dict[int, any]:
        hook = PostgresHook(conn_id="crm_db_connection")
        rows = hook.get_records(sql="./sql/read_sensor_metadata.sql", parameters=ids)
        data = dict()
        for row in rows:
            data[row[0]] = row
        return data

    @task
    def enrich(telemetry, metadata):
        sensor_data = []
        for t in telemetry:
            d = metadata[t[0]]
            sensor_data.append(tuple([d[0], d[1], t[1], t[2], d[2], d[3], d[4], d[5], d[6], d[7], d[8]]))
        return sensor_data

    @task
    def load(data):
        rows = ",\n".join([", ".join(d) for d in data])
        sql = f'insert into report (sensor_id, sensor_type, timestamp, value, product_id, product_type, person_id, last_name, first_name, patronymic, birthday) values ({rows})'
        ClickHouseHook(clickhouse_conn_id="clickhouse_connection").execute(sql)


    telemetry = extract_telemetry()
    sensor_ids = extract_ids(telemetry)
    sensor_metadata = extract_metadata(sensor_ids)
    enriched_data = enrich(telemetry, sensor_metadata)
    load(enriched_data)