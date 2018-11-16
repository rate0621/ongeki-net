import sys, re
from bs4 import BeautifulSoup

path = 'bbb.html'

with open(path) as fh:
    soup = BeautifulSoup(fh.read(), 'html.parser')


div_list = soup.find('table', class_='score_detail_table f_r')

# MAX COMBOはクラス名がつけられていないため以下の形でとれる
tr = div_list.find('tr', class_='')

max_combo = tr.find('td', class_='f_b').text

tr = div_list.find('tr', class_='score_critical_break')

score_critical_break = tr.find('td', class_='f_b').text


print (max_combo)
print (score_critical_break)


