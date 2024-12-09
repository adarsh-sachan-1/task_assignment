FROM python:3.10.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN apt-get update
RUN pip install -r requirements.txt
WORKDIR /usr/src/app