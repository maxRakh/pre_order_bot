FROM python:3.9-alpine3.17

COPY requirements.txt service/requirements.txt

RUN apk add --update alpine-sdk

RUN apk add postgresql-client build-base postgresql-dev libffi-dev

RUN pip install --upgrade pip

RUN pip install -r service/requirements.txt

COPY ./ /service

WORKDIR /service

EXPOSE 8000

RUN adduser --disabled-password service-user

USER service-user