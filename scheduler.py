from datetime import datetime

from loguru import logger
from prometheus_client import Gauge, start_http_server
import time
import schedule
from pymongo import MongoClient

from co2meter import CO2monitor
from schema import AirRecord
from settings import settings

mon = CO2monitor()
co2_gauge = Gauge('CO2_ppm', 'CO2 in ppm')
temp_gauge = Gauge('Temperature', 'Temperature in Celsius')


mongodb_url = 'mongodb://{0}:{1}@{2}:{3}'.format(
    settings.mongodb_username,
    settings.mongodb_password,
    settings.mongodb_host,
    settings.mongodb_port,
)
mongodb = MongoClient(mongodb_url)[settings.mongodb_name]


def read_sensor() -> None:
    co2, temp = mon.read_data()
    temp = round(temp, 1) if temp else temp
    logger.info(f'CO2={co2} t={temp}')
    if co2 and temp:
        temp_gauge.set(temp)
        co2_gauge.set(co2)
        record = AirRecord(
            timestamp=datetime.now(),
            co2=co2,
            temperature=temp,
        ).dict()
        mongodb['records'].insert_one(record)


def run_scheduler():
    start_http_server(settings.metric_port)
    schedule.every().minute.do(read_sensor)
    while True:
        schedule.run_pending()
        time.sleep(1)
