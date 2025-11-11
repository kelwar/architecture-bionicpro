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