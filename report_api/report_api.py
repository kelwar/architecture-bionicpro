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
    print(f"Authorization: {authorization}")
    token = str.replace(authorization, "Bearer ", "")
    print(f"token: {token}")
    user_info = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"], options={"verify_signature": False})
    print(f"user: {user_info}")
    email = user_info.get("email")
    print(f"email: {email}")

    client = clickhouse_connect.get_client(host=os.getenv("CLICKHOUSE_HOST"), port=int(os.getenv("CLICKHOUSE_PORT")),
                                           username=os.getenv("CLICKHOUSE_USER"), password=os.getenv("CLICKHOUSE_PASS"))
    result = client.query(query='SELECT * FROM report WHERE email = %(email)s',
                          parameters={"email": email})
    return result