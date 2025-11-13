create table if not exists report (
    sensor_id Int64,
    sensor_type String,
    timestamp DateTime,
    value Decimal(15,5),
    product_id Int64,
    product_type String,
    person_id Int64,
    last_name String,
    first_name String,
    patronymic String
)
ENGINE = ReplacingMergeTree
partition by toDate(timestamp)
order by (sensor_id, timestamp)