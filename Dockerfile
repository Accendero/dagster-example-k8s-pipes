FROM python:3.11-slim

RUN pip install dagster-pipes boto3 click

COPY containerized_script.py .
