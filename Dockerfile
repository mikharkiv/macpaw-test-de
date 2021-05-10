# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /macpaw-test
COPY requirements.txt /macpaw-test/
RUN pip install --no-cache-dir -r requirements.txt
COPY /src /macpaw-test/
COPY .flake8 /macpaw-test/
COPY config.ini /macpaw-test/
COPY pytest.ini /macpaw-test/
COPY .dockerignore /macpaw-test/
