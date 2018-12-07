import os, sys, re
from bs4 import BeautifulSoup

path = 'bbb.html'

with open(path) as fh:
    soup = BeautifulSoup(fh.read(), 'html.parser')


chara_div = soup.find('div', class_='t_c l_h_10').find_all('div', class_=re.compile('card_block f_l col3*'))
# とても可読性の低い書き方をしているがそういうことである
set_chara_1, ext = os.path.splitext(chara_div[0].find('img', class_='w_127')['src'].split('/')[-1])
set_chara_2, ext = os.path.splitext(chara_div[1].find('img', class_='w_127')['src'].split('/')[-1])
set_chara_3, ext = os.path.splitext(chara_div[2].find('img', class_='w_127')['src'].split('/')[-1])

set_chara_1_level = chara_div[0].find('span', class_='main_color').text
set_chara_2_level = chara_div[1].find('span', class_='main_color').text
set_chara_3_level = chara_div[2].find('span', class_='main_color').text

set_chara_1_attack = chara_div[0].find('span', class_='sub_color').text
set_chara_2_attack = chara_div[1].find('span', class_='sub_color').text
set_chara_3_attack = chara_div[2].find('span', class_='sub_color').text




sys.exit()

div = soup.find('table', class_='score_detail_table f_r')

# MAX COMBOはクラス名がつけられていないため以下の形でとれる
tr = div.find('tr', class_='')
max_combo = tr.find('td', class_='f_b').text

# CRITICAL_BREAK
tr = div.find('tr', class_='score_critical_break')
score_critical_break = tr.find('td', class_='f_b').text

# BREAK
# 面倒なので１行にまとめる(やっていることは上の２つと同じ)
_break = div.find('tr', class_='score_break').find('td', class_='f_b').text

# HIT
hit = div.find('tr', class_='score_hit').find('td', class_='f_b').text

# MISS
miss = div.find('tr', class_='score_miss').find('td', class_='f_b').text

# BELL
bell = div.find('tr', class_='score_bell').find('td', class_='f_b').text

# DAMAGE
damage = div.find('tr', class_='score_damage').find('td').text

# パーセンテージの値取得
table = soup.find('div', class_='col2 f_r p_5').find('table', class_='score_detail_table')

tr_list = table.find_all('tr')

tap       = tr_list[0].find('td', class_='f_b').text
hold      = tr_list[1].find('td', class_='f_b').text
flick     = tr_list[2].find('td', class_='f_b').text
side_tap  = tr_list[3].find('td', class_='f_b').text
side_hold = tr_list[4].find('td', class_='f_b').text

sys.exit()

print (max_combo)
print (score_critical_break)
print (_break)
print (hit)
print (miss)
print (bell)
print (damage)


