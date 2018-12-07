import sys, re
from bs4 import BeautifulSoup

path = 'datas/aaa.html'

with open(path) as fh:
    soup = BeautifulSoup(fh.read(), 'html.parser')


div_list = soup.find_all('div', class_='m_10')

log_list = []

for i, div in enumerate(div_list):
    # TODO: new recoredだったか否かも情報として抜くようにする。
    #       クラス名に_newがついてるかどうかで判断できるはず。
    play_date    = str(div.find('span', class_='f_r f_12 h_10').text).strip()
    music_name   = str(div.find('div',  class_='m_5 l_h_10 break').text).strip()

    #NOTE: [BATTLE SCORE]と[OVER DAMAGE]は、同じdivクラス(battle_score_block*)に入ってくる
    td_list = div.find_all('td', class_=re.compile('battle_score_block*'))
    battle_score = td_list[0].find('div',  class_='f_20').text
    over_damage  = td_list[1].find('div',  class_='f_20').text

    t_block = div.find('td',  class_=re.compile('technical_score_block*'))
    technical_score = t_block.find('div', class_='f_20').text

    idx = div.find('input')['value']

    s   = div.find('img')['src']
    print (s)
    if 'master' in s:
        print ('master!')
    else:
        print ('other')

    sys.exit()

    info = {
        'play_date'      : play_date,
        'music_name'     : music_name,
        'battle_score'   : battle_score,
        'over_damage'    : over_damage,
        'technical_score': technical_score,
        'idx'            : idx,
    }

    log_list.append(info)



url = 'https://ongeki-net.com/ongeki-mobile/record/playlogDetail/?idx=%s'

for i in log_list:
    aaa = url % i['idx']
    print (aaa)
