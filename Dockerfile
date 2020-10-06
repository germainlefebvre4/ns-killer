FROM python:3.7-alpine AS base

COPY requirements.txt .
RUN pip install -r requirements.txt


# Python libs and sources

COPY main.py .

CMD ["python", "main.py"]
