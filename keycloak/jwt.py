import jwt, datetime

secret = "kjfaeuswy3rrbfu32f982bf4398453b4tg98r3h"

payload = {
    "person_id": 1,
    "sub": "23345",
    "name": "Иван Петров",
    "iss": "https://google.com",
    "aud": "report-service",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
}

token = jwt.encode(payload, secret, algorithm="HS256")
print(token)