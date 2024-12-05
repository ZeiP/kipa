FROM ubuntu/nginx:1.24-24.04_beta

RUN apt-get update \
    && apt-get install -y python3.12 python3.12-venv \
    && apt-get clean

COPY web /app/
COPY --chown=nobody:nogroup web/media /media
COPY web/settings/docker.py.example /app/settings/docker.py
COPY requirements.txt /
COPY nginx.conf /etc/nginx/

RUN python3.12 -m venv venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /app

RUN rm -rf /app/media \
    && mkdir /db \
    && pip install -r /requirements.txt \
    && tr -dc A-Za-z0-9 < /dev/urandom | head -c 40 > /secret.txt \
    && python manage.py makemigrations tupa \
    && python manage.py migrate \
    && nginx -t \
    && echo "gunicorn --daemon --bind unix:/tmp/kipa.sock wsgi --error-logfile /tmp/errors " > /docker-entrypoint.d/gunicorn.sh \
    && chmod +x /docker-entrypoint.d/gunicorn.sh \
