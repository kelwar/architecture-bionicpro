from typing import Annotated

import clickhouse_connect
from fastapi import FastAPI, Header
import jwt

def getClient():
    return clickhouse_connect.get_client(host='clickhouse-server', port=8123, username='clickhouse', password='clickhouse')

app = FastAPI()

@app.get("/reports")
def getReport(token: Annotated[str | None, Header()]):
    payload = jwt.decode(token, "kjfaeuswy3rrbfu32f982bf4398453b4tg98r3h", algorithms="HS256")
    person_id = payload.get("person_id")

    client = getClient()
    result = client.query(query='SELECT * FROM report WHERE person_id = %(person_id)s',
                          parameters={ "person_id": person_id })
    return result