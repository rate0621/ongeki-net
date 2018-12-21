import sys, os, re
from time import sleep

import urllib.request
from urllib.parse import urlencode
import http.cookiejar
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


from lib import headers
from lib import db

class OngekiNet:
    def __init__(self):
        pass


    def login(self, name, password):
        # ログイン情報を保持させるため、CookieJarを作る
        self.cookiefile = "cookies.txt"
        self.cj = http.cookiejar.LWPCookieJar()
        if os.path.exists(self.cookiefile):
            self.cj.load(self.cookiefile)

        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(opener)


        # ログインする際にtokenが必要になるためtop画面よりいただく
        top_url    = 'https://ongeki-net.com/ongeki-mobile/'
        req = urllib.request.Request(top_url, None, headers.top_url_header)
        with urllib.request.urlopen(req) as res:
            html = res.read().decode("utf-8")
            cookie = res.getheader('Set-Cookie')
            res.close()

        soup = BeautifulSoup(html, "html.parser")
        token = soup.find(attrs={'name': 'token'}).get('value')
        cookie = cookie + '; segaId=' + name

        # ログイン
        login_post = {
            'segaId': name,
            'password': password,
            'save_cookie': "on",
            'token': token
        }
        self.data = urllib.parse.urlencode(login_post).encode("utf-8")

        submit_url = 'https://ongeki-net.com/ongeki-mobile/submit/'
        req = urllib.request.Request(submit_url, None, headers.default_header)
        with urllib.request.urlopen(req, data=self.data) as res:
            html = res.read().decode("utf-8")
            res.close()


        # ログイン後のaime選択画面を突破
        aime_url = 'https://ongeki-net.com/ongeki-mobile/aimeList/submit/?idx=0'
        req = urllib.request.Request(aime_url, None, headers.default_header)
        with urllib.request.urlopen(req, data=self.data) as res:
            html = res.read().decode("utf-8")
            res.close()


    def getPlayLog(self):
        url = 'https://ongeki-net.com/ongeki-mobile/record/playlog/'
        req = urllib.request.Request(url, None, headers.default_header)
        with urllib.request.urlopen(req, data=self.data) as res:
            html = res.read().decode("utf-8")
            res.close()

        soup = BeautifulSoup(html, 'html.parser')

        div_list = soup.find_all('div', class_='m_10')

        play_log_list = []

        for i, div in enumerate(div_list):
            # TODO: new recoredだったか否かも情報として抜くようにする。
            #       クラス名に_newがついてるかどうかで判断できるはず。

            # 曲名のIDの所在がわからないため、ジャケ写のpngのファイル名をID代わりに取得しておく
            img_url           = div.find('img',  class_='m_5 f_l')
            jacket_file_name  = img_url['src'].split('/')[-1]
            jacket_id, ext = os.path.splitext(jacket_file_name)

            play_date    = str(div.find('span', class_='f_r f_12 h_10').text).strip()
            music_name   = str(div.find('div',  class_='m_5 l_h_10 break').text).strip()

            #NOTE: [BATTLE SCORE]と[OVER DAMAGE]は、同じdivクラス(battle_score_block*)に入ってくる
            td_list = div.find_all('td', class_=re.compile('battle_score_block*'))
            battle_score = td_list[0].find('div',  class_='f_20').text
            over_damage  = td_list[1].find('div',  class_='f_20').text

            t_block = div.find('td',  class_=re.compile('technical_score_block*'))
            technical_score = t_block.find('div', class_='f_20').text
            idx = div.find('input')['value']

            difficult_img = div.find('img')['src']

            # NOTE: 本当は各難易度でしっかりとわけたいが、
            #       それのためにわざわざEXPERT以下の難易度をプレイするのを大変なので、
            #       MASTER以外は全部EXPERTとする
            if 'master' in difficult_img:
                difficult = 'MASTER'
            else:
                difficult = 'EXPERT'

            info = {
                'jacket_id'      : jacket_id,
                'play_date'      : play_date,
                'music_name'     : music_name,
                'difficult'      : difficult,
                'battle_score'   : battle_score.replace(',', ''),
                'over_damage'    : over_damage.replace('％', ''),
                'technical_score': technical_score.replace(',', ''),
                'idx'            : idx,
            }

            play_log_list.append(info)

        return play_log_list

    def getPlayLogDetail(self, idx):
        play_log_detail_url = 'https://ongeki-net.com/ongeki-mobile/record/playlogDetail/?idx=%s'
        url = play_log_detail_url % idx

        req = urllib.request.Request(url, None, headers.default_header)
        with urllib.request.urlopen(req, data=self.data) as res:
            html = res.read().decode("utf-8")
            res.close()

        soup = BeautifulSoup(html, 'html.parser')

        # まずセットしていたキャラクターの情報を取得
        chara_div = soup.find('div', class_='t_c l_h_10').find_all('div', class_=re.compile('card_block f_l col3*'))
        # とても可読性の低い書き方をしているがそういうことである
        set_chara_1, ext   = os.path.splitext(chara_div[0].find('img', class_='w_127')['src'].split('/')[-1])
        set_chara_2, ext   = os.path.splitext(chara_div[1].find('img', class_='w_127')['src'].split('/')[-1])
        set_chara_3, ext   = os.path.splitext(chara_div[2].find('img', class_='w_127')['src'].split('/')[-1])

        set_chara_1_level  = chara_div[0].find('span', class_='main_color').text
        set_chara_2_level  = chara_div[1].find('span', class_='main_color').text
        set_chara_3_level  = chara_div[2].find('span', class_='main_color').text

        set_chara_1_attack = chara_div[0].find('span', class_='sub_color').text
        set_chara_2_attack = chara_div[1].find('span', class_='sub_color').text
        set_chara_3_attack = chara_div[2].find('span', class_='sub_color').text


        div = soup.find('table', class_='score_detail_table f_r')

        # MAX COMBOはクラス名がつけられていないため以下の形でとれる
        tr = div.find('tr', class_='')
        max_combo = tr.find('td', class_='f_b').text

        # CRITICAL_BREAK
        tr = div.find('tr', class_='score_critical_break')
        critical_break = tr.find('td', class_='f_b').text

        # BREAK
        # 面倒なので１行にまとめる(やっていることは上の２つと同じ)
        _break = div.find('tr', class_='score_break').find('td', class_='f_b').text

        # HIT
        hit    = div.find('tr', class_='score_hit').find('td', class_='f_b').text

        # MISS
        miss   = div.find('tr', class_='score_miss').find('td', class_='f_b').text

        # BELL
        bell   = div.find('tr', class_='score_bell').find('td', class_='f_b').text

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


        detail = {
            'set_chara_1'        : set_chara_1,
            'set_chara_1_level'  : set_chara_1_level.replace('Lv.', ''),
            'set_chara_1_attack' : set_chara_1_attack,
            'set_chara_2'        : set_chara_2,
            'set_chara_2_level'  : set_chara_2_level.replace('Lv.', ''),
            'set_chara_2_attack' : set_chara_2_attack,
            'set_chara_3'        : set_chara_3,
            'set_chara_3_level'  : set_chara_3_level.replace('Lv.', ''),
            'set_chara_3_attack' : set_chara_3_attack,
            'max_combo'          : max_combo.replace(',', ''),
            'critical_break'     : critical_break.replace(',', ''),
            '_break'             : _break.replace(',', ''),
            'hit'                : hit.replace(',', ''),
            'miss'               : miss.replace(',', ''),
            'bell'               : bell.replace(',', ''),
            'damage'             : damage.replace(',', ''),
            'tap'                : tap.replace('%', ''),
            'hold'               : hold.replace('%', ''),
            'flick'              : flick.replace('%', ''),
            'side_tap'           : side_tap.replace('%', ''),
            'side_hold'          : side_hold.replace('%', ''),
        }

        return detail


if __name__ == '__main__':
    args = sys.argv
    on = OngekiNet()
    db = db.Db()
    last_play_date = db.getLastPlayDate()

    on.login(args[1], args[2])
    play_log_list = on.getPlayLog()

    for i, play_log in enumerate(play_log_list):
        if play_log['play_date'] == last_play_date:
            print ('weeeei')
            break


        detail = on.getPlayLogDetail(play_log['idx'])
        play_log_list[i].update(detail)

        db.insertPlayDetail(play_log_list[i])
        sleep(5)


    print ('END')
