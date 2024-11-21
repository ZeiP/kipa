FROM python:3.4

WORKDIR /app/web

ENTRYPOINT ["/app/docker-entrypoint.sh"]
EXPOSE 3000
CMD ["python", "./manage.py", "runserver", "0.0.0.0:3000"]

COPY . /app/
COPY web/settings/docker.py.example /app/web/settings/docker.py
RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt
