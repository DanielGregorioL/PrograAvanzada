""" The so-called CSV (Comma Separated Values) format is the most common import
and export format for spreadsheets and databases."""
import csv
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import schedule


def dollar():
    """
    This function downloads and saves the value of a dollar in Mexican pesos in a csv file
    """
    page = requests.get("https://www.eldolar.info/es-MX/mexico/dia/hoy")
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find(class_="content")
    clase = content.find_all(class_="xTimes")
    element = clase[1]
    type_of = element.get_text()
    with open("dollar.csv", "a", encoding='utf-8') as file_cambio:
        writer = csv.writer(file_cambio)
        date = datetime.now()
        fila = [type_of, f"{date.year}-{date.month}-{date.day} "
                         f"{date.hour}:{date.minute}:{date.second}"]
        writer.writerow(fila)


hours1 = ["07:00", "08:00", "09:00", "10:00", "11:00"]
hours2 = ["12:00", "13:00", "14:00", "15:00", "16:00"]
hours = hours1+hours2

for i in range(10):
    schedule.every().day.at(hours[i]).do(dollar)

while 1:
    n = schedule.idle_seconds()
    time.sleep(n)
    schedule.run_pending()
