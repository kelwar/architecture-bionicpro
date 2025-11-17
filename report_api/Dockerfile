FROM python:3.11-slim
USER root

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall JWT
RUN pip install PyJWT

EXPOSE 8000

CMD ["uvicorn", "report_api:app", "--host", "0.0.0.0"]
