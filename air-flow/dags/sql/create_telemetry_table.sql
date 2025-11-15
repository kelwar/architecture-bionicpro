create table if not exists telemetry (
    sensor_id Int64,
    timestamp Datetime,
    value Decimal(15,5)
)
ENGINE = ReplacingMergeTree()
partition by toYYYYMM(timestamp)
order by (sensor_id, timestamp)