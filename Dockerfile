FROM python:3.10-alpine3.17
LABEL maintainer="Inseyab"

ENV PYTHONUNBUFFERED=1


EXPOSE 8000

ARG DEV=false
RUN apk update
# Install neccessory Packages for building wheel of python
RUN apk add --update --no-cache jpeg-dev libstdc++ openssl1.1-compat
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    build-base unixodbc-dev musl-dev zlib zlib-dev linux-headers curl

# Install the Microsoft ODBC driver Linux.Follow the mssql documentation: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.8.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.8.1.1-1_amd64.apk

# Install the package(s)
RUN apk add --allow-untrusted msodbcsql17_17.8.1.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.8.1.1-1_amd64.apk

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

CMD ["run.sh"]