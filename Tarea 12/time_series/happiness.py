# -*- coding: utf-8 -*-
"""
Download world happiness time series from hedonometer project.
See https://hedonometer.org/timeseries/en_all/?from=2020-08-24&to=2022-02-23
Created on Tue Feb 24 15:35:23 2022

@author: Feliú Sagols
CDMX
"""
import csv
import datetime
import requests
from tools import loggers

TIMESERIES_DATABASE = "ts_db"

global LOGGER

# def last_available_date():
#     """
#     Returns the newest record base_date in happiness table
#     """
#     conn = psycopg2.connect("dbname=%s user=fsagols host=localhost" %
#                             TIMESERIES_DATABASE)
#     cur = conn.cursor()
#     cur.execute("""
#         select date_
#         from happiness
#         order by date_ desc
#         limit 1;
#         """)
#     date_ = cur.fetchone()[0]
#     conn.close()
#     return date_

# def get_happiness_ts(last_date, last_days):
#     """
#     Returns the happiness time series.
#
#     Parameters
#     ----------
#     last_date : datetime.pyi
#         Last base_date in the time period to download.
#     last_days:
#         Number of days previous to the last base_date to download.
#
#     Examples
#     --------
#     >>> get_happiness_ts(datetime.datetime(2022, 2, 26), 700)
#
#     Returns
#     -------
#         A dataframe with the time series.
#     """
#     conn = psycopg2.connect("dbname=%s user=fsagols host=localhost" %
#                             TIMESERIES_DATABASE)
#     cur = conn.cursor()
#     cur.execute(
#         """
#         select date_, happiness
#         from happiness
#         where date_ <= %(last_date)s
#         order by date_ desc limit %(last_days)s;
#         """, {
#             'last_date': last_date,
#             'last_days': last_days
#         })
#     answer = cur.fetchall()
#     answer.reverse()
#     answer = [[a[0], a[1]] for a in answer]
#     df = pd.DataFrame(data=answer, columns=['base_date', 'happiness'])
#     df.set_index('base_date', inplace=True)
#     return df


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
    # conn = psycopg2.connect("dbname=%s user=fsagols host=localhost" %
    #                         TIMESERIES_DATABASE)
    LOGGER.info("Storing happiness time series.")
    # cur = conn.cursor()
    # cur.executemany(
    #     """
    #     insert into happiness
    #     values (%s, %s, %s)
    #     on conflict (date_)
    #     do nothing;
    #     """, data)
    # conn.commit()
    # conn.close()
    return list(data_2)


LOGGER = loggers.define_logger("happiness.log")
date = datetime.datetime(2022, 1, 1)
data_3 = download_happiness(date, 5000)

with open("happiness.csv", "w", encoding='utf-8') as file_happy:
    writer = csv.writer(file_happy)
    for row in data_3:
        writer.writerow(row)


def retrieve_happiness(lista):
    """
    It retrieves happiness records between two dates with a jump of k days.
    With the option to also return the records between two other dates of our choosing

    Parameters
    ----------
    lista : List with two lists, the first list contains a start date, an end date, and an integer.
    The second list contains a start date, and an end date.
    """
    start_date = datetime.datetime.strptime(lista[0][0], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(lista[0][1], "%Y-%m-%d")
    index_1 = (end_date - date).days
    index_2 = (start_date - date).days

    with open("happiness.csv", "r", encoding='utf-8') as happy_file:
        reader = csv.reader(happy_file)
        data_2 = sorted(list(reader))
        dates_include_1 = list(range(index_2, index_1+1, lista[0][2]))
        if len(lista) == 2:
            index_3 = (datetime.datetime.strptime(lista[1][0], "%Y-%m-%d") - date).days
            index_4 = (datetime.datetime.strptime(lista[1][1], "%Y-%m-%d") - date).days
            dates_include_2 = list(range(index_3, index_4+1))
        else:
            dates_include_2 = []
        union_dates_include = sorted(list(set(dates_include_1+dates_include_2)))

        dates_show = []
        for i in union_dates_include:
            dates_show.append(data_2[i])
        return dates_show


print('\n'.join(str(d) for d in retrieve_happiness([['2022-01-01', '2022-01-22', 3],
                                                    ['2022-02-01', '2022-02-07']])))
