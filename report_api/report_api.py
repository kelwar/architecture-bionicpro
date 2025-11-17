import os
from typing import Annotated

import clickhouse_connect
import jwt
from fastapi import FastAPI, Header
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3000/"],
    allow_credentials=True,  # Set to True if your frontend sends cookies or authorization headers
    allow_methods=["*"],     # Or specify specific methods like ["GET", "POST"]
    allow_headers=["*"],     # Or specify specific headers
)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/reports")
async def getReport(authorization: Annotated[str | None, Header()]):
    token = str.replace(authorization, "Bearer ", "")
    user_info = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"], options={"verify_signature": False})
    email = user_info.get("email")
    print(f"email: {email}")

    client = clickhouse_connect.get_client(host=os.getenv("CLICKHOUSE_HOST"), port=int(os.getenv("CLICKHOUSE_PORT")),
                                           username=os.getenv("CLICKHOUSE_USER"), password=os.getenv("CLICKHOUSE_PASS"))
    result = client.query(query='SELECT * FROM report WHERE email = %(email)s', parameters={"email": email})
    return [{"sensor_id": r[0], "sensor_type": r[1], "timestamp": r[2], "value": r[3],
             "product_id": r[4], "product_type": r[5], "person_id": r[6], "last_name": r[7], "first_name": r[8], "patronymic": r[9],
             "birthday": r[10], "email": r[11]} for r in result.result_rows]