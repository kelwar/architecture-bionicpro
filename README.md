Путь к файлу диаграммы (задания 1 и 2): ./BionicPRO_C4_model.drawio.xml

Настройка проекта:
1. Запустить docker-compose up -d.
2. В airflow-webserver (http://localhost:8081) Admin -> Connections -> Add. Добавить 3 соединения:
- crm_db_connection, Postgres, crm-db, crm, crm_user, crm_pass, 5432
- clickhouse_connection, Generic, clickhouse-server, clickhouse, clickhouse, 9000
- clickhouse_http_connection, Generic, clickhouse-server, clickhouse, clickhouse, 8123
3. Запустить DAG init_tables - он проинициализирует таблицы телеметрии и отчёта.
4. Запустить любое количество раз telemetry_etl - будут сгенерированы псевдоданные с "датчиков".
5. Запустить report_etl - в отчёт будут собраны данные телеметрии вместе с метаданными датчиков, изделий и пользователей.
6. Нажатие кнопки загружает данные отчёта по авторизованному пользователю.