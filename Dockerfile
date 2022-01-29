FROM python:3.6-alpine3.7

ENV BASE_DIR=/app/ \
    STATIC_ROOT=/app/code/static/ \
    APP_DIR=/app/code/ \
    APP_USER=webapp \
    PATH=$PATH:/root/.local/bin \
    DJANGO_SETTINGS_MODULE=conf.settings.local

WORKDIR $APP_DIR

RUN apk add --no-cache imagemagick zlib-dev jpeg-dev build-base postgresql-dev tzdata && \
    cp "/usr/share/zoneinfo/$TZ" /etc/localtime && \
    apk add --no-cache git gcc libc-dev --virtual build && \
    mkdir $APP_DIR $MEDIA_ROOT $STATIC_ROOT -p && \
    addgroup -S $APP_USER && \
    adduser -D -S $APP_USER $APP_USER && \
    chown $APP_USER:$APP_USER -R $BASE_DIR /home/$APP_USER && \
    pip install pipenv && \
    apk del --no-cache build

USER $APP_USER

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --dev

COPY conf conf/
COPY bigtomato bigtomato/
COPY manage.py manage.py

EXPOSE 8000

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
