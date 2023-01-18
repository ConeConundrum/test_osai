FROM python:3.10.9 as pip-installed

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

FROM pip-installed
COPY . .

RUN  chmod +x scripts/*.sh && \
     mv scripts/* ./
