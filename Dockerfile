FROM python:2

WORKDIR /app/web

RUN echo "PYTHONPATH=/usr/local/lib/python2.7/site-packages" | tee -a /etc/profile
ENTRYPOINT ["/app/docker-entrypoint.sh"]
EXPOSE 3000
CMD ["python", "./manage.py", "runserver", "0.0.0.0:3000"]

COPY . /app/
COPY web/settings/docker.py.example /app/web/settings/docker.py
RUN pip install -r /app/requirements.txt
