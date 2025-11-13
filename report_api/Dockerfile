FROM python:3.9-slim
USER root

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /requirements.txt