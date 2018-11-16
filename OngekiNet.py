import sys, os, re

import urllib.request
from urllib.parse import urlencode
import http.cookiejar
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


import headers

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
            play_date    = str(div.find('span', class_='f_r f_12 h_10').text).strip()
            music_name   = str(div.find('div',  class_='m_5 l_h_10 break').text).strip()

            #NOTE: [BATTLE SCORE]と[OVER DAMAGE]は、同じdivクラス(battle_score_block*)に入ってくる
            td_list = div.find_all('td', class_=re.compile('battle_score_block*'))
            battle_score = td_list[0].find('div',  class_='f_20').text
            over_damage  = td_list[1].find('div',  class_='f_20').text

            t_block = div.find('td',  class_=re.compile('technical_score_block*'))
            technical_score = t_block.find('div', class_='f_20').text
            idx = div.find('input')['value']

            info = {
                'play_date'      : play_date,
                'music_name'     : music_name,
                'battle_score'   : battle_score,
                'over_damage'    : over_damage,
                'technical_score': technical_score,
                'idx'            : idx,
            }

            play_log_list.append(info)

        return play_log_list

    def get_play_log_detail(self, idx):
        play_log_detail_url = 'https://ongeki-net.com/ongeki-mobile/record/playlogDetail/?idx=%s'
        url = play_log_detail_url % idx

        req = urllib.request.Request(url, None, headers.default_header)
        with urllib.request.urlopen(req, data=self.data) as res:
            html = res.read().decode("utf-8")
            res.close()

        print (html)


if __name__ == '__main__':
    args = sys.argv
    on = OngekiNet()

    on.login(args[1], args[2])
    play_log_list = on.getPlayLog()

    on.get_play_log_detail(play_log_list[0]['idx'])


