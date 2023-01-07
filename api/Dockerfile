FROM python:3.11.1-slim-buster

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt
COPY dist/invoicer_api-0.0.1-py3-none-any.whl /app/invoicer_api-0.0.1-py3-none-any.whl

RUN apt-get update -y
RUN apt-get install \
    gcc \
    libssl-dev \
    libpcre3 \
    libpcre3-dev \
    -y # gcc required to build uwsgi
RUN pip install -r requirements.txt --compile
RUN pip install invoicer_api-0.0.1-py3-none-any.whl --no-deps --compile

CMD uwsgi \
    --socket 0.0.0.0:5001 \
    --protocol http \
    --module invoicer_api.app:app \
    --python-path ./venv/bin/python \
    --https =0,/ssl/fullchain.pem,/ssl/privkey.pem,HIGH
