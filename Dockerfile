FROM python:3.10-alpine3.17
LABEL maintainer="Inseyab"

ENV PYTHONUNBUFFERED=1


EXPOSE 8000

ARG DEV=false

# Install neccessory Packages for building wheel of python
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev linux-headers

# Copy requirements for dev and prod
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Install packages
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt

# Install development packages if DEV=true in docker-compose
RUN if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi

# Remove temporary files
RUN rm -rf /tmp
RUN apk del .tmp-build-deps

# Create a non-root user
RUN adduser --disabled-password --no-create-home django-user

COPY ./scripts /scripts

# Create directories for static and media files & set permissions
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN chown -R django-user:django-user /vol
RUN chmod -R 755 /vol && chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

COPY ./app /app
WORKDIR /app
RUN chown -R django-user:django-user /app


USER django-user

# CMD ["run.sh"]