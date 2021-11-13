FROM python:3.10-slim

WORKDIR /app/
COPY ./ /app/

RUN apt-get update && apt-get -y install libhidapi-libusb0
RUN pip install --upgrade pip && pip install -r requirements.txt
