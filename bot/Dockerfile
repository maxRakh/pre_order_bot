FROM python:3.9-alpine3.17

COPY requirements_bot.txt bot/requirements_bot.txt

RUN apk add --update alpine-sdk

RUN pip install --upgrade pip

RUN pip install -r bot/requirements_bot.txt

COPY ./ /bot

WORKDIR /bot

CMD python main.py

