import os
from typing import Annotated

import clickhouse_connect
from fastapi import FastAPI, Header
import jwt
# import traceback

app = FastAPI()
print(f"app: {app}")

@app.get("/reports")
def getReport(token: Annotated[str | None, Header()]):
    try:
        payload = jwt.decode(token, "kjfaeuswy3rrbfu32f982bf4398453b4tg98r3h", algorithms="HS256")
        person_id = payload.get("person_id")

        client = clickhouse_connect.get_client(host=os.getenv("CLICKHOUSE_HOST"), port=int(os.getenv("CLICKHOUSE_PORT")),
                                               username=os.getenv("CLICKHOUSE_USER"), password=os.getenv("CLICKHOUSE_PASS"))
        result = client.query(query='SELECT * FROM report WHERE person_id = %(person_id)s',
                              parameters={ "person_id": person_id })
        return result
    except Exception:
        print("Exception")
        # traceback.print_exc()