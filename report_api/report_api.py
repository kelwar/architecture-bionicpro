import os
from typing import Annotated

import clickhouse_connect
import jwt
from fastapi import FastAPI, Header
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/reports")
def getReport(token: Annotated[str | None, Header()]):
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms="HS256")
    person_id = payload.get("person_id")
    print(f"person_id: {person_id}")

    client = clickhouse_connect.get_client(host=os.getenv("CLICKHOUSE_HOST"), port=int(os.getenv("CLICKHOUSE_PORT")),
                                           username=os.getenv("CLICKHOUSE_USER"), password=os.getenv("CLICKHOUSE_PASS"))
    result = client.query(query='SELECT * FROM report WHERE person_id = %(person_id)s',
                          parameters={"person_id": person_id})
    return result