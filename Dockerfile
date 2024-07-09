FROM python:3.11.1-slim

RUN mkdir /src

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1

# for setting python output directly to the terminal with out buffering
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .
