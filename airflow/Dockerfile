FROM apache/airflow:3.1.2-python3.11
USER root

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN python3 -m venv myenv
RUN source myenv/bin/activate
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /requirements.txt