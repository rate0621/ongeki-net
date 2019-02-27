import sys, re
import csv
import sqlite3
import pandas as pd
import urllib.request
from urllib.parse import urlencode
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def getBaseRate():
    url = 'https://ongeki.gamerch.com/%E3%82%AA%E3%83%B3%E3%82%B2%E3%82%AD%20%E6%A5%BD%E6%9B%B2%E4%B8%80%E8%A6%A7%EF%BC%88Lv%E9%A0%86%EF%BC%89%E9%AB%98%E9%9B%A3%E6%98%93%E5%BA%A6'

    with urllib.request.urlopen(url) as res:
        html = res.read().decode("utf-8")
        res.close()

    soup = BeautifulSoup(html, 'html.parser')

    table_list = soup.find_all('tbody')

    music_list = []

    for table in table_list:
        if table.find('td', class_='no-min-width') is not None:
            tr_list = table.find_all('tr')
            for tr in tr_list:
                span_list = tr.find_all('span')
                info = {
                    'difficult'  : span_list[0].text,
                    'genre'      : span_list[1].text,
                    'title'      : span_list[2].text,
                    'total_notes': span_list[3].text.replace(',', ''),
                    'total_bells': span_list[4].text,
                    'base_rate'  : span_list[5].text,
                    'level'      : span_list[6].text,
                }

                music_list.append(info)


    header = music_list[0].keys()#ヘッダー用のデータを作っておく

    with open('base_rate.csv', 'w', newline='') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for musics in music_list:
            writer.writerow(musics)


def importBaseRateCsv():
    df = pd.read_csv("base_rate.csv")
    dbname = "../../../ongeki-data/ongeki.db"

    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    #if_existsでもしすでにbase_rateが存在していても、置き換えるように指示
    df.to_sql("baseratelist_music", conn, if_exists="replace", index_label='id')

    conn.close()



getBaseRate()
importBaseRateCsv()


