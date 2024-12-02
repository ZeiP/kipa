FROM python:3.3

WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN pip install --trusted-host pypi.python.org -r /requirements.txt
