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
    patronymic String,
    birthday String,
    email String
)
ENGINE = ReplacingMergeTree()
partition by toYYYYMM(timestamp)
order by (email, sensor_id, timestamp)