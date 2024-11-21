FROM python:3.4

WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
