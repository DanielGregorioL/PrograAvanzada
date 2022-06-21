# -*- coding: utf-8 -*-
"""
Download world happiness time series from hedonometer project.
See https://hedonometer.org/timeseries/en_all/?from=2020-08-24&to=2022-02-23
Created on Tue Feb 24 15:35:23 2022

@author: Feliú Sagols
CDMX
"""

import datetime
import requests
import matplotlib.pyplot as plt
from tools import loggers

TIMESERIES_DATABASE = "ts_db"


def download_happiness(start_date, records):
    """
    Download happiness records from the url below. Happiness records are stored
    into happiness database table.

    Parameters
    ----------
    start_date : datetime.pyi
        Initial downloading base_date.
    records : int
        Maximum number of records after start_date to download.
    """
    LOGGER.debug("Downloading happiness time series.")
    data_json = requests.get(
        'https://hedonometer.org/api/v1/happiness/?format=json&timeseries__'
        f'title=en_all&date__gte='
        f'{start_date.strftime("%Y-%m-%d")}&limit={records}')
    data = data_json.json()
    data_2 = [[
        datetime.datetime.strptime(d['date'], "%Y-%m-%d"), d['frequency'],
        float(d['happiness'])
    ] for d in data['objects']]
    LOGGER.info("Storing happiness time series.")
    return list(data_2)


LOGGER = loggers.define_logger("happiness.log")
date = datetime.datetime(2022, 1, 1)
data_3 = download_happiness(date, 5000)

dates = []
happy = []

for element in data_3:
    date_index = element[0]
    date_str = f"{date_index.day}/{date_index.month}/{date_index.year}"
    dates.append(date_str)
    happy.append(element[2])

x = [datetime.datetime.strptime(d, "%d/%m/%Y").date() for d in dates]

print(dates)
print(happy)
plt.title("Serie de tiempo de la felicidad")
plt.xlabel("Fechas del año 2022")
plt.xticks(rotation=90)
plt.ylabel("Indice de felicidad en escala del 1 al 9 \n 1 significa " +
           "extremadamente negativo \n 5 neutral y 9 extremadamente positivo")
plt.plot_date(x, happy, c="blue", ls="--", lw=1)
plt.show()
