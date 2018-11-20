import sys, re
import csv
from bs4 import BeautifulSoup

path = 'test_datas/ccc.html'

with open(path) as fh:
    soup = BeautifulSoup(fh.read(), 'html.parser')


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
                'music_name' : span_list[2].text,
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

