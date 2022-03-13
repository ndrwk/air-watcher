from loguru import logger
from prometheus_client import Gauge, start_http_server
import time
import schedule

from co2meter import CO2monitor

mon = CO2monitor()
co2_gauge = Gauge('CO2_ppm', 'CO2 in ppm')
temp_gauge = Gauge('Temperature', 'Temperature in Celsius')


def read_sensor() -> None:
    co2, temp = mon.read_data()
    temp = round(temp, 1) if temp else temp
    logger.info(f'CO2={co2} t={temp}')
    if co2 and temp:
        temp_gauge.set(temp)
        co2_gauge.set(co2)


def run_scheduler(metric_port: int):
    start_http_server(metric_port)
    schedule.every().minute.do(read_sensor)
    while True:
        schedule.run_pending()
        time.sleep(1)
